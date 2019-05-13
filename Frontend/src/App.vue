<template>
  <div id="app">
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive"></router-view>
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive"></router-view>
  </div>
</template>
<script>
  import headers from './components/header/homeHeader'
  import login from './components/Login'
  // import $ from 'jquery'
  export default {
    name: 'App',
    data () {
      return {}
    },
    mounted () {
     /**
      * 手机端的全屏显示
      * @example safari
      */
      // $('#app').css('height', window.innerHeight + 100)
      // window.scrollTo(0, 1)
      // $('#app').css('height', window.innerHeight)
      // document.addEventListener('touchmove', function (e) {
      //   e.preventDefault()
      // }, false)
    },
    components: {
      'v-header': headers,
      'login': login
    }
  }
</script>

<style>
</style>
