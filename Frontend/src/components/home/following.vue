<template>
  <v-home></v-home>
</template>

<script>
  import homeWrapper from './home'

  export default {
    name: 'following',
    data () {
      return {
      }
    },
    created: function () {
      this.GLOBAL.closeLoading()
    },
    components: {
      'v-home': homeWrapper
    }
  }
</script>

<style scoped>

</style>
