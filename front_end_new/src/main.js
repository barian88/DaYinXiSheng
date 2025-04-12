import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import router from './router'
import axios from 'axios';

// 引入iconfont图标
import './assets/icon/iconfont.css';

// 创建axios实例， springboot后端
const springService = axios.create({
    // axios中请求配置有baseURL选项，表示请求URL公共部分
    baseURL: 'http://43.143.226.11:8003',
    // baseURL: 'http://127.0.0.1:8003',
    // 超时
    timeout: 10000,
});
Vue.prototype.$axiosSpring = springService; // 挂载到 Vue 原型
// 创建 Flask 后端的 axios 实例
const flaskService = axios.create({
    // baseURL: 'http://localhost:5000', // 假设 Flask 后端运行在 5000 端口
    baseURL: 'http://43.143.226.11:5000',
    // 超时配置，如果需要
    // timeout: 10000,
});
Vue.prototype.$axiosFlask = flaskService; // 挂载到 Vue 原型

// 引入全局变量
import global from './global/global.js';
Vue.prototype.global = global


new Vue({
    router,
    render: h => h(App),
}).$mount('#app')
