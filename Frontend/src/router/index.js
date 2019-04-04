import Vue from 'vue'
import Router from 'vue-router'
import login from '../components/Login'
import index from '../components/home/index'
import message from '../components/Message/message'
import personal from '../components/User/personal'
import upload from '../components/Upload/editor'
import comment from '../components/Common/comment'
import following from '../components/home/following'
import followlist from '../components/User/followlist'
import messageDetail from '../components/Message/messageDetail'
import contentDetail from '../components/Message/contentDetail'
import forward from '../components/home/forward'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'login',
      component: login
    },
    {
      path: '/home',
      name: 'home',
      component: index,
      meta: {
        requireAuth: true,
        keepAlive: false
      }
    },
    {
      path: '/following',
      name: 'following',
      component: following,
      meta: {
        requireAuth: true,
        keepAlive: true
      }
    },
    {
      path: '/message',
      name: 'message',
      component: message,
      meta: {requireAuth: true}
    },
    {path: '/content/detail/:pid',
      name: 'content',
      component: contentDetail,
      meta: {requireAuth: true}},
    {
      path: '/message/admire',
      name: 'm_admire',
      component: messageDetail,
      meta: {requireAuth: true}
    },
    {
      path: '/message/follow',
      name: 'm_follow',
      component: messageDetail,
      meta: {requireAuth: true}
    },
    {
      path: '/message/comment',
      name: 'm_comment',
      component: messageDetail,
      meta: {requireAuth: true}
    },
    {
      path: '/message/private',
      name: 'm_private',
      component: messageDetail,
      meta: {requireAuth: true}
    },
    {
      path: '/message/forward',
      name: 'm_forward',
      component: messageDetail,
      meta: {requireAuth: true}
    },
    {
      path: '/user/:username',
      name: 'user',
      component: personal,
      meta: {requireAuth: true}
    },
    {
      path: '/user/:username/followers',
      name: 'followers',
      component: followlist,
      meta: {requireAuth: true}
    },
    {
      path: '/user/:username/followings',
      name: 'followings',
      component: followlist,
      meta: {requireAuth: true}
    },
    {
      path: '/create/details',
      name: 'upload',
      component: upload,
      meta: {requireAuth: true}
    },
    {
      path: '/comment/:pid',
      name: 'comment',
      component: comment,
      meta: {requireAuth: true}
    },
    {
      path: '/forward/:pid',
      name: 'forward',
      component: forward,
      meta: {requireAuth: true}
    }
  ]
})
