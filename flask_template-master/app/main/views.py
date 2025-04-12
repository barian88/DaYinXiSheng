#-*- coding=utf-8 -*-
import json
import os

import numpy as np
from flask import render_template, session, redirect, url_for, current_app, request, send_from_directory, make_response, \
    send_file

from app.python.main import predict, getVideo, getEmoFrames, videoEmo, musicMatch, getMusic, concatMV, clear_temp, \
    predictMulti, getImgVideo, getMusicEmo
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))


# 单张图片匹配音乐
@main.route('/singleImgEmo', methods=['GET', 'POST'])
def singleImgEmo():

    if request.method == 'GET':
        imgUrl = request.args.get('imgUrl')
    elif request.method == 'POST':
        imgUrl = request.args.get('imgUrl')
    emoValue = predict(imgUrl)
    # 匹配音乐
    musicList = musicMatch(emoValue)

    return json.dumps({"emoValue": emoValue, "musicList": musicList})

# 视频匹配音乐
@main.route('/matchMusicForVideo', methods=['GET', 'POST'])
def matchMusicForVideo():
    clear_temp()
    # 获取视频url参数
    videoUrl = request.args.get('videoUrl')
    #print(videoUrl)
    # 处理视频
    flag, processedVideoPath = getVideo(videoUrl)
    # 获取视频情绪值
    emoValue = videoEmo(processedVideoPath)
    # 根据情绪值匹配音乐
    musicList = musicMatch(emoValue)
    return json.dumps({"emoValue": emoValue, "musicList": musicList, "processedVideoPath": processedVideoPath})

# 拼接视频与音乐
@main.route('/exportVideo', methods=['GET', 'POST'])
def exportVideo():
    filePath = "app/python/temp/output.mp4"
    # print(os.path.exists(filePath))
    if os.path.exists(filePath):
        os.remove(filePath)
    # 获取处理好的视频地址
    processedVideoPath = request.args.get("processedVideoPath")
    # 获取音乐的url
    musicUrl = request.args.get("musicUrl")
    #print(processedVideoPath)
    #print(musicUrl)
    # 处理音乐
    processedMusicPath = getMusic(musicUrl, processedVideoPath)
    outPutPath = concatMV(processedMusicPath, processedVideoPath)

    return send_file("python/temp/output.mp4",
                     as_attachment=True,
                     )

# 多图匹配
@main.route('/multiImg', methods=['GET', 'POST'])
def multiImg():
    imgList = request.args.getlist('imgList')
    emoValue = predictMulti(np.array(imgList))
    # 根据情绪值匹配音乐
    musicList = musicMatch(emoValue)
    return json.dumps({"emoValue": emoValue, "musicList": musicList})

# 多张图片生成视频并配乐
@main.route('/getVideoForImages', methods=['GET', 'POST'])
def getVideoForImages():
    imgList = request.args.getlist('imgList')
    musicUrl = request.args.get("musicUrl")

    filePath = "app/python/temp/output.mp4"
    # print(os.path.exists(filePath))
    if os.path.exists(filePath):
        os.remove(filePath)

    # 图片拼接为视频
    processedVideoPath = getImgVideo(np.array(imgList))
    # 处理音乐
    processedMusicPath = getMusic(musicUrl, processedVideoPath)
    # 拼接
    outPutPath = concatMV(processedMusicPath, processedVideoPath)

    return send_file("python/temp/output.mp4",
                     as_attachment=True,
                     )

# 获取音乐的情绪值
@main.route('/getMusicEmo', methods=['POST'])
def getMusicEmoApi():
    file = request.files['file']
    if file:
        filePath = "app/python/temp/toAnalyseMusic.wav"
        # 删除旧文件
        if os.path.exists(filePath):
            os.remove(filePath)
        # 保存新文件
        file.save(filePath)
        return getMusicEmo(filePath)
    return {"error": "no file"}