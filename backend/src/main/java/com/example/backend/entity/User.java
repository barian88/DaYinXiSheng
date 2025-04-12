package com.example.backend.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
* @description: 
* @param: 
* @return: 
* @date: 2024/5/14 14:33
*/
@Data
@TableName(value = "user")
@NoArgsConstructor
@AllArgsConstructor
public class User {

    @TableId(value = "id", type = IdType.AUTO)
    private Integer id;
    
    @TableField(value = "user_id")
    private String userId;
    
    @TableField(value = "temp_user_id")
    private String tempUserId;
    
    @TableField(value = "avatar")
    private String avatar;
    
    @TableField(value = "nickname")
    private String nickname;
    
    @TableField(value = "ip_addr")
    private String ipAddr;
    
}
