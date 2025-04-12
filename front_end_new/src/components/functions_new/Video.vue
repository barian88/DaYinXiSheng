<template>
  <div class="video">
    <canvas id="myCanvas"></canvas>
    <div class="resourse">
      <div class="titlewords">视频素材</div>
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
      <div class="preview_up">
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
            <div class="titlewords">视频情绪</div>
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
          <el-button :disabled="playerOptions.sources[0].src.length === 0"
                     @click="requestMusicList">
            <i class="icon iconfont icon-fenxi"></i>
            <span>配乐</span>
          </el-button>
          <el-button :disabled="playerOptions.sources[0].src.length === 0 || playingMusic.url === '123'"
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
      // 当前选中播放的音乐
      playingMusic: {
        id: '',
        title: '',
        url: '123'
      },
      musicList: [],
      emo: {
        emoValue: 0,
        musicEmo: 0,
        musicEmoDis: "请选择"
      },
      selectedVideo: "", //当前被选择的视频文件，videoPlayer中播放的视频文件
      processedVideoPath: '',  //处理好的视频地址，仅用来后端传参
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
      outputUrl: '', //导出的视频的url,video组件播放时使用，与playerOptions.sources[0].src绑定
      outputBlobData: null, //导出的视频的blob对象，分享时用
      fileCoverUrl: '' //视频的封面url
    };
  },
  methods: {
    test(){
      function dataURLToFile(dataUrl, fileName) {
        const dataArr = dataUrl.split(',');
        const mime = dataArr[0].match(/:(.*?);/)[1];
        const bstr = atob(dataArr[1]);
        let n = bstr.length;
        const u8arr = new Uint8Array(n);
        while (n--) {
          u8arr[n] = bstr.charCodeAt(n);
        }
        return new File([u8arr], fileName, { type: mime });
      }
      let file = dataURLToFile(this.fileCoverUrl, '测试文件.png')
      // console.log(file);
      // 创建 FormData 对象
      const formData = new FormData();
      formData.append('file', file);
      this.$axiosSpring({
        method: 'post',
        url: '/cos/upload',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(res => {
        // console.log(res)
      })

    },

    // 删除视频，并从qCloud中删除
    handleRemove(file, fileList) {
      this.$axiosSpring({
        method: "POST",
        url: "cos/delete",
        params: {
          fileKey: file.fileKey,
        },
      });
    },
    // 选择视频，在videoPlayer中播放
    handlePreview(file, fileList) {
      // 将选中的视频存起来
      this.selectedVideo = file;
      // 初始化videoPlayer
      this.playerOptions.sources[0].src = file.videoPreviewUrl;
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
    // 上传成功后的回调
    handleSuccess(response, file, fileList) {
      //上传图片后将云服务器中的图片信息存到list
      let url = response.data.fileUrl;
      let key = response.data.fileKey;
      let obj = fileList[fileList.length - 1];
      obj["fileKey"] = key;
      obj["fileUrl"] = url;
      // 将视频的url存起来，因为findVideoCover会改变file.url用来回显；使用videoPreviewUrl作为video组件的src
      obj["videoPreviewUrl"] = file.url;
      fileList[fileList.length - 1] = obj;
      this.findVideoCover(url,file)

    },

    //截取视频第一帧作为播放前默认图片
    findVideoCover(url,file) {
      const video = document.createElement("video") // 也可以自己创建video
      video.src=url // url地址 url跟 视频流是一样的
      var canvas = document.getElementById('myCanvas') // 获取 canvas 对象
      const ctx = canvas.getContext('2d'); // 绘制2d
      video.crossOrigin = 'anonymous' // 解决跨域问题，也就是提示污染资源无法转换视频
      video.addEventListener('loadedmetadata', () => {
        video.currentTime = 0;  // 尝试获取第一帧
      });
      video.addEventListener('seeked', () => {
        canvas.width = video.videoWidth;  // 使用视频固有宽度
        canvas.height = video.videoHeight;  // 使用视频固有高度
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        file.url = canvas.toDataURL();  // 截取后的视频封面
        this.fileCoverUrl = file.url;  // 用于分享时的封面
        // console.log(this.fileCoverUrl )
      });
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

    // 请求flask端，对选中的视频进行配乐
    requestMusicList() {
      let message = this.$message({
        message: '正在智能分析中......',
        type: "info",
        duration: 0
      });
      this.$axiosFlask({
        method: "GET",
        url: "matchMusicForVideo",
        params: {
          videoUrl: this.selectedVideo.fileUrl,
        },
      }).then((res) => {
        message.close()
        // console.log(res.data)
        message = this.$message({
          message: '匹配成功！注意：点击“视频导出”前请确认已播放选中的配乐，否则导出不成功',
          type: "success",
        });
        this.emo.emoValue = (res.data.emoValue * 100).toString().slice(0,4)
        this.musicList = res.data.musicList
        this.processedVideoPath = res.data.processedVideoPath
      });
    },
    // 拼接音乐与视频并导出
    previewVideo(){
      // 弹出提醒
      let message = this.$message({
        message: '正在合成视频与背景音乐......',
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
        url: 'exportVideo',
        params: {
          processedVideoPath: this.processedVideoPath,
          musicUrl: this.playingMusic.url
        },
        responseType: 'blob' // 重要：设置响应类型为Blob
      }).then(response => {
        message.close();
        const videoBlob = new Blob([response.data], { type: 'video/mp4' });
        this.outputBlobData = videoBlob;
        this.outputUrl = URL.createObjectURL(videoBlob);// 创建一个URL来访问Blob
        // console.log(this.outputUrl);
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
        type: 'video',
        blob: this.outputBlobData, //视频是blob对象，没有cosURL，需要在Share组件中处理
        date: '',
        coverUrl: this.fileCoverUrl, //封面是DataURL对象，没有cosURL，需要在Share组件中处理
      };
      // 调用share组件的方法
      this.$refs.shareDialog.showShareDialog(post);
    }

  },
};
</script>


<style lang="scss" scoped>

@import "src/assets/style/video_album.scss";
#myCanvas {
  display: none;
}
</style>
