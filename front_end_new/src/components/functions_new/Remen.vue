<template>
  <div class="remen">
    <div class="remen_leftbar">
<!--      组件左上角的卡片-->
      <div class="remen_container">
        <div class="box" v-for="(item,index) in cards" :key="index">
          <img :src=item.url />
          <div class="box_title">{{item.box_title}}</div>
          <div class="box_tents">
            {{item.box_tents}}
          </div>
        </div>
      </div>
<!--      组件左下角的图标-->
      <div class="remen_emo"><Emotion></Emotion></div>
    </div>
<!--    组件最右侧的音乐列表-->
    <div class="remen_rightbar">
      <div class="remen_song">
        <div class="remen_titlewords">热门配乐</div>
        <div class="remen_song_list">
          <div class="remen_list_item" v-for="(item,index) in items" :key="index">
            <div class="remen_list_item_rank">
              {{item.remen_list_item_rank}}
            </div>
            <div class="remen_list_item_song">
                <div class="remen_list_item_title">
                  {{item.remen_list_item_title}}
                </div>
                <!--              <audio ref="audio" src="" controls="controls" style="height: 100%;weight:25%"></audio>-->
              <div class="remen_list_item_detail">
                <div class="remen_list_item_artist">
                  作者：{{item.remen_list_item_artist}}
                </div>
                <div class="remen_list_item_emo">
                  情绪值：{{(item.remen_list_item_emo * 100).toString().slice(0,5) + '%'}}
                </div>
                <div class="remen_list_item_times">
                  匹配次数：{{item.remen_list_item_times}}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Emotion from "./graph/emotion_like.vue";
export default {
  data() {
    return {
      cards: [
        {
          url:"https://bucket-1305916869.cos.ap-beijing.myqcloud.com/post_file/card_1.jpg",
          box_title:'杨家山里的月季花谷你去过吗',
          box_tents:'在杨家山里藏着一个世外桃源，漫山遍野的月季花含苞待放，适合御剑飞行，适合拍照，适合约会，还能遛娃，还能樱桃采摘！',
        },
        {
          url:"https://bucket-1305916869.cos.ap-beijing.myqcloud.com/post_file/card_2.jpg",
          box_title:'青山渔村-牌坊好美',
          box_tents:'整个渔村红瓦黄墙，层叠错落，拍照绝绝子，非常出片。不仅有美景，海边晓饭馆也值得推荐哦。',
        },
        {
          url:"https://bucket-1305916869.cos.ap-beijing.myqcloud.com/post_file/card_3.jpg",
          box_title:'亲子游玩好去处 二月二农场',
          box_tents:'可以自己做豆腐，做海凉粉等，还有小红军乐园可以畅玩一整天，一起来二月二农场亲近小动物体验乡村生活吧！',
        },
        {
          url:"https://bucket-1305916869.cos.ap-beijing.myqcloud.com/post_file/card_4.jpg",
          box_title:'青岛海神庙露营打卡，面朝大海春暖花开',
          box_tents:'海与浪，温与柔，爱与不爱，皆自由。这个夏天，来海神庙看海吧！',
        },
        {
          url:"https://bucket-1305916869.cos.ap-beijing.myqcloud.com/post_file/card_5.jpg",
          box_title:'沿着海边一路向北',
          box_tents:'走在沿海公路，吹着海风，感受一丝喧嚣外的宁静',
        },
      ],
      items: [
        {
          remen_list_item_rank:'1',
          remen_list_item_title:'how it feels to love you',
          remen_list_item_artist:'aimless',
          remen_list_item_emo:'0.349742',
          remen_list_item_times:'16'
        },
        {
          remen_list_item_rank:'2',
          remen_list_item_title:'夜空下的幻想',
          remen_list_item_artist:'余日秋山',
          remen_list_item_emo:'0.233506',
          remen_list_item_times:'13'
        },
        {
          remen_list_item_rank:'3',
          remen_list_item_title:'Children`s Introduction',
          remen_list_item_artist:'西原健一郎',
          remen_list_item_emo:'0.999998',
          remen_list_item_times:'11'
        },
        {
          remen_list_item_rank:'4',
          remen_list_item_title:'Normand Corbeil - 暴雨',
          remen_list_item_artist:'三亩地',
          remen_list_item_emo:'0.989386',
          remen_list_item_times:'9'
        },
        {
          remen_list_item_rank:'5',
          remen_list_item_title:'Lost In Your Eyes (ft Per Rinaldo)',
          remen_list_item_artist:'Timecop1983',
          remen_list_item_emo:'0.128668',
          remen_list_item_times:'7'
        },
        {
          remen_list_item_rank:'6',
          remen_list_item_title:'ワールド・ワイド・ボクシステム',
          remen_list_item_artist:'Annabel',
          remen_list_item_emo:'0.595077',
          remen_list_item_times:'5'
        },
        {
          remen_list_item_rank:'7',
          remen_list_item_title:'Five O\' Clock',
          remen_list_item_artist:'Away the ways',
          remen_list_item_emo:'0.981233',
          remen_list_item_times:'3'
        },
        {
          remen_list_item_rank:'8',
          remen_list_item_title:'So In Love (Original Mix)',
          remen_list_item_artist:'Brock Berrigan',
          remen_list_item_emo:'0.832692',
          remen_list_item_times:'2'
        },
      ]
    }
  },
  components: {
    Emotion,
  },
  methods: {
  //如果用户没有登陆，重定向到Login页面
  }
};
</script>


<style lang="scss" scoped>
@import "../../assets/style/base.scss";


.remen {
  margin: 3% 1% 0.5% 4%;
  width: 94%;
  height: 90%;
  display: flex;
  flex-direction: row;
  align-items: space-between;
  justify-content: space-between;
}
.remen_leftbar {
  position: relative;
  width: 62%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
}
.remen_container {
  position: relative;
  height: 56%;
  width: 100%;
  display: flex;
  margin-bottom: 2%;
}
.box {
  overflow: hidden;
  flex: 1;
  height: 100%;
  margin: 0 1% 0 0;
  border: $border-width-thinner solid $border-color;
  color: $default-font-color;
  transition: all 0.5s;
  border-radius: $default-border-radius;
}
.box img {
  object-fit: contain;
  height: 85%;
  display: block;
  transition: all 0.5s;
}

.box:hover {
  flex-basis: 40%;
}
.box:hover > img {
  height: 80%;
}
.box:hover > img:hover {
  height: 92%;
}
.box_tents {
  display: none;
  padding: 2%;
}
.box_title {
  margin-bottom: 2%;
  overflow: hidden;
}
.box:hover .box_tents {
  display: block;
  font-size: 0.8rem;
}
.remen_emo {
  width: 100%;
}
Emotion{
  position: relative;
  width: 100%;
  height: 100%;
}

.remen_rightbar{
  position: relative;
  width: 37%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  border: $border-width-thinner solid $border-color;
  border-radius: $default-border-radius;
}

.remen_song{
  position: relative;
  height: 100%;
  width: 100%;
  padding: 0 0% 0% 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
}
.remen_titlewords {
  height: 8%;
  width: 100%;
  /* padding: 0.2rem 1.5rem; */
  text-align: center;
  color: $default-font-color;
  /*border-bottom: solid 0.01rem #dce3eb;*/
  font-size: 1rem;
  font-weight: 900;
  font-family: YaHei;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: $theme-color;
  margin:0 0 2% 0;
  border-top-left-radius: $default-border-radius;
  border-top-right-radius: $default-border-radius;
}
.remen_song_list{
  position: relative;
  width: 100%;
  height: 110%;
  overflow: scroll;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;

}

.remen_list_item{
  width: 100%;
  display: flex;
  flex: 1;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  /*margin: 2%;*/
  padding: 2% 0 0 0;
  margin: 0 0 2% 0;
  transition: all 500ms ease-in-out;
}
.remen_list_item:hover{
  padding: 4% 0 0 0;
}
.remen_list_item_rank{
  height: 10%;
  margin-top: 3%;
  font-size: 1.2rem;
  color: $default-font-color;
  flex-basis: 10%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.remen_list_item_song{
  flex-basis: 90%;
  display: flex;
  flex-direction: column;
}

.remen_list_item_detail{
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  padding-right: 10%;
}

.remen_list_item_title {
  /*margin: 0 5% 0 0;*/
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  font-family: YaHei;
  color: $default-font-color;
  line-height: 1.8rem;
  font-size: 1.2rem;
  overflow: scroll;
  border-bottom: solid 0.05rem $border-color;
}
.remen_list_item_artist, .remen_list_item_emo, .remen_list_item_times {
  margin: 1rem 0rem;
  width: 100%;
  font-family: YouYuan;
  color: $default-font-color;
  font-size: 1rem;
  overflow: scroll;
}


</style>
