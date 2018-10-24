<template>
<brand-header></brand-header>
</template>

<script>
  import homeHeader from '../header/homeHeader'
    export default {
        name: 'home',
      components: {'brandHeader': homeHeader},
      created: function () {
       console.log('created!')
        let url = 'http://127.0.0.1:5000/api/v1/resource'
        this.$axios.get(url).then(function (response) {
          console.log(response)
        })
      },
data () {
          return {
            content: ''
          }
      }
    }
</script>

<style scoped>

</style>
