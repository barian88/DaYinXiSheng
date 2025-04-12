package com.example.backend.service.impl;


import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.backend.dto.PostDTO;
import com.example.backend.entity.Music;
import com.example.backend.entity.Post;
import com.example.backend.mapper.MusicMapper;
import com.example.backend.service.MusicService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

/**
* @description: 根据music的Id查询
* @date: 2024/5/13 14:36
*/
@Service
public class MusicServiceImpl extends ServiceImpl<MusicMapper, Music> implements MusicService {

    @Autowired
    MusicMapper musicMapper;
    /**
     * @description: 根据music的Id查询
     * @param:
     * @return:
     * @date: 2024/5/13 20:40
     */
    @Override
    public Music getMusicById(int id) {
        return musicMapper.selectById(id);
    }

    /**
     * @description: 音乐列表的分页查询
     * @param:
     * @return:
     * @date: 2024/5/21 19:05
     */
    @Override
    public JSONObject getMusicPage(int pageCount, int pageSize, int userId, String titleOrArtist) {

        //        构造查询条件
        QueryWrapper<Music> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("user_id", userId);
        queryWrapper.like("title", titleOrArtist);
        queryWrapper.or();
        queryWrapper.like("artist", titleOrArtist);

        Page<Music> page = new Page<>(pageCount, pageSize);

        IPage<Music> postIPage = musicMapper.selectPage(page,queryWrapper);
        JSONObject result = new JSONObject();
//        如果当前页数大于总页数，返回空列表
        if (postIPage.getPages() < pageCount) {
            result.put("list", new ArrayList<>());
            return result;
        }
//        正常情况，返回这一页的数据
        result.put("list", postIPage.getRecords());
        result.put("totalPages",
                postIPage.getTotal() % pageSize == 0 ? postIPage.getTotal() / pageSize : postIPage.getTotal() / pageSize + 1);
        result.put("totalRecords", postIPage.getTotal());

        return result;
    }

    /**
     * @description: 添加音乐
     * @param: music对象
     * @return: 新增记录数
     * @date: 2024/5/22 0:34
     */
    @Override
    public int insertMusic(Music music) {
        DecimalFormat decimalFormat = new DecimalFormat("#.000000");
        music.setValue(Double.parseDouble(decimalFormat.format(music.getValue())));
//        System.out.println(music.getValue());
        return musicMapper.insert(music);
    }

    /**
     * @description: 根据id和userId删除音乐
     * @param: id,userId
     * @return: 变更记录数
     * @date: 2024/5/22 1:03
     */
    @Override
    public int deleteMusicByIdAndUserId(int id, int userId) {
        QueryWrapper<Music> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("id", id);
        queryWrapper.eq("user_id", userId);
        return musicMapper.delete(queryWrapper);
    }

}
