import Vue from 'vue'
import Router from 'vue-router'
import login from '../components/Login'
import home from '../components/home/home'
import admin from '../components/admin/admin'
import personal from '../components/User/personal'
import upload from '../components/Upload/editor'
import comment from '../components/Common/comment'
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
      component: home,
      meta: {
        requireAuth: true,
        keepAlive: true
      }
    },
    {
      path: '/admin',
      name: 'admin',
      component: admin,
      meta: { requireAuth: true }
    },
    {
      path: '/user/:username',
      name: 'user',
      component: personal,
      meta: { requireAuth: true }
    },
    {
      path: '/create/details',
      name: 'upload',
      component: upload,
      meta: { requireAuth: true }
    },
    {
      path: '/comment/:id',
      name: 'comment',
      component: comment,
      meta: { requireAuth: true }
    }
  ]
})
