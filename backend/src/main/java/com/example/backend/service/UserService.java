package com.example.backend.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.example.backend.entity.User;

/**
* @description:
* @param:
* @return:
* @date: 2024/5/14 14:34
*/
public interface UserService extends IService<User> {

    /**
    * @description: 新增用户记录，根据userId判断唯一性，如果已经存在该用户只更新用户信息
    * @param: 用户对象
    * @return: 插入或者修改的结果
    * @date: 2024/5/14 14:37
    */
    boolean insertOrUpdateUser(User user);

    /**
    * @description: 根据tempUserId获取用户信息，用于轮询实现微信扫码登录
    * @param: tempUserId
    * @return: user
    * @date: 2024/5/14 15:09
    */
    User getUserByTempUserId(String tempUserId);

    /**
    * @description: 根据用户的Id获取用户信息
    * @param: 用户Id,不是微信登陆的userId
    * @return: user
    * @date: 2024/5/14 17:31
    */
    User getUserById(int id);
}
