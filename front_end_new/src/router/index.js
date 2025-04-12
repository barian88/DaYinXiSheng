import Vue from 'vue'
import VueRouter from 'vue-router';
Vue.use(VueRouter);

import Picture from '../components/functions_new/Picture.vue';
import Video from '../components/functions_new/Video.vue';
import Album from '../components/functions_new/Album.vue';
import Home from '../components/functions_new/Home.vue';
import Remen from '../components/functions_new/Remen.vue';
import Moment from '../components/functions_new/Moment.vue';
import MusicBase from "../components/functions_new/MusicBase.vue";
import Login from '../components//Login.vue';
import Structure from "../components/Structure.vue";

Vue.config.productionTip = false

const router = new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/login',
            component: Login
        },
        {
            path: '/',
            component: Structure,
            children: [
                {
                    path: '/',
                    component: Remen,
                }, {
                    path: '/home',
                    component: Home
                }, {
                    path: '/picture',
                    component: Picture
                }, {
                    path: '/video',
                    component: Video
                }, {
                    path: '/album',
                    component: Album
                }, {
                    path: '/moment',
                    component: Moment
                },
                {
                    path: '/musicBase',
                    component: MusicBase
                }
            ]
        }

    ]
})

export default router;