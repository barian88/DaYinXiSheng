<template>
  <div class="music-base">
    <div class="database">
      <div class="table">
        <div class="header">
          <div class="upper">
              <div class="info">{{this.global.user.nickname}}的音乐库</div>
              <div class="right">
                <i class="icon iconfont icon-shuaxin" @click="getMusicPage"></i>
                <div class="search">
                  <el-input placeholder="请输入歌曲名称" v-model="searchMusicValue" @change="getMusicPageFirstWithCondition">
                    <i slot="prefix" class="el-input__icon el-icon-search"></i>
                  </el-input>
                </div>
              </div>
          </div>
          <div class="column">
            <div>名称</div>
            <div>歌手</div>
            <div>情绪值</div>
            <div>类型</div>
            <div>操作</div>
          </div>
        </div>
        <div class="body">
          <div class="music-item" v-for="(item,index) in musicList" :key="index">
            <div>{{item.title}}</div>
            <div>{{item.artist}}</div>
            <div>{{(item.value * 100).toString().slice(0,4) + '%'}}</div>
            <div>{{item.isCustom?'用户上传':'系统默认'}}</div>
            <div>
              <el-popconfirm popper-class="custom-popover" icon="false" @confirm="deleteMusic(item)"
                  title="确定删除这首音乐吗？"
              >
                <i slot="reference" class="icon iconfont icon-shanchu"></i>
              </el-popconfirm>

            </div>
          </div>
        </div>
        <div class="footer">
          <el-pagination
              @current-change="getMusicPage"
              layout="prev, pager, next"
              :current-page.sync="currentPage"
              :page-size.sync="pageSize"
              :total="totalRecords"
              :page-count="totalPages">
          </el-pagination>
        </div>
      </div>
    </div>
    <div class="divider"></div>
    <div class="upload-music">
      <div class="header"><span>上传本地音乐</span></div>
      <div class="upload">
        <el-upload
            class="upload-demo"
            drag
            :action="this.global.cosApi"
            :data="addPra"
            :on-success="handleSuccess"
            :before-upload="beforeUpload"
            :limit=1>
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将音乐文件拖到此处，或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">目前仅支持上传wav文件，命名格式为：歌曲名称---歌手.wav</div>
        </el-upload>
      </div>
      <div class="info">
        <div class="info-item">
          <div class="title">歌曲名称</div>
          <div class="info">{{musicInfo.title}}</div>
        </div>
        <div class="info-item">
          <div class="title">歌手</div>
          <div class="info">{{musicInfo.artist}}</div>
        </div>
        <div class="info-item">
          <div class="title">音乐情绪</div>
          <i class="icon iconfont icon-xiaolian"></i>
          <el-progress :text-inside="true" :stroke-width="30" :percentage=musicInfo.emoValue color="#00C1CD"></el-progress>
          <i class="icon iconfont icon-nanguo"></i>
        </div>
      </div>
      <div class="footer">
        <el-button :disabled="musicInfo.emoValue === 0" @click="submitMusicToDB">
          <i class="icon iconfont icon-queren"></i>
          <span>上传</span>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      // 音乐数据库表格相关
      musicList:[],
      totalPages: 0,
      totalRecords: 0,
      currentPage: 1,
      pageSize: 8,
      searchMusicValue: '',
      //音乐上传时的参数
      addPra: {
        keyPrefix: 'custom_music/'
      },
      // 音乐原始文件
      musicFile: null,
    //   分析得到的音乐信息
      musicInfo: {
        title: '',
        artist: '',
        emoValue: 0,
        url: ''
      },
      originalEmoValue: 0, //分析得到的原始emoValue
    };
  },
  methods: {
    // 获取音乐列表
    getMusicPage(){

      this.$axiosSpring({
        url: '/music/getMusicPage',
        method: 'get',
        params: {
          pageCount: this.currentPage,
          pageSize: this.pageSize,
          userId: this.global.user.id,
          titleOrArtist: this.searchMusicValue
        }
      }).then(res => {
        this.musicList = res.data.data.list;
        this.totalPages = res.data.data.totalPages;
        this.totalRecords = res.data.data.totalRecords;
      })
    },
    // 搜索音乐
    getMusicPageFirstWithCondition(){

      this.currentPage = 1;
      this.getMusicPage();
    },

    handleSuccess(response){
      this.getMusicEmo();
      this.musicInfo.url = response.data.fileUrl
      console.log(this.musicInfo)
    },
    beforeUpload(file){
      // 将文件保存
      this.musicFile = file
      let fileName = file.name
      this.musicInfo.title = fileName.split('---')[0].trim()
      this.musicInfo.artist = fileName.split('---')[1].replace('.wav', '').trim()
    },
    // 获得音乐情绪值
    async getMusicEmo(){
      let message = this.$message({
        message: '音乐情绪分析中...',
        type: 'info',
        duration: 0
      });
      let formData = new FormData();
      formData.append('file', this.musicFile)
      let res = await this.$axiosFlask({
        url: '/getMusicEmo',
        method: 'post',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      message.close()
      if(res.status){
        this.musicInfo.emoValue = (res.data.emo * 100).toString().slice(0,4)
        this.originalEmoValue = res.data.emo
      }else {
        this.$message({
          message: '音乐情绪分析失败',
          type: 'error'
        })
      }
    },
  //   将音乐添加到数据库
    async submitMusicToDB(){
      let music = {
        id: null,
        title: this.musicInfo.title,
        artist: this.musicInfo.artist,
        value: this.originalEmoValue,
        url: this.musicInfo.url,
        userId: this.global.user.id,
        isCustom: true
      }
      let res = await this.$axiosSpring({
        url: '/music/insertMusic',
        method: 'post',
        data: music
      })
      if(res.data.code === 200){
        this.$message({
          message: '音乐上传成功',
          type: 'success'
        })
      }
    },
  //   删除音乐
    async deleteMusic(music){
      // 删除cos中的音乐

      // 删除数据库中的音乐
      let response = await this.$axiosSpring({
        url: '/music/deleteMusic',
        method: 'delete',
        params: {
          id: music.id,
          userId: music.userId
        }
      })
      if(response.data.code === 200){
        this.$message({
          message: '删除成功',
          type: 'success'
        })
        // 在前端列表移除,重新请求数据
        this.getMusicPage()
      }

    },

  },
  mounted() {
    this.getMusicPage()
  },
};
</script>

<style scoped lang="scss">
@import "../../assets/style/base.scss";
.music-base{
  height: 90%;
  width: 100%;
  padding: 0 2%;
  display: flex;
}
.database{
  width: 60%;
  height: 100%;
  margin-top: 2%;
  font-size: 1.2rem;
  .table{
    height: 100%;
    display: flex;
    flex-direction: column;
    .header{
      .upper{
        padding: 0 24px 12px 12px;
        display: flex;
        justify-content: space-between;
        .info{
            color: $default-font-color;
            border-bottom: solid 2px $theme-color;
            font-weight: bold;
        }
        .right{
          display: flex;
          align-items: center;
          flex-basis: 35%;
          i{
            font-size: 1.4rem;
            color: $secondary-font-color;
            margin-right: 5%;
          }
          .icon-shuaxin:hover{
            color: $default-font-color;
            cursor: pointer;
          }
          .search{
            width: 100%;
            ::v-deep .el-input__inner{
              background-color: $background-color;
              border-radius: $default-border-radius $default-border-radius;
              color: $default-font-color;
              border: 2px solid $background-color-selected;
            }
          }
        }
      }
      .column{
        color: $default-font-color;
        display: flex;
        padding: 0 0 2% 0;
        div{
          padding: 0 12px;
        }
        div:nth-child(1){
          flex-basis: 40%;
        }
        div:nth-child(2){
          flex-basis: 30%;
        }
        div:nth-child(3), div:nth-child(4), div:nth-child(5){
          flex-basis: 10%;
          display: flex;
          justify-content: center;
        }
      }

    }
    .body{
      .music-item{
        display: flex;
        color: $secondary-font-color;
        padding: 2% 0;
        height: 5%;
        div{
          padding: 0 12px;
          display: flex;
          align-items: center;
        }
        div:nth-child(1){
          flex-basis: 40%;
        }
        div:nth-child(2){
          flex-basis: 30%;
        }
        div:nth-child(3), div:nth-child(4), div:nth-child(5){
          flex-basis: 10%;
          justify-content: center;
        }
        i{
          font-size: 1.5rem;
          color: $secondary-font-color;
          cursor: pointer;
        }
      }
      .music-item:nth-child(2n+1){
        background-color: $background-color-selected;
      }
      .music-item:hover{
        background-color: #575757FF;
      }
    }
    .footer{
      margin-top: auto;
      display: flex;
      justify-content: center;
      ::v-deep .el-pagination{
        color: $secondary-font-color;
        max-width: fit-content;
        button:disabled{
          background-color: $background-color ;
          color: $secondary-font-color;
        }
        button{
          background-color: $background-color ;
          color: $secondary-font-color;
        }

        li{
          background-color: $background-color;
        }
        li:hover, .active{
          color: $theme-color;
        }
      }
    }
  }
}
.divider{
  width: 2px;
  height: 95vh;
  background-color: $border-color;
}
.upload-music{
  width: 38%;
  height: 100%;
  margin-top: 2%;
  .header{
    width: 96%;
    margin: auto;
    padding: 0 0 12px 0;
    display: flex;
    justify-content: center;
    span{
      color: $default-font-color;
      font-weight: bold;
      font-size: 1.2rem;
    }
  }
  .upload{
    width: 96%;
    margin: 0 2%;
    padding: 0 0 4% 0;
    display: flex;
    justify-content: center;
    border-bottom: 2px solid $background-color-selected;
    .upload-demo{
      width: 360px;
    }
    .el-upload__tip{
      color: $secondary-font-color;
    }
    ::v-deep .el-upload-dragger{
      background-color: $background-color-selected;
    }
    ::v-deep .el-icon-upload, .el-upload__text{
      color: $secondary-font-color;
    }

    ::v-deep .el-upload-list__item-name{
      color: $secondary-font-color;
      i{
        color: $secondary-font-color;
      }
    }
    ::v-deep .el-upload-list__item:hover{
      background-color: $background-color;
      color: #7a00ff;
    }
  }
  .info{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    .info-item{
      width: 80%;
      display: flex;
      align-items: center;
      color: $default-font-color;
      font-size: 1.2rem;
      margin: 5% 0;
      .title{
        width: 20%;
      }
      .info{
        width: fit-content;
        font-weight: bold;
      }
      .el-progress{
        width: 240px;
        margin: 0 6px;
      }
      i{
        font-size: 1.6rem;
      }
    }
  }
  .footer{
    display: flex;
    margin-top: 8%;
    justify-content: center;
    .el-button{
      width: 80%;
      background-color: $theme-color;
      color: $default-font-color;
      border: 0;
      border-radius: $default-border-radius;
      .icon{
        font-size: 1.2rem;
        vertical-align: middle;
        margin-right: 5%;
      }
      span{
        vertical-align: middle;
      }
    }
  }
}

</style>

<style lang="scss">
@import "../../assets/style/base.scss";

.custom-popover{
  color: $secondary-font-color;
  background: $background-color-selected;
  border-color: $border-color;
  .el-button--text{
    color: $theme-color;
  }
  .el-button--primary{
    background: $theme-color;
  }

}
</style>