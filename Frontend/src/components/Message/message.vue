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
          <span class="icon-desc">@我的动态  <el-badge :hidden="this.GLOBAL.COUNT.forwardCount === 0"
                                                   :value="this.GLOBAL.COUNT.forwardCount" :max="99"
                                                   class="badge"/>
          </span>
        </div>
      </el-col><el-col :span="24" @click="forwardDetails">
        <div class="row-wrapper" @click="commentDetails">
          <span style="background-color: #00be70" class="icon-wrapper">
            <i class="fa fa-comments"></i>
          </span>
          <span class="icon-desc">评 论  <el-badge :hidden="this.GLOBAL.COUNT.commentCount === 0"
                                                   :value="this.GLOBAL.COUNT.commentCount" :max="99"
                                                   class="badge"/>
          </span>
        </div>
      </el-col>
      <el-col :span="24" @click="admireDetails">
        <div class="row-wrapper" @click="admireDetails">
          <span style="background-color: #fa5a5a" class="icon-wrapper">
            <i class="fa fa-thumbs-o-up"></i>
          </span>
          <span class="icon-desc">我收到的赞  <el-badge :hidden="this.GLOBAL.COUNT.admireCount === 0"
                                                   :value="this.GLOBAL.COUNT.admireCount" :max="99"
                                                   class="badge"/>
          </span>
        </div>
      </el-col>
      <el-col :span="24" @click="followDetails">
        <div class="row-wrapper" @click="followDetails">
          <span style="background-color: #418DFF" class="icon-wrapper">
            <i class="fa fa-users"></i>
          </span>
          <span class="icon-desc">好友关注  <el-badge :hidden="this.GLOBAL.COUNT.followCount === 0"
                                                  :value="this.GLOBAL.COUNT.followCount" :max="99"
                                                  class="badge"/>
          </span>
        </div>
      </el-col>
    </el-row>
  </el-container>
</template>

<script>
  export default {
    name: 'message',
    data () {
      return {}
    },
    created: function () {
    },
    methods: {
      goBack: function () {
        this.GLOBAL.showLoading()
        this.$router.push('/home')
      },
      admireDetails: function () {
        this.$router.push({
          name: 'm_admire',
          params: {
            label: '我收到的赞'
          }
        })
      },
      followDetails: function () {
        this.$router.push({
          name: 'm_follow',
          params: {
            label: '好友关注'
          }
        })
      },
      forwardDetails: function () {
        this.$router.push({
          name: 'm_forward',
          params: {
            label: '@我的动态'
          }
        })
      },
      commentDetails: function () {
        this.$router.push({
          name: 'm_comment',
          params: {
            label: '评 论'
          }
        })
      }

    }
  }
</script>

<style scoped>
  .el-header {
    padding: 0 !important;
    height: 2rem !important;
    margin-bottom: 0.6rem;
  }

  .el-header span {
    vertical-align: center;
    display: inline-block;
    color: rgba(43, 43, 43, 0.93);
    width: 80%;
    text-align: center;
    font-size: 1.0rem;
    line-height: 2rem;
    font-weight: 700;
  }

  .el-icon-back {
    position: relative;
    display: inline-block;
    width: 2rem;
    height: 1.2rem;
    border-radius: 4px;
    line-height: 1.2rem;
    text-align: center;
    margin-left-left: 2%;
    font-size: 1rem;
  }

  .el-icon-back:hover {
    background-color: lightgray;
  }

  .row-wrapper {
    margin: 0.4rem 0;
  }

  .badge {
    display: inline-block;
    float: right;
    line-height: 2rem;
  }

  .icon-wrapper {
    display: inline-block;
    height: 2rem;
    width: 2rem;
    text-align: center;
    line-height: 2rem;
    border-radius: 50%;
    font-size: 1rem;
    color: white;
    margin-left: 0.6rem;
  }

  .icon-desc {
    display: inline-block;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    font-weight: normal;
    font-size: 0.8rem;
    line-height: 2rem;
    width: 76%;
    margin-left: 0.6rem;
    border-bottom: 1px solid rgb(226, 226, 226);
  }
</style>
