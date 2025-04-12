import os
import json

import numpy as np
import pandas as pd
import torch
from PIL import Image
from torchvision import transforms
import cv2
from shutil import copyfile
from pydub import AudioSegment
import ffmpeg
import shutil
from urllib.request import urlopen


from app.python.model import ResNet, BasicBlock

MAXSECOND = 15.0    # 最长视频秒数
TEMPDIR = "./app/python/temp/" # 临时缓存文件夹地址
N = 5   # 预测的最优配乐数


def resnet34(num_classes=1000, include_top=True):
    # https://download.pytorch.org/models/resnet34-333f7ec4.pth
    return ResNet(BasicBlock, [3, 4, 6, 3], num_classes=num_classes, include_top=include_top)

# 预测视频情绪值
# 输入图片url
# 输出情绪值
def predict(img_url):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")     # 假如能用gpu就用0号gpu，没有就用cpu

    # 图像预处理：缩放，切割等
    data_transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.CenterCrop(224), #从中心取出224*224
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    # load image
    print("predict:"+str(img_url))
    cap = cv2.VideoCapture(img_url)
    print("predict:"+str(cap.isOpened()))
    ret, img = cap.read() #读取一帧图像, ret 是一个布尔值，表示是否成功读取图像
    img = Image.fromarray(img) #NumPy的图像转换为 PIL 图像格式
    cap.release()
    img = data_transform(img)
    # [N, C, H, W]
    # expand batch dimension  增加一个新维度：N batch size C 通道数 H 高度 W宽度
    img = torch.unsqueeze(img, dim=0)

    # create model
    model = resnet34(num_classes=2).to(device)

    # load model weights
    weights_path = "./app/python/resNet34.pth"
    assert os.path.exists(weights_path), "file: '{}' dose not exist.".format(weights_path)
    model.load_state_dict(torch.load(weights_path, map_location=device))

    # prediction  切换到评估模式
    model.eval()
    # 不对损失梯度进行跟踪
    with torch.no_grad():
        # predict class
        # 压缩batch维度
        output = torch.squeeze(model(img.to(device))).cpu()
        # 用softmax处理得到概率分布
        predict = torch.softmax(output, dim=0)

    # 输出情绪值， predict[0] 取得预测结果中第一个类别的概率
    emo = float(predict[0].numpy())

    return emo


# 前端需要控制一下输入的n不能超过120
# 根据情绪值匹配n个音乐
# 返回匹配的音乐列表
def musicMatch(emo):
    # 创建导出的列表
    music_list = []
    # 导入音乐库
    music_database = pd.read_excel("./app/python/music database.xlsx")
    # 匹配   id i+1 是完成表格中的index和数据库中id的对应
    for i, line in music_database.iterrows():
        emo_dis = abs(emo - line["value"])
        if len(music_list) < N:
            music_list.append({"id": i + 1, "title": line["title"], "artist": line["artist"], "value": line["value"],
                               "url": line["url"], "dis": emo_dis})
        else:
            music_list.sort(key=lambda dic: dic["dis"])
            if emo_dis < music_list[N - 1]["dis"]:
                music_list[N - 1] = {"id": i + 1, "title": line["title"], "artist": line["artist"], "value": line["value"],
                                     "url": line["url"], "dis": emo_dis}
            else:
                break

    return music_list


# 导入视频并处理（裁剪至15秒内，并将视频存到temp里）
# 输入视频的url
# 返回视频是否超过xx秒（超过1，不超过0），处理好后的视频地址
def getVideo(video_url):
    print(video_url)
    cap = cv2.VideoCapture(video_url)  # 打开视频文件
    print(cap.isOpened())
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # 获得视频文件的帧宽
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 获得视频文件的帧高
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 获得视频文件的帧数
    fps = cap.get(cv2.CAP_PROP_FPS)  # 获得视频文件的帧率
    video_length = frames / fps  # 计算视频长度/s

    # 创建存放处理后的视频的路径
    processed_video_path = os.path.join(TEMPDIR, "video.mp4")
    if not os.path.isdir(TEMPDIR):
        os.mkdir(TEMPDIR)

    if video_length > MAXSECOND:    # 如果原视频长度大于xx秒就裁剪
        flag = 1
        # 创建保存视频文件类对象
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(processed_video_path, fourcc, fps, (int(width), int(height)))

        # 设置帧读取的开始位置
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        pos = cap.get(cv2.CAP_PROP_POS_FRAMES)  # 获得帧位置
        while pos <= MAXSECOND * fps:
            ret, frame = cap.read()  # 捕获一帧图像
            out.write(frame)  # 保存帧
            pos = cap.get(cv2.CAP_PROP_POS_FRAMES)

        out.release()
    else:                           # 如果原视频小于xx秒就直接下载视频到temp
        flag = 0
        # 从网络上下载视频到本地
        f = open(processed_video_path, 'wb')
        url = urlopen(video_url)
        content = url.read()
        f.write(content)
        f.close()

    cap.release()
    return flag, processed_video_path


# 处理目标音乐
# 输入是音乐地址，处理好的视频地址（用于获取视频长度）
# 输出是处理好的音乐地址
def getMusic(music_url, video_path):
    # 从网络上下载音乐到本地
    full_music_path = os.path.join(TEMPDIR, "full_music.wav")
    if not os.path.isdir(TEMPDIR):
        os.mkdir(TEMPDIR)
    f = open(full_music_path, 'wb')
    url = urlopen(music_url)
    content = url.read()
    f.write(content)
    f.close()

    # 读取音频文件
    wav = AudioSegment.from_wav(full_music_path)

    # 得到视频长度
    cap = cv2.VideoCapture(video_path)  # 打开视频文件
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 获得视频文件的帧数
    fps = cap.get(cv2.CAP_PROP_FPS)  # 获得视频文件的帧率
    video_length = frames / fps  # 计算视频长度/s
    cap.release()

    # 读取前xx秒的音频并保存在music.wav中
    processed_music_path = os.path.join(TEMPDIR, "music.wav")
    if not os.path.isdir(TEMPDIR):
        os.mkdir(TEMPDIR)
    wav[:video_length * 1000].export(processed_music_path, format="wav")

    return processed_music_path


# 将图片列表转化为xx秒的视频
# 输入：图片url列表
# 输出：生成的视频的地址
def getImgVideo(img_list):
    fps = 30
    width = 1280
    height = 720
    img_mat_list = []

    print("at getImgVideo")

    # 根据img_list中的url读取图片存放到img_mat_list
    for img_url in img_list:
        # load image
        cap = cv2.VideoCapture(img_url)
        print(cap.isOpened())
        ret, img = cap.read()
        h, w = img.shape[0:2]
        if h*16 > w*9:
            img = cv2.resize(img, (width, int(h*(width/w))))
            h_center = (int(h*(width/w)) - height)//2
            img = img[h_center: h_center+height, 0: width]
        elif h*16 == w*9:
            img = cv2.resize(img, (width, int(h * (width / w))))
        else:
            img = cv2.resize(img, (int(w*(height/h)), height))
            w_center = (int(w*(height/h)) - width)//2
            img = img[0: height, w_center: w_center+width]
        img_mat_list.append(img)
        cap.release()
    img_mat_list.append(np.zeros((height, width, 3), dtype=np.uint8))     # 最后增加一个黑屏

    # 创建存放处理后的视频的路径
    processed_video_path = os.path.join(TEMPDIR, "video.mp4")
    if not os.path.isdir(TEMPDIR):
        os.mkdir(TEMPDIR)

    # 创建保存视频文件类对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(processed_video_path, fourcc, fps, (width, height))

    # 生成视频
    frames_each_img = int(MAXSECOND*fps / len(img_list))    # 每张图片占的帧数
    frames_fade = int(fps/2)    # 渐变部分占的帧数
    pos = 0
    for i in range(len(img_list)):  # 遍历每张图片
        for f in range(frames_each_img-frames_fade):    # 内容
            frame = cv2.addWeighted(img_mat_list[i], 1, img_mat_list[i + 1], 0, 0)
            out.write(frame)
            pos = pos + 1
        for f in range(frames_fade):    # 渐变
            x = f/(frames_fade-1)
            y = 1-x
            frame = cv2.addWeighted(img_mat_list[i], y, img_mat_list[i+1], x, 0)
            out.write(frame)
            pos = pos + 1

    while pos < MAXSECOND*fps:  # 不足xx秒用黑屏补足
        out.write(img_mat_list[-1])
        pos = pos + 1

    out.release()

    print(processed_video_path)

    return processed_video_path


# 拼接音乐和视频
# 输入是处理好的音乐和视频地址
# 输出是合并后的视频地址
def concatMV(music_path, video_path):
    video = ffmpeg.input(video_path)
    music = ffmpeg.input(music_path)

    output_path = os.path.join(TEMPDIR, "output.mp4")
    ffmpeg.concat(video, music, v=1, a=1).output(output_path).run()

    return output_path


# 对视频进行截图，截好的图片用于情绪分析
# 输入是处理好的视频地址
# 输入是存放截图的文件夹
def getEmoFrames(video_path):
    cap = cv2.VideoCapture(video_path)  # 打开视频文件
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 获得视频文件的帧数
    fps = cap.get(cv2.CAP_PROP_FPS)  # 获得视频文件的帧率
    video_length = frames / fps  # 计算视频长度/s

    # 创建存放截图的文件夹
    cutimg_dir = os.path.join(TEMPDIR, "./cut/")
    if not os.path.isdir(cutimg_dir):
        os.mkdir(cutimg_dir)

    # 获取截图
    for t in range(int(video_length)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, t * fps)
        ret, frame = cap.read()
        cutimg_path = os.path.join(cutimg_dir, "img_{}.jpg".format(t))
        cv2.imwrite(cutimg_path, frame)
    cap.release()

    # 将封面复制到temp
    cover_path = os.path.join(TEMPDIR, "cover.jpg")
    copyfile(os.path.join(cutimg_dir, "img_0.jpg"), cover_path)

    return cutimg_dir


# 计算视频的情绪值
# 输入是处理好的视频地址
# 输出是视频的情绪值
def predictMulti(img_list):
    emo_list = []

    # 逐个截图判断其情绪值并存入emo_list
    for img_url in img_list:
        emo_list.append(predict(img_url))

    # 帧的中间情绪值作为多图情绪值
    emo_list.sort()
    emo = emo_list[len(emo_list)//2]

    return emo


# 计算单张图片的情绪值
# 输入是单张图片的地址
# 输出是图片的情绪值
def singleImgEmo(img_url):
    return predict(img_url)


# 计算多张图片的情绪值
# 输入是多张图片的地址（列表形式）
# 输出是图片的情绪值
def multiImgEmo(img_list):
    return predictMulti(img_list)


# 计算视频的情绪值
# 输入是视频的地址
# 输出是视频的情绪值
def videoEmo(video_path):
    frames_path = getEmoFrames(video_path)
    frame_list = os.listdir(frames_path)

    for i in range(len(frame_list)):
        frame_list[i] = os.path.join(frames_path, frame_list[i])

    return multiImgEmo(frame_list)


# 获取音乐的情绪
# 输入是音乐地址
# 输出是音乐的情绪值
def getMusicEmo(music_path):
    from app.python.music_emo import getEmo

    return {"emo": getEmo(music_path)}

# 清空temp文件夹
def clear_temp():
    if os.path.isdir(TEMPDIR):
        shutil.rmtree(TEMPDIR)


if __name__ == '__main__':
    # # 图片配乐
    # img_url = "http://rialb9qcc.hd-bkt.clouddn.com/299KAfqLUpoQG2NE.png"    # 输入图片url
    # emo = singleImgEmo(img_url)
    # print(emo)
    # music = musicMatch(emo)
    # print(music)
    #
    # # 视频配乐
    # video_url = "http://rijsxyzz7.bkt.clouddn.com/VID-1.mp4"
    # flag, processed_video_path = getVideo(video_url)
    # if flag == 1:
    #     print("视频长度大于15秒！")
    #
    # emo = videoEmo(processed_video_path)
    # print(emo)
    # cover_path = os.path.join(TEMPDIR, "cover.jpg")
    # music = musicMatch(emo)
    # print(music)
    #
    # music_path = music[0]["url"]
    # processed_music_path = getMusic(music_path, processed_video_path)
    # concatMV(processed_music_path, processed_video_path)
    #
    # # 多图配乐
    # img_list = ["http://rijsxyzz7.bkt.clouddn.com/IMGA.jpg", "http://rijsxyzz7.bkt.clouddn.com/IMGB.jpg",
    #             "http://rijsxyzz7.bkt.clouddn.com/IMGC.jpg", "http://rijsxyzz7.bkt.clouddn.com/IMGD.jpg"]
    # emo = multiImgEmo(img_list)
    # print(emo)
    # music = musicMatch(emo)
    # print(music)

    # 多图生成配乐视频
    img_list = ["http://rijsxyzz7.bkt.clouddn.com/IMG-1.jpg", "http://rijsxyzz7.bkt.clouddn.com/IMG-2.jpg",
                "http://rijsxyzz7.bkt.clouddn.com/IMG-3.jpg", "http://rijsxyzz7.bkt.clouddn.com/IMG-4.jpg",
                "http://rijsxyzz7.bkt.clouddn.com/IMG-5.jpg", "http://rijsxyzz7.bkt.clouddn.com/IMG-6.jpg",
                "http://rijsxyzz7.bkt.clouddn.com/IMG-7.jpg", "http://rijsxyzz7.bkt.clouddn.com/IMG-8.jpg",
                "http://rijsxyzz7.bkt.clouddn.com/IMG-9.jpg"]
    processed_video_path = getImgVideo(img_list)
    emo = multiImgEmo(img_list)
    print(emo)
    music = musicMatch(emo)
    print(music)
    music_path = music[0]["url"]
    processed_music_path = getMusic(music_path, processed_video_path)
    concatMV(processed_music_path, processed_video_path)

    # # 清除temp文件夹
    # clear_temp()


