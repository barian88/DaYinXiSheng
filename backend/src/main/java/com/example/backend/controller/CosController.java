package com.example.backend.controller;

import com.example.backend.service.CosService;
import com.example.backend.utils.AjaxResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

/**
 * @description:
 * @author:
 * @time: 2024/4/18 15:54
 */

@RestController
@RequestMapping("/cos")
public class CosController {
    @Autowired
    private CosService cosService;

    /**
    * @description: 上传文件,对应elementUI的上传组件
    * @param: MultipartFile文件，keyPrefix文件的路径前缀，默认为temp/
    * @return: AjaxResult
    * @date: 2024/5/15 23:09
    */
    @PostMapping("/upload")
    @CrossOrigin
    public AjaxResult uploadFile(@RequestParam("file") MultipartFile multipartFile,
                                 @RequestParam(value = "keyPrefix", defaultValue = "temp/", required = false) String keyPrefix) throws IOException {
        return cosService.uploadFile(multipartFile, keyPrefix);
    }


    /**
    * @description: 删除文件
    * @param: fileKey
    * @return:
    * @date: 2024/5/15 23:10
    */
    @PostMapping("/delete")
    public AjaxResult deleteFile(String fileKey){
        return cosService.deleteFile(fileKey);
    }


}
