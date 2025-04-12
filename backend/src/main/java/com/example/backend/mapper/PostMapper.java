package com.example.backend.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.backend.entity.Post;
import org.apache.ibatis.annotations.Mapper;

/**
 * @description:
 * @date: 2024/5/13 14:33
 */
@Mapper
public interface PostMapper extends BaseMapper<Post> {
}
