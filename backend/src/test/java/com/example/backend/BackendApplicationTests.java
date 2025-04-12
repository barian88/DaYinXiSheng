package com.example.backend;

import com.example.backend.entity.Music;
import com.example.backend.service.MusicService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@SpringBootTest
class BackendApplicationTests {

    @Autowired
    MusicService musicService;

    @Test
    void contextLoads() {
    }


}
