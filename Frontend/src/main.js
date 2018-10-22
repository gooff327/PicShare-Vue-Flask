// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import store from './vuex/user.js'

Vue.prototype.$axios = axios
Vue.use(VueAxios)
Vue.use(ElementUI)
Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
  console.log('全局路由控制')
  let token = store.state.token
  if (to.matched.some(route => route.meta.requireAuth)) {
    if (token) {
      next()
    } else {
      next({
        path: '/',
        query: {redirect: to.fullPath}
      })
    }
  } else {
    next()
  }
})
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
