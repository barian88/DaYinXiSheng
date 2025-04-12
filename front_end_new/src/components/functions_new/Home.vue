<template>
  <div class="home">
    <img :src="user.avatar" alt="" />
    <div class="nickname">用户名: {{user.nickname}}</div>
    <div class="ip">登陆地址: {{user.ipAddr}}</div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      user: {}
    };
  },
  methods: {

  },
  mounted() {
    this.user = this.global.user;
  },
};
</script>

<style scoped lang="scss">
@import "../../assets/style/base.scss";

.home{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  img{
    width: 15%;
    border-radius: 50%;
    margin-top: -8%;
  }
  .nickname{
    font-size: 1.5rem;
    margin-top: 1rem;
    color: $default-font-color;
  }
  .ip{
    font-size: 1.5rem;
    margin-top: 1rem;
    color: $secondary-font-color;
  }
}
</style>