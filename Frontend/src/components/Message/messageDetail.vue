<template>
  <el-container>
    <el-header>
      <i @click="goBack" class="el-icon-back"></i>
      <span v-text="this.$route.params.label"></span>
    </el-header>
  </el-container>
</template>

<script>
  export default {
    name: 'messageDetail',
    created: function () {
      this.initMessage(this.$route.name)
    },
    methods: {
      goBack: function () {
        this.$router.back()
      },
      initMessage: function (messageType) {
        let url = this.GLOBAL.BASE_URL + '/api/v1/get/messages'
        this.$axios.get(url, {
          params: {messageType: messageType.slice(2)}
        }).then(function (res) {
          console.log(res.data)
        })
      }
    }
  }
</script>

<style scoped>
  .el-header {
    padding: 0;
    margin: 0;
    padding-bottom: 1rem;
    border-bottom: 1px gainsboro solid;
    height: 2.6rem !important;
  }

  .el-header span {
    vertical-align: center;
    display: inline-block;
    color: rgba(43, 43, 43, 0.93);
    width: 86%;
    text-align: center;
    font-size: 1.0rem;
    line-height: 2.6rem;
    font-weight: 700;
  }

  .el-icon-back {
    position: relative;
    width: 6%;
    line-height: 100%;
    padding-left: 1%;
    font-size: 1rem;
  }
</style>
