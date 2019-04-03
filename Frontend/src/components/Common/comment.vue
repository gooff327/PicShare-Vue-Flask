<template>
  <el-row>
    <el-col :span="24" class="commentTitle">
      <i @click="goBack" class="el-icon-back"></i>
      <span class="dialogTitle">评 论</span>
    </el-col>
    <el-col :span="24" v-if="this.comments.length === undefined || this.comments.length === 0" class="commentTips">
      <h3 class="emptyContent" v-text="tips"></h3>
    </el-col>
    <el-col :span="24" v-else v-for="comment in this.comments" class="commentInfo" :key="comment.cid">
      <el-col :span="3" class="avatarWrapper">
        <img class="commentAvatars" :src="comment.avatar" alt="">
      </el-col>
      <el-col :span="4">
        <span class="commentUsername">{{comment.username}} : </span>
      </el-col>
      <el-col :span="12">
        <span class="commentContent">{{comment.comments}}</span>
      </el-col>
      <el-col :span="4">
        <span v-text="comment.datetime" class="commentDatetime"></span>
      </el-col>
    </el-col>

    <div class="dialog-footer">
      <img class="commentAvatar" :src="this.GLOBAL.USER.avatar" alt="">
      <el-input class="inputComment" type="textarea" :autosize="{ minRows: 1, maxRows: 6 }" v-model="inputContent"
                placeholder="添 加 评 论 ..."></el-input>
      <el-button class="submitBtn" :disabled="!this.inputContent" size="mini" type="primary" @click="submit">评 论
      </el-button>
    </div>
  </el-row>
</template>

<script>
  export default {
    name: 'comment',
    data () {
      return {
        tips: '',
        commentPanel: false,
        inputContent: this.inputContent,
        comments: [],
        pid: ''
      }
    },
    created: function () {
      this.getComment(this.$route.params.pid)
    },
    methods: {
      goBack: function () {
        this.$router.back()
      },
      getComment: function (pid) {
        this.comments = []
        this.pid = pid
        console.log('pid', pid)
        this.tips = '加载中...'
        this.commentPanel = true
        let url = this.GLOBAL.BASE_URL + '/api/v1/comments'
        this.$axios.get(url, {
          params: {
            pid: `${pid}`
          }
        }).then(function (response) {
          console.log(response)
          this.comments = response.data
          if (this.comments.length === undefined || this.comments.length === 0) {
            this.tips = '当前还没有评论哦！'
          }
        }.bind(this))
      },
      submit: function () {
        let url = this.GLOBAL.BASE_URL + '/api/v1/comments'
        console.log(url)
        let data = {
          pid: `${this.pid}`,
          uid: `${this.GLOBAL.USER.uid}`,
          vid: `${this.$route.params['vid']}`,
          username: `${this.GLOBAL.USER.username}`,
          commit: `${this.inputContent}`
        }
        console.log(data)
        this.$axios.post(url, data).then(function (response) {
          if (response.data.tips === 'Successed!') {
            this.inputContent = ''
            this.getComment(this.pid)
          }
          this.$message({
            type: 'success',
            message: '评 论 成 功 ！',
            center: true,
            duration: 1000
          })
        }.bind(this))
      }
    }
  }
</script>

<style scoped>
  .commentTitle {
    position: fixed;
    line-height: 1.5rem;
    top: 0;
    width: 100%;
    text-align: center;
    background-color: white;
    z-index: 10;
  }

  .commentTitle i {
    display: inline-block;
    position: fixed;
    top: 1rem;
    left: 1.2rem;
    width: 8%;
    height: 8vw;
    line-height: 8vw;
    font-weight: bolder;
  }

  .dialogTitle {
    display: inline-block;
    font-weight: bold;
    line-height: 3rem;
  }

  .avatarWrapper {
    margin-right: 0.4rem;
  }

  .commentAvatar {
    display: inline-block;
    margin: 0;
    padding: 0;
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    float: left;
  }

  .commentTips {
    padding-top: 40vh;
    display: block;
    margin-bottom: 0.6rem;
    text-align: center;
    color: gray;
  }

  .commentInfo {
    display: block;
    position: relative;
    top: 3rem;
    padding-bottom: 0.5rem;
  }

  .commentUsername {
    display: inline-block;
    max-width: 100%;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    overflow: hidden;
    white-space: nowrap;
    font-size: 0.8rem;
    font-weight: 200;
    line-height: 2.4rem;
    text-overflow: ellipsis; /*超出部分用...代替*/
  }

  .commentContent {
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    font-weight: normal;
    display: inline-block;
    width: 90% !important;
    float: left !important;
    padding-top: 0.65rem;
    word-wrap: break-word;
    color: rgba(64, 64, 64, 0.9);
    font-size: 0.8rem;
  }

  .commentDatetime {
    margin-top: 0.82rem;
    font-size: 0.6rem;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid;
    border-radius: 0.3rem;
    line-height: 0.6rem;
    color: darkgray;
  }

  .commentAvatars {
    margin-right: 0.4rem;
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
  }

  .submitBtn {
    display: inline-block;
    position: fixed;
    bottom: 0.6rem;
    right: 1rem;
    height: 33px;
  }

  .inputComment {
    position: fixed;
    bottom: 0.6rem;
    width: 60%;
    padding: 0 0 0 0;
    margin: 0;
    display: inline-block;
    padding-right: 0.6rem;
    padding-left: 0.6rem;
  }

  .dialog-footer {
    position: fixed;
    bottom: 0px;
    width: 100%;
    padding-top: 0.5rem;
    padding-bottom: 0.4rem;
    text-align: left;
    height: 42px;
    background-color: rgba(255, 255, 255, 0.8)
  }
</style>
