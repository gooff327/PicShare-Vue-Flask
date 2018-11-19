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
          <el-button @click="editorVisible" size="mini">编辑主页</el-button>
          <el-dialog
            :visible.sync="editSelfPanel"
            :show-close="false"
            :fullscreen="true"
          width="100%">
          </el-dialog>
        </div>
      </el-col>
      <el-col :span="24" class="middle-tab-a">
        <div class="posts">
          <span class="quantity">1</span>
          <br>
          <span class="label">帖子</span>
        </div>
        <div class="followers">
          <span class="quantity">9</span>
          <br>
          <span class="followers">粉丝</span>
        </div>
        <div class="following">
          <span class="quantity">10</span>
          <br>
          <span class="following">关注</span>
        </div>
      </el-col>
      <el-col :span="24" class="middle-tab-b">
        <span class="fa fa-th"></span><span class="fa fa-navicon"></span>
      </el-col>
    </el-row>
  </el-main>
  <nav-bottom></nav-bottom>
</el-container>
</template>

<script>
  import navBottom from '../bottom/bottom'
  export default {
      name: 'personal',
      components: {
          'navBottom': navBottom
      },
      data () {
          return {
            editSelfPanel: false
          }
      },
    methods: {
        editorVisible: function () {
          this.editSelfPanel = true
        }
    }
    }
</script>

<style scoped>
  .el-row{
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;;
  }
  .el-header{
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
    color:rgba(43,43,43,0.93);
  }
  .el-main{
    padding: 0;
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
  .content-left{
    padding-bottom: 1rem;
  }
  .content-right .el-button{
    width: 100%;
  }
  .middle-tab-a{
    border-top: 1px solid gainsboro;
    padding: 0 !important;
  }
  .middle-tab-b{
    border-top: 1px solid gainsboro;
    border-bottom: 1px solid gainsboro;
    padding: 0 !important;
  }
  .middle-tab-a div{
    display: block;
    padding: 0;
    margin: 0;
    width: 33%;
    text-align: center;
    line-height: 2rem;
    float: left;
  }
  .middle-tab-b span{
    display: inline-block;
    padding: 0;
    margin: 0;
    width: 50%;
    text-align: center;
    line-height: 2rem;
  }
</style>
