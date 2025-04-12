package com.example.backend.service;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.extension.service.IService;
import com.example.backend.entity.Music;

import java.util.List;

public interface MusicService extends IService<Music> {

    /**
    * @description: 根据music的Id查询
    * @param:
    * @return:
    * @date: 2024/5/13 20:40
    */
    Music getMusicById(int id);


    /**
    * @description: 音乐列表的分页查询
    * @param: 当前页，页大小，用户id，根据音乐名称或歌手模糊查询的条件
    * @return:
    * @date: 2024/5/21 19:05
    */
    JSONObject getMusicPage(int pageCount, int pageSize, int userId, String titleOrArtist);

    /**
    * @description: 添加音乐
    * @param: music对象
    * @return: 新增记录数
    * @date: 2024/5/22 0:34
    */
    int insertMusic(Music music);

    /**
    * @description: 根据id和userId删除音乐
    * @param: id,userId
    * @return: 变更记录数
    * @date: 2024/5/22 1:03
    */
    int deleteMusicByIdAndUserId(int id, int userId);

}
