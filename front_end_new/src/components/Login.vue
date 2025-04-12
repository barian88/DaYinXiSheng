<template>
  <div class="login">
    <div class="logo">
      <img src="../assets/image/logo-white.png" />
      <div class="title">音画伴侣</div>
    </div>
    <div class="card beautiful-border">
      <div class="left">
          <div class="title">扫码登陆</div>
          <div class="qrcode">
            <!--      <vue-qr :logoSrc="imageUrl" :text="qrCodeUrl" :size="400"></vue-qr>-->
            <vue-qr :text="qrCodeUrl" :size="200"></vue-qr>
          </div>

          <div class="tip">
            <div class="word">使用</div>
            <i class="icon iconfont icon-weixin"></i>
            <div class="word">微信APP扫描二维码授权登陆</div>
          </div>
      </div>
      <div class="right">
          <div class="tip">
            <img src="../../src/assets/image/logo-grey.png" alt="" />
            <div class="title">音画伴侣</div>
            <div class="detail">申请使用以下权限</div>
          </div>
          <div class="content">
            <div class="circle"></div>
            <div class="word">
              <div class="title">微信公开信息</div>
              <div class="detail">头像、昵称</div>
            </div>
          </div>
    </div>


  </div>
  </div>
</template>

<script>
import axios from 'axios';
// 引入二维码插件
import vueQr from 'vue-qr';

export default {
  components: {vueQr},
  data() {
    return {
      qrCodeUrl: "",
      tempUserId: "",
      // 用于存储定时器
      timer: null
    };
  },
  methods: {
    // 请求二维码
    getQrCode(){
      axios.get('https://login.vicy.cn/8lXdSX7FSMykbl9nFDWESdc6zfouSAEz/wxLogin/tempUserId?secretKey=fb733c052b2742db88095ce359851827')
          .then(res => {
            this.qrCodeUrl = res.data.data.qrCodeReturnUrl;
            this.tempUserId = res.data.data.tempUserId;
            this.pollingLogin();
          })
    },
    // 轮询是否扫码成功
    pollingLogin() {
      this.timer = setInterval(() => {
        this.$axiosSpring({
          method: "GET",
          url: "login/polling",
          params: {
            tempUserId: this.tempUserId,
          },
        }).then(res => {
          console.log(res.data);
          // 登陆成功
          if (res.data.code === 200) {
            // 修改用户登录状态和信息
            this.global.setLoginStatus(true);
            this.global.setUser(res.data.data);
            // 清除定时器
            clearInterval(this.timer);
            // 设置cookie存储登录信息
            this.setCookie(JSON.stringify(res.data.data), 1);
            // 跳转到首页
            this.$router.push("/");
          }
        }).catch(err => {
          console.error(err);
          // 如果需要，在这里处理错误，例如显示错误信息
        });
      }, 1000);
    },
    //设置cookie
    setCookie(user, exdays) {
      let exdate = new Date();
      exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * exdays); // 保存的天数
      // 字符串拼接cookie
      window.document.cookie = "user=" + encodeURIComponent(user) + ";path=/;expires=" + exdate.toGMTString();
    }

  },
  mounted() {
    this.getQrCode();
  },
  beforeDestroy() {
    // 确保在组件销毁时清除定时器
    if (this.timer) {
      clearInterval(this.timer);
    }
  }
};
</script>



<style scoped lang="scss">
@import "../assets/style/base.scss";
@import "../assets/style/special.scss";

.login{
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}
.logo{
  display: flex;
  align-items: center;
  margin: 4% 0 2% 0;
  img{
    height: 7vh;
    width: 7vh;
  }
  .title{
    color: #fff;
    font-size: 2.4rem;
    font-family: 华文行楷;
    margin-left: 0.6vw;
  }

}
.card{
  height: 55%;
  width: 70%;
  padding: 2% 0;
  background-color: $background-color-selected;
  border-radius: $bigger-border-radius;
  display: flex;
  .left{
    height: 100%;
    width: 60%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 3vh;
    .title{
      font-size: 1.4rem;
      color: $default-font-color;
      font-weight: bold;
      padding-bottom: 3%;
      width: 200px;
      border-bottom: solid 3px $theme-color;
      display: flex;
      justify-content: center;
    }

    .qrcode{
      margin: 4% 0;
      img{
        border-radius: $bigger-border-radius;
      }
    }
    .tip{
      display: flex;
      align-items: center;
      i{
        font-size: 1.7rem;
        color: #28C445;
        margin: 0 2px;
      }
      .word{
        font-size: 1.2rem;
        color: $secondary-font-color;
      }
    }

  }
  .right{
    width: 40%;
    border-left: solid 2px #414141;
    font-size: 1.2rem;
    color: $secondary-font-color;
    padding-left: 6%;
    .tip {
      display: flex;
      width: 100%;
      margin-top: 3vh;
      img{
        width: 1.6rem;
        height: 1.6rem;
        margin-left: -6px;
      }
      .title{
        color: $default-font-color;
        font-weight: bold;
        padding: 0 2%;
      }
    }
    .content{
      display: flex;
      align-items: center;
      margin-top: 5%;
      .circle{
        width: 10px;
        height: 10px;
        background-color: $secondary-font-color;
        border-radius: 50%;
        margin-right: 10%;
      }
      .word{
        .title{
          color: $default-font-color;
        }
        .detail{
          font-size: 1rem;
        }
      }
    }
  }
}
</style>