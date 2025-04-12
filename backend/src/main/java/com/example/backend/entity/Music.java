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
* @date: 2024/5/13 14:28
*/
@Data
@TableName(value = "user_music")
@NoArgsConstructor
@AllArgsConstructor
public class Music {

    @TableId(value = "id", type = IdType.AUTO)
    private Integer id;

    @TableField(value = "title")
    private String title;

    @TableField(value = "artist")
    private String artist;

    @TableField(value = "value")
    private double value;

    @TableField(value = "url")
    private String url;

    @TableField(value = "user_id")
    private Integer userId;

    @TableField(value = "is_custom")
    private Boolean isCustom;
}
