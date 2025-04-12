<template>
    <div class="moment">
      <div class="container" id="con" @scroll="handleScroll">
        <div class="item" v-for="(item, index) in postList" :key="index" @click="previewPost(item)">
          <img :src="(item.coverUrl)" alt=""/>
          <i v-if="item.type === 'video'" class="icon iconfont icon-bofang"></i>
          <i v-if="item.type === 'album'" class="icon iconfont icon-album"></i>
          <div class="title">{{item.title}}</div>
          <div class="user-info">
            <img :src="(item['user'].avatar)" alt=""/>
            <div class="username">{{item['user'].nickname}}</div>
          </div>
        </div>
        <div :class="{'loading': true, 'initial': postList.length === 0, 'later': postList.length !== 0}" v-if="isLoading">
          <i class="el-icon-loading"></i>
        </div>
      </div>
      <div class="dialog">
        <el-dialog
            :visible.sync="dialogVisible"
            width="60%">
         <div class="selected-post">
           <div class="left">
             <img v-if="selectedPost.type === 'picture'" :src="selectedPost.coverUrl"  alt="" />
             <div v-if="playerOptions.sources[0].src.length !== 0" class="my-video-player">
               <videoPlayer
                   class="video-player vjs-custom-skin"
                   ref="videoPlayer"
                   :playsinline="true"
                   :options="playerOptions"
               >
               </videoPlayer>
             </div>
           </div>
           <div class="right">
             <div class="right-up">
               <div class="user-info">
                 <img :src="(selectedPost['user'].avatar)" alt=""/>
                 <div class="username">{{selectedPost['user'].nickname}}</div>
                 <div class="date">{{selectedPost.date}}</div>
               </div>
               <div class="title">{{selectedPost.title}}</div>
               <div class="detail">{{selectedPost.detail}}</div>
             </div>
             <div class="right-down">
               <div class="music">
                  <div class="music-info">
                    <i class="icon iconfont icon-yinyue"></i>
                    <div class="music-title">{{selectedPost['music'].title}}</div>
                  </div>
                 <div class="audio" v-if="selectedPost.type === 'picture'">
                   <mini-audio class="audio-player" :audio-source="selectedPost.music.url" ref="audio">
                     <!--                    audio-source="https://bucket-1305916869.cos.ap-beijing.myqcloud.com/music_recommendation/06BA9LHRT0.wav"-->
                   </mini-audio>
                 </div>

               </div>
             </div>
           </div>
         </div>
        </el-dialog>
      </div>
    </div>
</template>

<script >
import Emotion from "@/components/functions_new/graph/emotion_like.vue";
//引入视频播放组件
import "video.js/dist/video-js.css";
import { videoPlayer } from "vue-video-player";

export default {
  components: {
    videoPlayer
  },
  data() {
    return {
      dialogVisible: false,
      selectedPost: {
        music: {
          title: ''
        },
        user: {
          nickname: '',
          avatar: ''
        }
      },
      postList: [],
      playerOptions: {
        autoplay: false, //如果true,浏览器准备好时开始回放。
        muted: false, // 是否静音。
        loop: false, // 是否循环播放。
        preload: "false", // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        language: "zh-CN",
        aspectRatio: "16:9", // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
        fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
        sources: [
          {
            type: "video/mp4", //mp4格式视频,若为m3u8格式，type需设置为 application/x-mpegURL
            src: "", //url地址
          },
        ],
        notSupportedMessage: "此视频暂无法播放，请稍后再试", //允许覆盖Video.js无法播放媒体源时显示的默认信息。
        controlBar: {
          timeDivider: true,
          durationDisplay: true,
          remainingTimeDisplay: false,
          fullscreenToggle: true, //是否显示全屏按钮
        },
      },
      // 设置分页查询参数
      postPageCount: 1,
      postPageSize: 5,
      // 加载状态
      isLoading: true
    }
  },
  methods: {
    // 瀑布流布局初始化
    waterFall() {
      // 1. 设置container盒子的宽度
      //      注意：浏览器的可视区域的宽度 / 一个item元素的宽度 = 一行的排列的元素的个数
      let container = document.getElementById("con")
      let item = document.getElementsByClassName("item")
      //获取元素的宽度(含border，padding)
      let width = item[0].offsetWidth
      //计算出浏览器窗口的宽度，这里应该是container盒子的宽度
      // let clientWidth = container.offsetWidth;
      //计算出应该放几列（向下取整）
      // let columnCount = Math.floor(clientWidth / width)
      // 固定放3列
      let columnCount = 3

      // 2.设置每一个item元素的排列位置
      //  第一行整体的top值都是0 后面的依次找上一行高度最小的容器，在它下面进行排列
      let hrr = []
      // 设置左右和上线间距
      let marginLeft = 30;
      let marginTop = 30;
      for (let i = 0; i < item.length; i++) {
        //定位第一行的图片
        if (i < columnCount) {
          item[i].style.top = 0;
          item[i].style.left = i * (width + marginLeft) + "px"
          hrr.push(item[i].offsetHeight)
        //   显示定位完成的item
          item[i].style.visibility = "visible"
        } else {
          //第一行之后的
          //选择总高度最小的列
          let min = Math.min(...hrr)
          let index = hrr.indexOf(min)
          //将每个元素定位到当前总高度最小的列下
          item[i].style.top = (min + marginTop) + "px"
          item[i].style.left = index * (width + marginLeft) + "px"
          //当前定位的元素加入该列
          hrr[index] += item[i].offsetHeight + marginTop
          //   显示定位完成的item
          item[i].style.visibility = "visible"
        }
      }
      //  // 计算并设置container的宽度
      // container.style.width = columnCount * (width + 20) + "px"

    },
    // 选择预览的帖子
    previewPost(item){
      // 清除上次dialog的记录
      this.playerOptions.sources[0].src = '';
      // 设置新的dialog item
      this.selectedPost = item;
      // 如果是视频，初始化播放器资源
      if(item.type === 'video' || item.type === 'album'){
        this.playerOptions.sources[0].src = item.url;
      }
      // 显示dialog
      this.dialogVisible = true;
    },
    // 请求帖子列表
    getPostList(){
      this.isLoading = true
        this.$axiosSpring({
        method: 'get',
        url: 'post/getPostPage',
        params: {
          pageCount: this.postPageCount,
          pageSize: this.postPageSize
        }
      }).then(res => {
        let data = res.data.data;
        if (data.length === 0){
          this.$message({
            message: '没有更多数据了！',
          });
          // 关闭加载
          this.isLoading = false
          return;
        }
        //   关闭加载
        this.isLoading = false
        // 拼接新数据
        this.postPageCount++;
        this.postList = this.postList.concat(data);
        setTimeout(() => {
          this.waterFall();
        }, 500)
      })
    },
    // 触底加载更多
    handleScroll() {
      const container = document.getElementById("con");
      if (container.scrollTop + container.clientHeight + 0.5 >= container.scrollHeight) {
        this.getPostList();
      }
    }
  },
  mounted() {
    // 页面加载时
    // window.onload = () => {
    //   this.waterFall();
    // };
    this.getPostList();
    // 窗口大小变化时
    window.onresize = () => {
      this.waterFall();
    };
  },
  // 路由变化，也就是从其他页面跳转时
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.$nextTick(() => {
        vm.waterFall();
      });
    });
  }


}


</script>
<style scoped lang="scss">
@import "../../assets/style/base.scss";
.moment{
  height: 100%;
  width: 100%;
}
.container{
  position: relative;
  height: 98%;
  width: calc(29vw * 3 + 60px);
  margin: 0 auto;
  overflow: scroll;
  top: 2%;
}

.item:hover{
  cursor: pointer;
}
.item{
  width: 29vw;
  height: auto;
  position: absolute;
  visibility: hidden;
  img{
    width: 100%;
    border-radius: $default-border-radius;
    transition: all 0.3s ease-in-out;
  }
  img:hover{
    scale: (1.05);
    filter: brightness(1.1);
  }
  i{
    color: $default-font-color;
    background-color: rgba(192, 192, 192, 0.5);
    font-size: 2vw;
    position: absolute;
    top: 1.5vw;
    right: 1.5vw;
    border-radius: 50%;
  }
  .title{
    color: $default-font-color;
    font-size: 1.3rem;
    font-weight: 900;
    padding: 14px 6px;
  }
  .user-info{
    display: flex;
    align-items: center;
    justify-content: flex-start;
    img{
      width: 2rem;
      height: 2rem;
      border-radius: 50%;
      padding: 0 6px;
    }
    .username{
      color: $secondary-font-color;
    }
}


}
.dialog{
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
  .selected-post{
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
    .my-video-player{
      max-height: 80%;
      width: 100%;
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
        margin: 5% 0;
        color: $default-font-color;
        font-size: 1.8rem;
        font-weight: 900;
      }
      .detail{
        color: $default-font-color;
        font-size: 1.6rem;
      }
    }
    .right-down{
      margin-top: auto;
      .music{
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
        .audio{
          width: 100%;
          margin: 4% 0 0 0;
          .audio-player{
            width: 90%;
            margin: 0;
            padding: 0;
            background-color: $background-color;
            background-image: none;
            box-shadow: none;
          }
          ::v-deep .vueAudioBetter[data-v-3a8dc9f9]{
            height: auto;
            line-height: normal;
          }
          ::v-deep .vueAudioBetter .operate .icon-stopcircle-fill{
            display: none;
          }
          ::v-deep .vueAudioBetter span[data-v-3a8dc9f9] {
            color: #ffffff;
            font-size: 1.5rem;
          }
          ::v-deep .vueAudioBetter .operate span[data-v-3a8dc9f9]:last-child{
            font-size: 1rem;
          }

        }
      }
    }
  }
}
.loading{
  z-index: 999;
  position: fixed;
  left: 50%;
  .el-icon-loading{
    color: $default-font-color;
    font-size: 3rem;
  }
}
.initial{
  top: 5vh;
}
.later{
  bottom: 0;
}
</style>