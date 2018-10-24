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
  if (to.meta.requireAuth) {
    if (store.state.token) {
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

axios.interceptors.request.use(
  config => {
    if (store.state.token) {
      config.auth = {username: `${store.state.token}`}
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
