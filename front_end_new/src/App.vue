<template>
  <div id="app">
    <RouterView></RouterView>
  </div>
</template>

<script>

export default {
  name: "app",
  components: {
  },
};
</script>

<style lang="scss">
@import "./assets/style/base.scss";

:root{
  font-size: 14px;
  background-color: $background-color;

}
::-webkit-scrollbar {
  width: 0;
  height: 0;
}

// 阿里字体图标设置
.icon, .iconfont {
  font-family:"iconfont" !important;
  font-size:16px;
  font-style:normal;
  -webkit-font-smoothing: antialiased;
  -webkit-text-stroke-width: 0.2px;
  -moz-osx-font-smoothing: grayscale;
}

</style>
