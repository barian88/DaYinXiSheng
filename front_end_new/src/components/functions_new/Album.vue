<template>
  <div class="album">
    <div class="resourse">
      <div class="titlewords">多图生成</div>
      <div class="file-list-uploading">
        <el-upload
            class="upload-picture"
            :action="this.global.cosApi"
            :on-success="handleSuccess"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            :limit="9"
            multiple
            :on-exceed="handleExceed"
            :file-list="fileList"
            list-type="picture-card"
        >
          <i class="el-icon-plus"></i>
        </el-upload>
      </div>
    </div>
    <div class="divider"></div>
    <div class="preview">
      <div class="preview_up" id="swiper">
<!--        轮播器，默认展示-->
        <div v-if="imgUrlList.length !== 0 && playerOptions.sources[0].src.length === 0" class="preview_up_album">
          <el-carousel :interval="4000" :height="height">
            <el-carousel-item v-for="item in imgUrlList" :key="item">
              <img :src="item"  >
            </el-carousel-item>
          </el-carousel>
        </div>
        <!--     视频播放器，预览视频时展示-->
        <div v-if="playerOptions.sources[0].src.length !== 0" class="preview_up_video">
          <videoPlayer
              class="video-player vjs-custom-skin"
              ref="videoPlayer"
              :playsinline="true"
              :options="playerOptions"
          >
          </videoPlayer>
        </div>

      </div>
      <div class="preview_down">
        <div class="preview_down_info">
          <div class="preview_down_info_item">
            <div class="titlewords">多图情绪</div>
            <i class="icon iconfont icon-xiaolian"></i>
            <el-progress :text-inside="true" :stroke-width="16" :percentage="emo.emoValue" color="#00C1CD"></el-progress>
            <i class="icon iconfont icon-nanguo"></i>
          </div>
          <div class="preview_down_info_item">
            <div class="titlewords">音乐情绪</div>
            <i class="icon iconfont icon-xiaolian"></i>
            <el-progress :text-inside="true" :stroke-width="16" :percentage="emo.musicEmo" color="#00C1CD"></el-progress>
            <i class="icon iconfont icon-nanguo"></i>
          </div>
          <div class="preview_down_info_item">
            <div class="titlewords">匹配损失</div>
            <div class="tents">{{emo.musicEmoDis}}</div>
          </div>
        </div>
        <div class="preview_down_operation">
          <el-button :disabled="imgUrlList.length === 0"
                     @click="requestMusicList">
            <i class="icon iconfont icon-fenxi"></i>
            <span>配乐</span>
          </el-button>
          <el-button :disabled="imgUrlList.length === 0 || playingMusic.url === '123'"
                     @click="previewVideo">
            <i class="icon iconfont icon-yulan"></i>
            <span>预览</span>
          </el-button>
          <div class="circle_button">
            <el-button size="small" @click="downloadVideo" :disabled="outputUrl.length === 0">
              <i class="icon iconfont icon-xiazai"></i>
            </el-button>
            <el-button size="small" :disabled="outputUrl.length === 0" @click="showShareDialog">
              <i class="icon iconfont icon-fenxiang"></i>
            </el-button>
          </div>
        </div>
      </div>
    </div>
    <div class="divider"></div>
    <div class="music">
      <div class="titlewords">音乐推荐</div>
      <div @click="play(item)"
           class="music_item"
           v-for="(item, index) in musicList"
           :key="index + 2">
          <span class="music-info">
            <span class="music_title">{{ item.title }}</span>
            <span class="music_author">{{ item.artist }}</span>
          </span>
        <span class="music_loss">
            匹配误差：{{ (item.dis * 100).toString().slice(0,4) + '%' }}
          </span>
      </div>
      <div class="music_play_button">
        <mini-audio class="audio-player" :audio-source="playingMusic.url" ref="audio">
          <!--                    audio-source="https://bucket-1305916869.cos.ap-beijing.myqcloud.com/music_recommendation/06BA9LHRT0.wav"-->
        </mini-audio>
<!--        <audio ref="audio" :src="playingMusic.url" controls="controls"></audio>-->
      </div>
    </div>
    <Share ref="shareDialog"></Share>
  </div>
</template>

<script>

import {Message} from "element-ui";
import qs from 'qs'
//引入视频播放组件
import "video.js/dist/video-js.css";
import { videoPlayer } from "vue-video-player";
import Share from "@/components/functions_new/share/Share.vue";


export default {
  components: {
    Share,
    videoPlayer,
  },
  data() {
    return {
      fileList: [],
      emo: {
        emoValue: 0,
        musicEmo: 0,
        musicEmoDis: "请选择"
      },
      // 当前选中播放的音乐
      playingMusic: {
        id: '',
        title: '',
        url: '123'
      },
      musicList: [],
      imgUrlList: [], //轮播器中图片的url地址
      SuccessFileCount: 0, //用来保持fileList和imgUrlList的一致性的计数器
      outputUrl: '', //导出的视频的url,video组件播放时使用，与playerOptions.sources[0].src绑定
      outputBlobData: null, //导出的视频的blob对象，分享时用
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
    };
  },
  computed: {
    height() {
      return document.getElementById('swiper').clientHeight + 'px'
    },
  },
  methods: {
    // 删除图片，并从qCloud中删除,并从imgUrlList中删除
    handleRemove(file, fileList) {
      this.$axiosSpring({
        method: "POST",
        url: "cos/delete",
        params: {
          fileKey: file.fileKey,
        },
      });
      this.imgUrlList = this.imgUrlList.filter(item => item !== file.fileUrl)
      // 计数器相应变化，保持fileList和imgUrlList的一致性
      this.SuccessFileCount --;
    },
    handlePreview(file, fileList) {
    },
    // 上传文件超过限制时的提示
    handleExceed(files, fileList) {
      this.$message.warning(
          `当前限制选择 9 个文件，本次选择了 ${files.length} 个文件，共选择了 ${
              files.length + fileList.length
          } 个文件`
      );
    },
    // 删除文件前的提示
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },

    // 上传成功后的回调,每有一个文件上传成功，就会执行一次这个方法
    handleSuccess(response, file, fileList) {
       // console.log(fileList)
      // 为file添加两个属性，方便后续使用
      let url = response.data.fileUrl;
      let key = response.data.fileKey;
      let obj = file;
      obj["fileKey"] = key;
      obj["fileUrl"] = url;
      file = obj;
      // 上传成功的文件数加一
      this.SuccessFileCount = this.SuccessFileCount + 1
      // 判断是否全部文件上传成功,成功之后，设置imgUrlList,这样做的原因是不会乱序
      if (this.SuccessFileCount === fileList.length){
        this.imgUrlList = fileList.map(item => item.fileUrl)
      }
    },

    play(item){
      this.playingMusic = item
      this.$refs.audio.play()
      this.emo.musicEmo = (item.value * 100).toString().slice(0,4)
      this.emo.musicEmoDis = (item.dis * 100).toString().slice(0,4) + '%'
      // const audio = this.$refs.audio;
      // if (audio) {
      //   audio.oncanplay = () => {
      //     audio.play();
      //   };
      // }
    },

    // 请求flask端，对选中的图片进行配乐
    requestMusicList(){
      let message = this.$message({
        message: '正在智能分析中，请确认图片右上角均已出现绿色勾号后再点击分析！',
        type: "info",
        duration: 0
      });
      console.log(this.imgUrlList)
      this.$axiosFlask({
        method: "GET",
        url: "multiImg",
        params: {
          imgList: this.imgUrlList
        },
        paramsSerializer: params => {
          return qs.stringify(params, { indices: false })
        }
      }).then((res) => {
        //console.log(res.data)
        this.emo.emoValue = (res.data.emoValue * 100).toString().slice(0,4)
        this.musicList = res.data.musicList
        message.close()
        this.$message({
          message: '匹配成功！注意：点击“视频导出”前请确认已播放选中的配乐，否则导出不成功',
          type: "success",
        });
        console.log(this.musicList)
      });
    },
// 拼接音乐与视频并导出
    previewVideo(){
      // 弹出提醒
      let message = this.$message({
        message: '正在合成视频与背景音乐,合成时间较长，请等待!',
        type: 'info',
        duration: 0
      })
      //销毁上一次的blob对象，避免内存泄漏
      if (this.outputUrl) {
        URL.revokeObjectURL(this.outputUrl)
      }
      // 发送请求，获取blob对象
      this.$axiosFlask({
        method: 'get',
        url: 'getVideoForImages',
        params: {
          imgList: this.imgUrlList,
          musicUrl: this.playingMusic.url
        },
        paramsSerializer: params => {
          return qs.stringify(params, { indices: false })
        },
        responseType: 'blob' // 重要：设置响应类型为Blob
      }).then(response => {
        message.close();
        const videoBlob = new Blob([response.data], { type: 'video/mp4' });
        this.outputBlobData = videoBlob; // 保存blob对象，用于分享
        this.outputUrl = URL.createObjectURL(videoBlob);// 创建一个URL来访问Blob,用于视频组件访问
        console.log(this.outputUrl);
        message = this.$message({
          message: '合成成功！',
          type: 'success'
        })
        // 设置video组件的src
        this.playerOptions.sources[0].src  = this.outputUrl;
        //   播放拼接好的视频
        //   this.$refs.videoPlayer.player.play();
      })
    },
//   将拼接好的视频下载到本地
    downloadVideo() {
      const a = document.createElement('a');
      a.style.display = 'none'; // 隐藏这个元素，避免影响页面布局
      a.href = this.outputUrl; // 将输出视频的 URL 设置为下载链接
      a.download = 'video.mp4'; // 设置下载的文件名
      document.body.appendChild(a); // 将元素添加到文档中
      a.click(); // 模拟用户点击这个链接
      document.body.removeChild(a); // 下载后移除这个元素
    },
    // 显示分享弹窗
    showShareDialog(){
      let post = {
        id: null,
        userId: null,
        music: this.playingMusic,
        title: '',
        detail: '',
        type: 'album',
        blob: this.outputBlobData, //视频是blob对象，没有cosURL，需要在Share组件中处理
        date: '',
        coverUrl: this.imgUrlList[0], //封面是cosURL
      };
      // 调用share组件的方法
      this.$refs.shareDialog.showShareDialog(post);
    },


  },
};
</script>


<style lang="scss" scoped>

@import "src/assets/style/video_album.scss";

</style>