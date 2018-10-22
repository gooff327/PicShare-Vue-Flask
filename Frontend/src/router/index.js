import Vue from 'vue'
import Router from 'vue-router'
import login from '../components/Login'
import home from '../components/home/home'
import admin from '../components/admin/admin'
Vue.use(Router)

export default new Router({
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
      meta: { requireAuth: true }
    },
    {
      path: '/admin',
      name: 'admin',
      component: admin,
      meta: { requireAuth: true }
    }
  ]
})
