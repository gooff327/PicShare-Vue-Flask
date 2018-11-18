<template>
  <div>
    <brand-header></brand-header>
    <home-contents @setContents="contentsUpdate" :contents = 'contents'></home-contents>
  </div>
</template>
<script>
  import homeHeader from '../header/homeHeader'
  import contentsPanel from './contents'
    export default {
        name: 'home',
      components: {
          'brandHeader': homeHeader,
          'HomeContents': contentsPanel
      },
      data () {
        return {
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
          contentsUpdate: function (newData) {
            this.contents = newData
          }
      }
    }
</script>

<style scoped>

</style>
