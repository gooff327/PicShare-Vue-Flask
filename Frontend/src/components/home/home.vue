<template>
  <div>
    <brand-header></brand-header>
    <home-contents :contents = 'contents'></home-contents>
    <nav-bottom :selected=style_active></nav-bottom>
  </div>
</template>
<script>
  import homeHeader from '../header/homeHeader'
  import contentsPanel from './contents'
  import navBottom from '../bottom/bottom'
    export default {
        name: 'home',
      components: {
          'brandHeader': homeHeader,
          'homeContents': contentsPanel,
          'navBottom': navBottom
      },
      data () {
        return {
          style_active: 'color = #409EFF;',
          contents: {}
        }
      },
      created: function () {
        var url = this.GLOBAL.BASE_URL + '/api/v1/resources'
        this.$axios.get(url).then(function (response) {
          this.contents = response.data
          console.log(this.contents)
        }.bind(this))
      },
      methods: {
      }
    }
</script>

<style scoped>
  .homeBtn{
    background-color: black;
  }
</style>
