package com.example.backend.dto;

import com.example.backend.entity.Music;
import com.example.backend.entity.Post;
import com.example.backend.entity.User;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PostDTO {


//        Post的属性
        private Integer id;

        private Integer userId;

        private Integer musicId;

        private String title;

        private String detail;

        private String type;

        private String url;

        private String coverUrl;

        private String date;

        private Music music;

        private User user;

//        根据Post构造PostDTO
        public PostDTO(Post post) {
            this.id = post.getId();
            this.userId = post.getUserId();
            this.musicId = post.getMusicId();
            this.title = post.getTitle();
            this.detail = post.getDetail();
            this.type = post.getType();
            this.url = post.getUrl();
            this.coverUrl = post.getCoverUrl();
            this.date = post.getDate().toString();
            this.music = null;
            this.user = null;
        }
}
