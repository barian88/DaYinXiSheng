package com.example.backend.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.example.backend.dto.PostDTO;
import com.example.backend.entity.Post;

import java.util.List;

public interface PostService extends IService<Post> {

    /**
    * @description: 获取一页post
    * @param: 当前页，页大小
    * @return: postDTO列表，包括Post,Music,User的信息
    * @date: 2024/5/13 20:46
    */
    List<PostDTO> getPostPage(int pageCount, int pageSize);

    /**
    * @description: 新增post
    * @param: post
    * @return: 新增的记录数
    * @date: 2024/5/16 11:19
    */
    int insertPost(Post post);

}
