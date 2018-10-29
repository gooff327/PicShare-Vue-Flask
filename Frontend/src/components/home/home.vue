<template>
  <div>
    <brand-header></brand-header>
    <home-content :content = 'content'></home-content>
  </div>
</template>
<script>
  import homeHeader from '../header/homeHeader'
  import content from './content'
    export default {
        name: 'home',
      components: {
          'brandHeader': homeHeader,
          'HomeContent': content
      },
      data () {
        return {
          content: {}
        }
      },
      created: function () {
        let url = 'http://127.0.0.1:5000/api/v1/resource'
        this.$axios.get(url).then(function (response) {
          this.content = response.data
          console.log(this.content)
        }.bind(this))
      }
    }
</script>

<style scoped>

</style>
