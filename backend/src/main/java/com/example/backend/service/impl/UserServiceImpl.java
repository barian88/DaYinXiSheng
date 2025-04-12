package com.example.backend.service.impl;


import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.backend.entity.User;
import com.example.backend.mapper.UserMapper;
import com.example.backend.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
* @description:
* @param:
* @return:
* @date: 2024/5/14 14:36
*/
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    @Autowired
    UserMapper userMapper;

    /**
     * @description: 新增用户记录，根据userId判断唯一性，如果已经存在该用户只更新用户信息
     * @param: 用户对象
     * @return: 插入或者修改的结果
     * @date: 2024/5/14 14:37
     */
    @Override
    @Transactional
    public boolean insertOrUpdateUser(User user) {

        QueryWrapper<User> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("user_id", user.getUserId());

        User existingUser = userMapper.selectOne(queryWrapper);

        if (existingUser != null){
            // 用户存在，更新用户信息
            user.setId(existingUser.getId()); // 如果主键id是自增的，需要保留原有的id
            return userMapper.updateById(user) > 0;
        }
        // 用户不存在，新增用户
        return userMapper.insert(user) > 0;

    }

    /**
     * @description: 根据tempUserId获取用户信息，用于轮询实现微信扫码登录
     * @param: tempUserId
     * @return: user
     * @date: 2024/5/14 15:09
     */
    @Override
    public User getUserByTempUserId(String tempUserId) {
        QueryWrapper<User> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("temp_user_id", tempUserId);
        return userMapper.selectOne(queryWrapper);
    }

    /**
     * @description: 根据用户的Id获取用户信息
     * @param: 用户Id,不是微信登陆的userId
     * @return: user
     * @date: 2024/5/14 17:31
     */
    @Override
    public User getUserById(int id) {
        return userMapper.selectById(id);
    }
}
