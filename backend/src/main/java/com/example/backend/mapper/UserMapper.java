package com.example.backend.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.backend.entity.User;
import org.apache.ibatis.annotations.Mapper;

/**
* @description:
* @param:
* @return:
* @date: 2024/5/14 14:33
*/
@Mapper
public interface UserMapper extends BaseMapper<User> {

}
