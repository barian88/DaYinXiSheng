package com.example.backend.service.impl;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.backend.dto.PostDTO;
import com.example.backend.entity.Post;
import com.example.backend.mapper.PostMapper;
import com.example.backend.service.MusicService;
import com.example.backend.service.PostService;
import com.example.backend.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
 * @description:
 * @date: 2024/5/13 14:36
 */
@Service
public class PostServiceImpl extends ServiceImpl<PostMapper, Post> implements PostService {

    @Autowired
    PostMapper postMapper;
    @Autowired
    MusicService musicService;
    @Autowired
    UserService userService;

    /**
     * @description: 获取一页post
     * @param: 当前页，页大小
     * @return: postDTO列表，包括Post,Music,User的信息
     * @date: 2024/5/13 20:46
     */
    @Override
    public List<PostDTO> getPostPage(int pageCount, int pageSize) {

        Page<Post> page = new Page<>(pageCount, pageSize);
        IPage<Post> postIPage = postMapper.selectPage(page, null);
//        如果当前页数大于总页数，返回空列表
        if (postIPage.getPages() < pageCount) {
            return new ArrayList<>();
        }
//        正常情况，返回这一页的数据
        List<Post> postList = postIPage.getRecords();
        List<PostDTO> postDTOList = new ArrayList<>();
        postList.forEach(post -> {
//          根据post构造postDTO
            PostDTO postDTO = new PostDTO(post);
//          为music属性赋值
            postDTO.setMusic(musicService.getMusicById(post.getMusicId()));
//          为user属性赋值
            postDTO.setUser(userService.getUserById(post.getUserId()));

            postDTOList.add(postDTO);
        });
        return postDTOList;
    }


    /**
     * @description: 新增post
     * @param: post
     * @return: 新增的记录数
     * @date: 2024/5/16 11:19
     */
    @Override
    public int insertPost(Post post) {
        return postMapper.insert(post);
    }
}
