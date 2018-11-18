<template>
<el-container>
  <el-header>
    <span class="fa fa-cog"></span>
    <span class="headTitle">个人主页</span>
    <span class="fa fa-user-plus"></span>
  </el-header>
  <el-main>
    <el-row :gutter="20">
      <el-col :span="6">
        <div class="content-left">
          <img class="user-avatar" :src="['data:Image/png;base64,'+this.GLOBAL.USER.avatar]" alt="">
        </div>
      </el-col>
      <el-col :span="18">
        <div class="content-right">
          <span class="user-username" v-text="this.GLOBAL.USER.username"></span>
          <el-button size="mini">编辑主页</el-button>
          <el-dialog
            :visible.sync="editSelfPanel"
            :show-close="false"
            :fullscreen="true"
          width="100%">
          </el-dialog>
        </div>
      </el-col>
    </el-row>
  </el-main>
</el-container>
</template>

<script>
    export default {
        name: 'personal',
      data () {
          return {
            editSelfPanel: false
          }
      }
    }
</script>

<style scoped>
  .el-header{
    padding: 0;
    height: 30px !important;
    border-bottom: 1px solid gainsboro;
  }
  .el-header span {
    vertical-align: center;
    display: inline-block;
    color:rgba(43,43,43,0.93);
  }
  .fa-cog{
    width: 6%;
    line-height: 100%;
    padding-left: 1%;
    font-size: 1.4rem;
  }
  .headTitle{
    width: 80%;
    text-align: center;
    font-size: 1.0rem;
  }
  .fa-user-plus{
    width: 6%;
    float: right;
    padding-right: 10px;
    font-size: 1.4rem;
  }
  .user-avatar{
    width: 100%;
    height: 100%;
    border-radius: 50%;
  }
  .user-username{
    display: inline-block;
    width: 100%;
    font-size: 1.2rem;
    text-align: center;
    padding-bottom: 0.6rem;
  }
  .content-right .el-button{
    width: 100%;
  }
</style>
