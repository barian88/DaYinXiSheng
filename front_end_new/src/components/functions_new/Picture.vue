<template>
  <div class="picture">
    <div class="resourse">
      <div class="titlewords">项目素材</div>
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
          <div v-if="imgShow.length !== 0" class="preview_up_img">
            <img
              :src="imgShow"
            />
          </div>
        </div>
      <div class="preview_down">
        <div class="preview_down_left">
          <div class="preview_down_left_item">
            <div class="titlewords">图片情绪</div>
            <i class="icon iconfont icon-xiaolian"></i>
            <el-progress :text-inside="true" :stroke-width="16" :percentage="emo.emoValue" color="#00C1CD"></el-progress>
            <i class="icon iconfont icon-nanguo"></i>
          </div>
          <div class="preview_down_left_item">
            <div class="titlewords">音乐情绪</div>
            <i class="icon iconfont icon-xiaolian"></i>
            <el-progress :text-inside="true" :stroke-width="16" :percentage="emo.musicEmo" color="#00C1CD"></el-progress>
            <i class="icon iconfont icon-nanguo"></i>
          </div>
          <div class="preview_down_left_item">
            <div class="titlewords">匹配损失</div>
            <div class="tents">{{emo.musicEmoDis}}</div>
          </div>
        </div>
        <div class="preview_down_right">
          <div class="preview_down_right_item">
            <el-button :disabled="imgShow.length === 0" @click="requestMusicList">
              <i class="icon iconfont icon-fenxi"></i>
              <span>配乐</span>
            </el-button>
          </div>
          <div class="preview_down_right_item">
            <el-button :disabled="playingMusic.url === '123'" @click="showShareDialog">
              <i class="icon iconfont icon-fenxiang"></i>
              <span>分享</span>
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
<!--        <audio ref="audio" :src="playingMusic.url" controls="controls"></audio>-->
        <mini-audio class="audio-player" :audio-source="playingMusic.url" ref="audio">
        <!--                    audio-source="https://bucket-1305916869.cos.ap-beijing.myqcloud.com/music_recommendation/06BA9LHRT0.wav"-->
        </mini-audio>
<!--        <vue-audio style="position: absolute; top: 0; left: 0; width: 300px; height:100px;"-->
<!--                    audio-source="https://bucket-1305916869.cos.ap-beijing.myqcloud.com/music_recommendation/06BA9LHRT0.wav"-->
<!--        ></vue-audio>-->
      </div>
    </div>

    <Share ref="shareDialog"></Share>
  </div>
</template>

<script>
import Share from "./share/Share.vue";
export default {

  components: {
    Share
  },
  data() {
    return {
      fileList: [],
      imgShow: "",
      imgShowCosUrl: "",
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
    };
  },
  methods: {
    // 删除图片，并从qCloud中删除
    handleRemove(file, fileList) {
      this.$axiosSpring({
        method: "POST",
        url: "cos/delete",
        params: {
          fileKey: file.fileKey,
        },
      });
    },
    // 预览图片
    handlePreview(file, fileList) {
      // 图片前台展示
      this.imgShow = file.url;
      //  图片的cos地址
      this.imgShowCosUrl = file.fileUrl;
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
      //上传图片后将response中的图片信息存到list
      let url = response.data.fileUrl;
      let key = response.data.fileKey;
      let obj = file;
      obj["fileKey"] = key;
      obj["fileUrl"] = url;
      file = obj;
      // console.log(fileList)
    },
    // 请求flask端，对选中的图片进行配乐
    requestMusicList(){
      // 提示message
      let message = this.$message({
        message: '正在智能分析中，请确认图片右上角均已出现绿色勾号后再点击分析！',
        type: "info",
        duration: 0
      });
      //console.log(file, fileList)
      // 请求flask接口
      this.$axiosFlask({
        method: "GET",
        url: "singleImgEmo",
        params: {
          imgUrl: this.imgShowCosUrl,
        },
      }).then((res) => {
        console.log(res.data)
        this.emo.emoValue = (res.data.emoValue * 100).toString().slice(0,4)
        this.musicList = res.data.musicList
        message.close()
        this.$message({
          message: '匹配成功！注意：点击“视频导出”前请确认已播放选中的配乐，否则导出不成功',
          type: "success",
        });
      });
    },
    // 选中歌曲时自动播放，同时更新音乐情绪值
    play(item){
      this.playingMusic = item
      this.$refs.audio.play()
      this.emo.musicEmo = (item.value * 100).toString().slice(0,4)
      this.emo.musicEmoDis = (item.dis * 100).toString().slice(0,4) + '%'
      // const audio = this.$refs.audio;
      //
      // if (audio) {
      //   audio.oncanplay = () => {
      //     audio.play();
      //   };
      // }
    },
    // 显示分享弹窗
    showShareDialog(){
      let post = {
        id: null,
        userId: null,
        music: this.playingMusic,
        title: '',
        detail: '',
        type: 'picture',
        url: this.imgShowCosUrl, //cos地址
        date: '',
        coverUrl: this.imgShow, //前台展示地址
      };
      // 调用share组件的方法
      this.$refs.shareDialog.showShareDialog(post);
    }

  },
};
</script>


<style lang="scss" scoped>

@import "src/assets/style/picture.scss";

</style>

