<template>
  <div>
    <home-contents @loadMore="getMore" @refresh="refresh" :contents='contents'></home-contents>
    <nav-bottom :selected=style_active></nav-bottom>
  </div>
</template>
<script>
  import contentsPanel from './contents'
  import navBottom from '../bottom/bottom'
  import $ from 'jquery'

  export default {
    name: 'home',
    components: {
      'homeContents': contentsPanel,
      'navBottom': navBottom
    },
    data () {
      return {
        startIndex: 0,
        lastIndex: 10,
        style_active: 'color = #409EFF;',
        contents: {},
        tempContents: {}
      }
    },
    created: function () {
      this.getUpdate(this.$route.name)
    },
    watch: {
      '$route' (to, from) {
        if (to.path === '/following') {
          this.getUpdate(this.$route.name)
        } else if (to.path === 'home') {
          this.getUpdate(this.$route.name)
        }
      }
    },
    methods: {
      getUpdate: function (path) {
        let currentPath = path
        let url = this.GLOBAL.BASE_URL + '/api/v1/resources'
        this.$axios.get(url, {
          params: {
            currentPath: currentPath,
            startIndex: this.startIndex,
            lastIndex: this.lastIndex
          }
        }).then(function (response) {
          this.tempContents = this.contents
          this.contents = response.data
          this.contents = $.extend(this.contents, this.tempContents)
          this.GLOBAL.closeLoading()
        }.bind(this))
      },

      getMore: function () {
        this.startIndex += 10
        this.lastIndex += 10
        this.getUpdate(this.$route.name)
      },

      refresh: function () {
        this.startIndex = 0
        this.lastIndex = 10
        this.contents = {}
        this.getUpdate(this.$route.name)
      }
    }
  }
</script>

<style scoped>
</style>
