<template>
  <div>
    <brand-header></brand-header>
    <home-contents @loadMore="getMore" @refresh="refresh" :contents='contents'></home-contents>
    <nav-bottom :selected=style_active></nav-bottom>
  </div>
</template>
<script>
  import homeHeader from '../header/homeHeader'
  import contentsPanel from './contents'
  import navBottom from '../bottom/bottom'
  import $ from 'jquery'

  export default {
    name: 'home',
    components: {
      'brandHeader': homeHeader,
      'homeContents': contentsPanel,
      'navBottom': navBottom
    },
    data () {
      return {
        startIndex: 0,
        lastIndex: 5,
        style_active: 'color = #409EFF;',
        contents: {},
        tempContents: {},
        preContents: {}
      }
    },
    watch: {
      '$route' (to, from) {
        console.log(to.path, from.path)
        if (from.path === '/create/details') {
          this.getUpdate()
        }
      }
    },
    created: function () {
      this.getUpdate()
    },
    methods: {
      getUpdate: function () {
        let url = this.GLOBAL.BASE_URL + '/api/v1/resources'
        this.$axios.get(url, {
          params: {
            startIndex: this.startIndex,
            lastIndex: this.lastIndex
          }
        }).then(function (response) {
          console.log('res', response.data)
          this.tempContents = this.contents
          this.contents = response.data
          console.log('get', this.contents)
          this.preContents = $.extend(this.contents, this.tempContents)
          console.log('pre', this.preContents)
          this.contents = this.preContents
          console.log(this.contents)
        }.bind(this))
      },
      getMore: function () {
        this.startIndex += 5
        this.lastIndex += 5
        this.getUpdate()
      },
      refresh: function () {
        this.startIndex = 0
        this.lastIndex = 5
        this.getUpdate()
      }
    }
  }
</script>

<style scoped>
  .homeBtn {
    background-color: black;
  }
</style>
