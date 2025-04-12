import torch
import torch.nn as nn
import torchvision.models as models
import librosa
import numpy as np
import os


# 定义模型架构
class EmotionResNet(nn.Module):
    def __init__(self, base_model):
        super(EmotionResNet, self).__init__()
        self.base_model = base_model
        self.base_model.fc = nn.Sequential(
            nn.Linear(self.base_model.fc.in_features, 1),
            nn.Sigmoid()  # 添加Sigmoid激活函数
        )

    def forward(self, x):
        return self.base_model(x)


# 加载预训练的ResNet-34模型
resnet34 = models.resnet34(pretrained=False)  # 注意：这里不需要预训练参数
model = EmotionResNet(resnet34)

# 加载训练好的模型参数
model.load_state_dict(torch.load('app/python/music_emo.pth'))
model.eval()


# 提取梅尔频谱图函数
def extract_mel_spectrogram(audio_filename, max_len=128):
    try:
        y, sr = librosa.load(audio_filename)
        mel_spect = librosa.feature.melspectrogram(y=y, sr=sr)
        mel_spect_db = librosa.power_to_db(mel_spect, ref=np.max)

        if mel_spect_db.shape[1] > max_len:
            mel_spect_db = mel_spect_db[:, :max_len]
        else:
            pad_width = max_len - mel_spect_db.shape[1]
            mel_spect_db = np.pad(mel_spect_db, ((0, 0), (0, pad_width)), mode='constant')

        # 将单通道复制为三通道
        mel_spect_db = np.stack([mel_spect_db] * 3, axis=0)

        return mel_spect_db
    except Exception as e:
        print(f"Error loading {audio_filename}: {e}")
        return None


# 预测函数
def predict_emotion(audio_path):
    mel_spectrogram = extract_mel_spectrogram(audio_path)
    if mel_spectrogram is not None:
        mel_spectrogram = torch.tensor(mel_spectrogram, dtype=torch.float32).unsqueeze(0)  # 增加batch维度
        with torch.no_grad():
            prediction = model(mel_spectrogram)
        return prediction.item()
    else:
        return None


# 示例：预测一个新音频文件的情绪值
audio_path = 'D:\\musicdata\\music_recommendation\\9CJ46UV495.wav'
# audio_path = 'https://bucket-1305916869.cos.ap-beijing.myqcloud.com/music_recommendation/06BA9LHRT0.wav'

def getEmo(audio_path):
    emotion_value = predict_emotion(audio_path)
    return emotion_value
