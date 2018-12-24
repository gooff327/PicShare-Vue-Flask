<template>
  <el-container>
    <el-header>
      <i @click="goBack" class="el-icon-back"></i>
      <span>消 息</span>
    </el-header>
  </el-container>
</template>

<script>
  export default {
    name: 'message',
    data () {
      return {}
    },
    methods: {
      goBack: function () {
        this.$router.back()
      }
    }
  }
</script>

<style scoped>
  .el-header {
    padding: 0;
    margin-top: 10px;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px gainsboro solid;
    height: 30px !important;
  }

  .el-header span {
    vertical-align: center;
    display: inline-block;
    color: rgba(43, 43, 43, 0.93);
    width: 86%;
    text-align: center;
    font-size: 1.0rem;
  }

  .el-icon-back {
    position: relative;
    width: 6%;
    line-height: 100%;
    padding-left: 1%;
    font-size: 1rem;
  }

</style>
