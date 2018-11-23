<template>
  <div id="app">
       <!--<router-view></router-view>-->
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive"></router-view>
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive"></router-view>
  </div>
</template>

<script>
  import headers from './components/header/header'
  import login from './components/Login'
export default {
    name: 'App',
    components: {
      'v-header': headers,
      'login': login
    }
}
</script>

<style>

</style>
