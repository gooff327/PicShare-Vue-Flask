<template>
  <el-container>
    <el-header>
      <i @click="goBack" class="el-icon-back"></i>
      <span>消 息</span>
    </el-header>
    <el-row>
      <el-col :span="24" @click="forwardDetails">
        <div class="row-wrapper" @click="forwardDetails">
          <span style="background-color: #f17c67" class="icon-wrapper">
            <i class="fa fa-share-alt"></i>
          </span>
          <span class="icon-desc">@我的动态  <el-badge :hidden="this.GLOBAL.COUNT.forwardCount === 0" :value="this.GLOBAL.COUNT.forwardCount" :max="99"
                                                   class="badge"/></span>
        </div>
      </el-col>
      <el-col :span="24" @click="goBack">
        <div class="row-wrapper" @click="admireDetails">
          <span style="background-color: #fa5a5a" class="icon-wrapper">
            <i class="fa fa-thumbs-o-up"></i>
          </span>
          <span class="icon-desc">我收到的赞  <el-badge :hidden="this.GLOBAL.COUNT.admireCount === 0" :value="this.GLOBAL.COUNT.admireCount" :max="99"
                                                   class="badge"/></span>
        </div>
      </el-col>
      <el-col :span="24" @click="privateDetails">
        <div class="row-wrapper" @click="privateDetails">
          <span style="background-color: #00be70" class="icon-wrapper">
            <i class="fa fa-envelope-open-o"></i>
          </span>
          <span class="icon-desc">私信  <el-badge :hidden="this.GLOBAL.COUNT.privateCount === 0" :value="this.GLOBAL.COUNT.privateCount" :max="99" class="badge"/></span>
        </div>
      </el-col>
      <el-col :span="24" @click="followDetails">
        <div class="row-wrapper" @click="followDetails">
          <span style="background-color: #418DFF" class="icon-wrapper">
            <i class="fa fa-users"></i>
          </span>
          <span class="icon-desc">好友关注  <el-badge :hidden="this.GLOBAL.COUNT.followCount === 0" :value="this.GLOBAL.COUNT.followCount" :max="99"
                                                  class="badge"/></span>
        </div>
      </el-col>
      <!--<el-col :span="24" @click="commentDetails">-->
        <!--<div class="row-wrapper" @click="forwardDetails">-->
          <!--<span style="background-color: #f17c67" class="icon-wrapper">-->
            <!--<i class="fa fa-share-alt"></i>-->
          <!--</span>-->
          <!--<span class="icon-desc">@我的动态  <el-badge :value="this.GLOBAL.COUNT.sum" :max="99" class="badge"/></span>-->
        <!--</div>-->
      <!--</el-col>-->
    </el-row>
  </el-container>
</template>

<script>
  export default {
    name: 'message',
    data () {
      return {
      }
    },
    created: function () {
    },
    methods: {
      goBack: function () {
        this.$router.back()
      },
      admireDetails: function () {
      },
      followDetails: function () {
      },
      privateDetails: function () {
      },
      forwardDetails: function () {
      },
      commentDetails: function () {
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

  .row-wrapper {
    margin: 0.4rem 0;
  }

  .badge {
    display: inline-block;
    float: right;
    line-height: 3rem;
  }

  .icon-wrapper {
    display: inline-block;
    height: 3rem;
    width: 3rem;
    text-align: center;
    line-height: 3rem;
    border-radius: 50%;
    font-size: 1.4rem;
    color: white;
    margin-left: 0.6rem;
  }

  .icon-desc {
    display: inline-block;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    font-weight: 600;
    line-height: 3rem;
    width: 76%;
    margin-left: 0.6rem;
    border-bottom: 1px solid rgb(226, 226, 226);
  }
</style>
