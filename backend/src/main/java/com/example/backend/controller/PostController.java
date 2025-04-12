package com.example.backend.controller;

import com.example.backend.dto.PostDTO;
import com.example.backend.entity.Post;
import com.example.backend.service.PostService;
import com.example.backend.utils.AjaxResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
* @description:
* @date: 2024/5/13 16:39
*/
@RestController
@RequestMapping("/post")
public class PostController {

    @Autowired
    PostService postService;

    @GetMapping("/getPostPage")
    AjaxResult getPostPage(Integer pageCount, Integer pageSize){
        List<PostDTO> list = postService.getPostPage(pageCount, pageSize);
        if (list.size() == 0) {
            return AjaxResult.success("没有更多数据了", list);
        }
        return AjaxResult.success(list);
    }

    @PostMapping("/insertPost")
    AjaxResult insertPost(@RequestBody Post post){
        if (post == null) {
            return AjaxResult.error("参数错误");
        }
        int result = postService.insertPost(post);
        if (result == 1) {
            return AjaxResult.success("新增成功");
        }
        return AjaxResult.error("新增失败");
    }
}
