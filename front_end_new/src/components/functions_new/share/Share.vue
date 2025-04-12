<template>
  <div class="share-dialog">
    <el-dialog
        :visible.sync="dialogVisibility"
        width="60%">
      <div class="post">
        <div class="left">
          <i v-if="post.type === 'video'" class="icon iconfont icon-bofang"></i>
          <i v-if="post.type === 'album'" class="icon iconfont icon-album"></i>
          <img :src="post.coverUrl"  alt="" />
        </div>
        <div class="right">
          <div class="right-up">
            <div class="user-info">
              <img :src="(user.avatar)" alt=""/>
              <div class="username">{{user.nickname}}</div>
              <div class="date">{{date}}</div>
            </div>
            <div class="title">
              <el-input placeholder="请输入标题" v-model="title" maxlength="20" show-word-limit></el-input>
            </div>
            <div class="divider">
              <div class="divider-inner"></div>
            </div>
            <div class="detail">
              <el-input placeholder="请输入内容" type="textarea" v-model="detail" maxlength="255" show-word-limit></el-input>
            </div>
            <div class="music">
              <div class="music-info">
                <i class="icon iconfont icon-yinyue"></i>
                <div class="music-title">{{post['music'].title}}</div>
              </div>
            </div>
          </div>
          <div class="right-down">
            <div class="share-button">
              <el-button @click="confirmShare">
                <i class="icon iconfont icon-queren"></i>
                <span>确认</span>
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>

  </div>
</template>


<script>
import util from "../../../../src/util.js";
import { Loading } from 'element-ui';

export default {
  name: "Share",
  components: {},
  data() {
    return{
      dialogVisibility: false,
      post: {
        coverUrl: require('@/assets/image/2.jpg'),
        music: {
          title: '',
        },
      },
      user: {
        avatar: '',
        nickname: ''
      },
      date: '',
      title: '',
      detail: ''
    }
  },
  methods: {
    initUser(){
      this.user = this.global.user
    },
    // 初始化日期
    initDate(){
      this.date = util.getNowFormatDate();
    },
  //   更改dialog的显示状态
    showShareDialog(post){
      this.dialogVisibility = true;
      // 初始化内容
      this.post = post;
      console.log(post)
    },
  //   确认分享，将数据存储到数据库
  //   对于图片，url和coverUrl不需要处理
  //   对于视频，blob和coverUrl都需要上传到cos，再存储
  //             blob对象，coverUrl是dataURL对象
  //   对于专辑，blob需要上传，coverUrl不需要
  //             blob对象
    async confirmShare() {
      // 展示loading
      let loadingInstance = Loading.service({
        lock: true,
        text: '分享中...',
        background: 'rgba(0, 0, 0, 0.7)'
      });

      let cosUrl = await this.uploadFileAndCoverToCos();
      // 构造一个postDTO对象
      const postDTO = {
        id: this.post.id,
        userId: this.global.user.id,
        musicId: this.post.music.id,
        title: this.title,
        detail: this.detail,
        type: this.post.type,
        url: cosUrl.fileUrl,
        date: this.date,
        coverUrl: cosUrl.coverUrl
      }
    //   数据上传到数据库
      const response = await this.$axiosSpring({
        method: 'post',
        url: '/post/insertPost',
        data: postDTO
      });
      if (response.data.code === 200) {
        this.$message({
          message: '分享成功',
          type: 'success'
        });
        this.dialogVisibility = false;
      } else {
        this.$message({
          message: '分享失败',
          type: 'error'
        });
      }
      // 关闭loading
      this.$nextTick(() => { // 以服务的方式调用的 Loading 需要异步关闭
        loadingInstance.close();
      });
    },

    async uploadFileAndCoverToCos() {
      let fileUrl = '';
      let coverUrl = '';

      // 对于图片类型
      if (this.post.type === 'picture') {
        fileUrl = this.post.url;
        coverUrl = this.post.url;
      }

      // 对于视频类型
      if (this.post.type === 'video') {
        // 将视频资源blob对象转换为file对象并上传
        const videoFile = util.blobToFile(this.post.blob, 'video.mp4', 'video/mp4');
        // 创建 FormData 对象
        const videoFormData = new FormData();
        videoFormData.append('file', videoFile);
        videoFormData.append('keyPrefix', 'test/video/');

        const videoResponse = await this.$axiosSpring({
          method: 'post',
          url: '/cos/upload',
          data: videoFormData,
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        fileUrl = videoResponse.data.data.fileUrl;

        // 将封面资源转换为file对象并上传
        const coverFile = util.dataURLToFile(this.post.coverUrl, 'cover.png');
        // 创建 FormData 对象
        const coverFormData = new FormData();
        coverFormData.append('file', coverFile);
        coverFormData.append('keyPrefix', 'test/cover/');

        const coverResponse = await this.$axiosSpring({
          method: 'post',
          url: '/cos/upload',
          data: coverFormData,
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        coverUrl = coverResponse.data.data.fileUrl;
      }

      // 对于多图类型
      if (this.post.type === 'album') {
        // 将视频资源blob对象转换为file对象并上传
        const videoFile = util.blobToFile(this.post.blob, 'video.mp4', 'video/mp4');
        // 创建 FormData 对象
        const videoFormData = new FormData();
        videoFormData.append('file', videoFile);
        videoFormData.append('keyPrefix', 'test/video/');

        const videoResponse = await this.$axiosSpring({
          method: 'post',
          url: '/cos/upload',
          data: videoFormData,
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        fileUrl = videoResponse.data.data.fileUrl;
        coverUrl = this.post.coverUrl;
      }

      return {
        fileUrl: fileUrl,
        coverUrl: coverUrl
      };
    }



  },
  mounted() {
    this.initUser();
    this.initDate();
  }
}
</script>


<style scoped lang="scss">
@import "src/assets/style/base.scss";

::v-deep .el-dialog{
  background-color: $background-color;
  border-radius: $default-border-radius;
  margin-top: 10vh !important;
}
::v-deep .el-dialog__header{
  padding: 0;
}
::v-deep .el-dialog__body{
  padding: 0;
  height: 70vh;
}
.post{
  width: 100%;
  height: 100%;
  display: flex;
}
.left{
  width: 60%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  img{
    max-height: 80%;
    width: 100%;
    object-fit: contain;
    border-radius: $default-border-radius;
  }
  .icon{
    color: $default-font-color;
    background-color: rgba(192, 192, 192, 0.5);
    font-size: 2vw;
    height: fit-content;
    width: fit-content;
    border-radius: 50%;
    position: absolute;
    top: 10vh;
    right: 28vw;
  }
}
.right{
  background-color: $background-color-selected;
  border-bottom-right-radius: $default-border-radius;
  border-top-right-radius: $default-border-radius;
  width: 40%;
  padding: 3% 20px;
  display: flex;
  flex-direction: column;
  .right-up{
    .user-info{
      display: flex;
      align-items: center;
      justify-content: flex-start;
      img{
        width: 3rem;
        height: 3rem;
        border-radius: 50%;
      }
      .username{
        color: $secondary-font-color;
        margin-left: 15px;
      }
      .date{
        color: $secondary-font-color;
        margin: 0 15px 0 auto;
      }
    }

    .title{
      margin: 7% 0 0 0;
      color: $default-font-color;
      ::v-deep .el-input__inner{
        background-color: $background-color;
        border-radius: $default-border-radius $default-border-radius 0 0;
        color: $default-font-color;
        border: 0;
        font-size: 1.4rem;
      }
      ::v-deep .el-input__count-inner{
        background-color: $background-color;
      }
    }
    .divider{
      width: 100%;
      height: 2px;
      background-color: $background-color;
      .divider-inner{
        width: calc(100% - 30px);
        height: 100%;
        margin: 0 15px;
        background-color: $background-color-selected;
      }
    }
    .detail{
      color: $default-font-color;
      ::v-deep .el-textarea__inner{
        background-color: $background-color;
        border-radius: 0 0 $default-border-radius $default-border-radius;
        color: $default-font-color;
        border: 0;
        font-size: 1.2rem;
        height: 25vh;
      }
      ::v-deep .el-input__count{
        background-color: $background-color;
      }
    }
    .music{
      margin-top: 5%;
      padding: 4% 0 4% 4%;
      background-color: $background-color;
      border-radius: $default-border-radius;

      .music-info{
        display: flex;
        align-items: flex-start;
        .music-title{
          color: $secondary-font-color;
          font-size: 1.2rem;
        }
        .icon{
          font-size: 1.5rem;
          color: $theme-color;
          margin-right: 2%;
        }
      }
    }

  }
  .right-down{
    margin-top: auto;
    .share-button{

      .el-button{
        width: 100%;
        background-color: $theme-color;
        border: 0;
        border-radius: $default-border-radius;
        color: $default-font-color;
      }
      .icon{
        font-size: 1.2rem;
        margin-right: 2%;
        vertical-align: middle;
      }
      span{
        vertical-align: middle;
      }
    }
  }
}
</style>