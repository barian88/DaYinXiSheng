package com.example.backend.controller;

import com.alibaba.fastjson.JSONObject;
import com.example.backend.entity.User;
import com.example.backend.service.UserService;
import com.example.backend.utils.AjaxResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@RequestMapping("/login")
@RestController
public class LoginController {

    @Autowired
    UserService userService;
    /**
    * @description: 码上登录的回调函数
    * @param: 参数为user的属性
    * @return: 将登陆结果返回给码上登录
    * @date: 2024/5/14 14:26
    */
    @PostMapping(value = "/callback")
    public JSONObject backUserScanedInfo(
            @RequestParam(value = "userId",required = false)  String userId,
            @RequestParam(value = "tempUserId",required = false) String tempUserId,
            @RequestParam(value = "nickname",required = false) String nickname,
            @RequestParam(value = "avatar",required = false) String avatar,
            @RequestParam(value = "ipAddr",required = false) String ipAddr,
            HttpServletResponse httpServletResponse) throws IOException {
        System.out.println("用户信息============\r\n"+ "【userId】"+userId+ " 【tempUserId】 "+tempUserId+ " 【nickname】 "+nickname+ " 【headimgurl】 "+avatar+ " 【ipAddr】"+ipAddr);

        // 写自己的逻辑 保存用户或更新用户信息到数据库
        User user = new User();
        user.setUserId(userId);
        user.setTempUserId(tempUserId);
        user.setAvatar(avatar);
        user.setNickname(nickname);
        user.setIpAddr(ipAddr);
        userService.insertOrUpdateUser(user);

        // 返回状态码
        JSONObject jsonObject = new JSONObject();
        if (userId != null){
            jsonObject.put("errcode",0);
            jsonObject.put("message","success");
        }else {
            jsonObject.put("errcode",1);
            jsonObject.put("message","error");
        }
        return jsonObject;
    }

    @GetMapping("/polling")
    public AjaxResult checkLogin( @RequestParam(value = "tempUserId")  String tempUserId){
        if (tempUserId.equals(""))
            return AjaxResult.error("tempUserId不能为空");
        User user = userService.getUserByTempUserId(tempUserId);
        if (user == null)
            return AjaxResult.error("用户信息不存在");
        else
            return AjaxResult.success("OK",user);
    }
}
