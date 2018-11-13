<template>
  <div class="el-container">
    <div class="row">
      <i class="fa fa-home"></i>
      <i class="fa fa-handshake-o"></i>
      <i class="fa fa-plus-circle"></i>
      <i class="fa fa-envelope-o"></i>
      <i class="fa fa-user-o"></i>
    </div>
  </div>
</template>

<script>
    export default {
        name: 'bottom'
    }
</script>

<style scoped>
  .row{
    width: 100%;
  }
  .el-container{
    position: fixed;
    bottom: 0;
    background-color: rgba(255,255,255,1);
  }
  .fa{
    color: #409EFF;
    font-size: 36px;
  }
</style>
