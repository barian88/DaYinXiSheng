package com.example.backend.service.impl;

import com.example.backend.service.CosService;
import com.example.backend.utils.AjaxResult;
import com.example.backend.utils.CosManager;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import javax.annotation.Resource;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;


/**
 * @description:
 * @author: WYG
 * @time: 2020/4/18 15:46
 */
@Service
public class CosServiceImpl implements CosService {

    @Resource
    private CosManager cosManager;
    @Override
    public AjaxResult uploadFile(MultipartFile file, String keyPrefix) throws IOException {
        // 获取文件名
        String fileName = file.getOriginalFilename();
        // System.out.println("上传的文件名为：" + fileName);
        // 获取文件的后缀名
        String suffixName = fileName.substring(fileName.lastIndexOf("."));
        // System.out.println("上传的后缀名为：" + suffixName);

        String QCloudBaseUrl = "https://bucket-1305916869.cos.ap-beijing.myqcloud.com/";
        String key = keyPrefix + getRandomCharacterAndNumber(10) + suffixName;//生成随机文件名
        File localFile = transferToFile(file, key.replace(suffixName, ""), suffixName);
        Map<String,String> res = new HashMap<>();

        try{
            cosManager.putObject(key, localFile);
            res.put("fileKey", key);
            res.put("fileUrl",QCloudBaseUrl + key);
            return AjaxResult.success("文件上传成功！",res);
        }catch (Exception e){
            return AjaxResult.error("文件上传失败！");
        }
    }

    @Override
    public AjaxResult deleteFile(String fileKey) {

        try {
            cosManager.deleteObject(fileKey);
        } catch (Exception ex) {
            //如果遇到异常，说明删除失败
            return AjaxResult.error("文件删除失败！");
        }
        return AjaxResult.success("文件删除成功！");
    }

    /**
    * @description: 生成随机字符串
    * @param: 字符串长度
    * @return:
    * @date: 2024/5/15 23:23
    */
    private static String getRandomCharacterAndNumber(int length) {
        String val = "";
        Random random = new Random();
        for (int i = 0; i < length; i++) {
            String charOrNum = random.nextInt(2) % 2 == 0 ? "char" : "num"; // 输出字母还是数字

            if ("char".equalsIgnoreCase(charOrNum)) // 字符串
            {
                int choice = random.nextInt(2) % 2 == 0 ? 65 : 97; // 取得大写字母还是小写字母
                val += (char) (choice + random.nextInt(26));
                // int choice = 97; // 指定字符串为小写字母
                val += (char) (choice + random.nextInt(26));
            } else if ("num".equalsIgnoreCase(charOrNum)) // 数字
            {
                val += String.valueOf(random.nextInt(10));
            }
        }
        return val;
    }

    /**
     * 用缓冲区来实现这个转换, 即创建临时文件 使用 MultipartFile.transferTo()
     *
     * @param multipartFile
     * @return
     */
    private static File transferToFile(MultipartFile multipartFile, String prefix, String suffix) throws IOException {
        File file = File.createTempFile(prefix, suffix);
        multipartFile.transferTo(file);
        return file;
    }

}

