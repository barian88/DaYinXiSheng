package com.example.backend.controller;

import com.alibaba.fastjson.JSONObject;
import com.example.backend.entity.Music;
import com.example.backend.service.MusicService;
import com.example.backend.utils.AjaxResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
* @description:
* @date: 2024/5/13 14:46
*/
@RestController
@RequestMapping("/music")
public class MusicController {

    @Autowired
    MusicService musicService;

    @GetMapping("/getMusicPage")
    AjaxResult getMusicPage(@RequestParam("pageCount") Integer pageCount,
                            @RequestParam("pageSize")Integer pageSize,
                            @RequestParam("userId")Integer userId,
                            @RequestParam(value = "titleOrArtist", required = false)String titleOrArtist) {

        JSONObject result = musicService.getMusicPage(pageCount, pageSize, userId, titleOrArtist);
        List<Music> list = (List<Music>) result.get("list");
        if (list.size() == 0) {
            return AjaxResult.success("没有更多数据了", result);
        }
        return AjaxResult.success(result);
    }

    @PostMapping("/insertMusic")
    AjaxResult insertMusic(@RequestBody Music music) {
        if (music == null) {
            return AjaxResult.error("参数错误");
        }
        int result = musicService.insertMusic(music);
        if (result == 1) {
            return AjaxResult.success("新增成功");
        }
        return AjaxResult.error("新增失败");
    }

    @DeleteMapping("/deleteMusic")
    AjaxResult deleteMusicByIdAndUserId(Integer id, Integer userId) {
        if (id == null || userId == null) {
            return AjaxResult.error("参数错误");
        }
        int result = musicService.deleteMusicByIdAndUserId(id, userId);
        if (result == 1) {
            return AjaxResult.success("删除成功");
        }
        return AjaxResult.error("删除失败");
    }

}


