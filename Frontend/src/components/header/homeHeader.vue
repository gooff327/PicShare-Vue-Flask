<template>
<div class="brand">
  <img src="../../../static/icons/logo.png">
</div>
</template>

<script>
    export default {
      name: 'homeHeader',
      methods: {
        toAdmin () {
          this.$router.push({path: '/admin'})
        }
      }
    }
</script>

<style scoped>
.brand img{
  position: relative;
  top: 0;
  width: 95%;
  height: 2rem;
}

</style>
