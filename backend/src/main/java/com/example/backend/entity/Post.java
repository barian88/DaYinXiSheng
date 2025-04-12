package com.example.backend.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

/**
* @description:
* @date: 2024/5/13 16:13
*/
@Data
@TableName(value = "post")
@NoArgsConstructor
@AllArgsConstructor
public class Post {

    @TableId(value = "id", type = IdType.AUTO)
    private Integer id;

    @TableField(value = "user_id")
    private Integer userId;

    @TableField(value = "music_id")
    private Integer musicId;

    @TableField(value = "title")
    private String title;

    @TableField(value = "detail")
    private String detail;

    @TableField(value = "type")
    private String type;

    @TableField(value = "url")
    private String url;

    @TableField(value = "cover_url")
    private String coverUrl;

    @TableField(value = "date")
    private LocalDate date;
}
