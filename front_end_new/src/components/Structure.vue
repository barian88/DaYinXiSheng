<template>
  <div class="container">
      <div class="headBar">
        <div class="logo">
          <img src="../assets/image/logo-grey.png" alt="" />
          <input type="text" placeholder="欢迎使用音画伴侣配乐平台！" />
        </div>
      </div>
      <div class="leftBar">
        <div class="up">
          <div><div class="logo">
              <img :src="this.global.user.avatar" :key="imgKey" alt="" />
            </div>
          </div>
          <div>
            <div class="menu-item" @click="route('/')" >
              <i class="icon iconfont icon-remen"></i>
              <span class="words">主页热门</span>
            </div>
          </div>
          <div>
            <div class="menu-item" @click="route('/picture')">
              <i class="icon iconfont icon-tupian"></i>
              <span class="words">单图配乐</span>
            </div>
          </div>
          <div>
            <div class="menu-item"  @click="route('/video')">
              <i class="icon iconfont icon-shipin"></i>
              <span class="words">视频配乐</span>
            </div>
          </div>
          <div>
            <div class="menu-item" @click="route('/album')">
              <i class="icon iconfont icon-album"></i>
              <span class="words">多图生成</span>
            </div>
          </div>
          <div>
            <div class="menu-item" @click="route('/musicBase')">
              <i class="icon iconfont icon-yinyueshangdian"></i>
              <span class="words">音乐列表</span>
            </div>
          </div>
          <div>
            <div class="menu-item" @click="route('/moment')">
              <i class="icon iconfont icon-faxian"></i>
              <span class="words">发现</span>
            </div>
          </div>
        </div>
        <div class="middle"></div>
        <div class="down">
          <div>
            <div class="menu-item" @click="route('/home')">
              <i class="icon iconfont icon-zhuye"></i>
              <span class="words">我的</span>
            </div>
          </div>
        </div>
      </div>
      <div class="content">
        <router-view></router-view>
      </div>
    <div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import ElementUI from "element-ui";
Vue.use(ElementUI);
// 引入audio-better组件
import VueAudio from 'vue-audio-better'
Vue.use(VueAudio);

import util from "@/util";

export default {
  components: {
  },
  data() {
    return {
      // 用于刷新用户头像
      imgKey: 0,
    };
  },
  methods: {
    // 路由跳转
    route(path) {
      this.$router.push(path);
    },
  //   判断登陆状态
    isLogin(){
      // 首先尝试从cookie中获取用户信息
      let user = util.getCookie('user');
      // console.log('user: ' +  user)
      // 转为json对象
      if(user){
        user = JSON.parse(user);
        // 如果cookie中有用户信息，直接设置用户信息和登陆状态
        if(user){
          this.global.setUser(user);
          this.global.setLoginStatus(true);
          // 刷新用户头像
          this.imgKey = 1;
        }
      }

      // console.log(user)
      if(!this.global.loginStatus)
        this.$router.push('/login')
    }
  },
  mounted() {
    this.isLogin();
  }

};
</script>

<style lang="scss" scoped>

//引入全局样式
@import "../assets/style/base.scss";

.content {
  position: absolute;
  width: 96.5%;
  height: 95%;
  top: 5%;
  left: 3.5%;
}

.leftBar {
  background-color: $background-color;
  border-right: $border-width solid $border-color ;
  position: absolute;
  width: 3.5%;
  height: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
  transition: all 300ms ease-in-out;
  z-index: 1;
}

.leftBar:hover {
  width: 5%;
}
.leftBar .up {
  flex: 12rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
}
.leftBar .up .logo img {
  margin-top: 1rem;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 1.5rem;
}
.leftBar .menu-item, {
  border: 0;
  height: 3.7rem;
  width: 4rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  transition: all 200ms ease-in-out;
  font-size: 1rem;
  font-weight: 100;
  color: $default-font-color;
  text-align: center;
  font-family: YouYuan;
}

.leftBar .menu-item i {
  font-size: 1.6rem;
  color: #666666;
}
/*这一部分实现悬停时图片和文字切换  */
.leftBar .menu-item .words {
  display: none;
}
.leftBar .menu-item:hover .words {
  display: inline-block;
  cursor: pointer;
}
.leftBar .menu-item:hover i  {
  display: none;
}

.leftBar .middle {
  flex: 14.5rem;
  -webkit-app-region: drag;
}
.leftBar .down {
  flex: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
}

.headBar {
  border-bottom: $border-width solid $border-color ;
  position: absolute;
  width: 100%;
  height: 5%;
  overflow: hidden;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  z-index: 1;
  background-color: $background-color;
}
.headBar .logo {
  width: 18rem;
  height: 1.5rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  border-radius: 1rem;
  transition: all 200ms ease-in-out;
}
.headBar .logo:hover {
  width: 22rem;
  background: $border-color;
}
.headBar .logo:hover input {
  width: 17.5rem;
}
.headBar .logo img {
  margin-top: 0.2rem;
  width: 1rem;
  height: 1rem;
}
.headBar .logo input {
  width: 15.5rem;
  background-color: #0000;
  border: 0;
  outline: medium;
  color: $default-font-color;
  font-size: 1rem;
  text-align: center;
  transition: all 200ms ease-in-out;
}
.headBar .logo input::-webkit-input-placeholder {
  color: $default-font-color;
  text-align: center;
}
</style>