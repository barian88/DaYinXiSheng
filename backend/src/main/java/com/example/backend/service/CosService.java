package com.example.backend.service;

import com.example.backend.utils.AjaxResult;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;


public interface CosService {
    AjaxResult uploadFile(MultipartFile file, String keyPrefix) throws IOException;


    AjaxResult deleteFile(String fileKey);
}

