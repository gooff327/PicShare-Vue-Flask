<template>
  <el-dialog
    :visible.sync="commentPanel"
    :fullscreen="true"
    :show-close="false">
    <div slot="title" class="commentTitle">
      <i @click="commentPanel=false" class="el-icon-back"></i>
      <span class="dialogTitle">评 论</span>
    </div>
    <div v-if="this.comments.length === undefined || this.comments.length === 0" class="commentTips">
      <h1 class="emptyContent" v-text="tips"></h1>
    </div>
    <div v-else v-for="comment in this.comments" class="commentInfo" :key="comment.cid">
      <img class="commentAvatars" :src="['data:Image/png;base64,'+comment.avatar]" alt="">
      <span class="commentUsername">{{comment.username}} : <span class="commentContent">{{comment.comments}}</span></span>
      <span class="commentDate">{{comment.datetime}}</span>
    </div>
    <div slot="footer" class="dialog-footer">
      <img class="commentAvatar" :src="['data:Image/png;base64,'+this.GLOBAL.USER.avatar]" alt="">
      <el-input class="inputComment" type="textarea" :autosize="{ minRows: 1, maxRows: 6 }" v-model="inputContent" placeholder="添 加 评 论 ..."></el-input>
      <el-button class="submitBtn" :disabled="!this.inputContent"  size="mini" type="primary"   @click="submit">评 论</el-button>
    </div>
  </el-dialog>
</template>

<script>
    export default {
        name: 'comment',
      data () {
          return {
            tips: '',
            commentPanel: false,
            inputContent: this.inputContent,
            comments: []
          }
      },
      methods: {
        commentEvent: function (passage) {
          this.comments = []
          this.tips = '加载中...'
          this.commentPanel = true
          let url = this.GLOBAL.BASE_URL + '/api/v1/comments'
          this.$axios.get(url, {
            params: {
              pid: `${passage.pid}`
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
          if (this.inputContent === '' || this.inputContent === undefined) {
            this.$message.error('不能提交空内容')
          } else {
            let url = this.GLOBAL.BASE_URL + '/api/v1/comments'
            this.$axios.post(url, {
              pid: `${this.passage.pid}`,
              uid: `${this.GLOBAL.USER.uid}`,
              username: `${this.GLOBAL.USER.username}`,
              commit: `${this.inputContent}`
            }).then(function (response) {
              if (response.data.tips === 'Successed!') {
                this.inputContent = ''
                let url = this.GLOBAL.BASE_URL + '/api/v1/comments'
                this.$axios.get(url, {
                  params: {
                    pid: `${this.passage.pid}`
                  }
                }).then(function (response) {
                  console.log(response)
                  this.comments = response.data.reverse()
                }.bind(this))
              }
              this.$message({
                type: 'success',
                message: '评 论 成 功 ！',
                center: true,
                duration: 1000})
            }.bind(this))
          }
        }
      }
    }
</script>

<style scoped>
  .commentTitle{
    position: fixed;
    line-height: 50px;
    top: 0;
    width: 100%;
    background-color: rgba(255,255,255,0.4);
  }
  .commentTitle i{
    position: relative;
    left: 20px;
    font-size: larger;
    font-weight: bolder;
  }
  .dialogTitle{
    width: 88%;
    display: inline-block;
    font-weight: normal;
    text-align: center;
  }
  .commentAvatar{
    margin: 0;
    padding: 0;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    float: left;
  }
  .commentTips{
    display: block;
    margin-bottom: 0.6rem;
    text-align: center;
  }
  .commentInfo{
    display: block;
    margin-bottom: 0.6rem;
  }
  .commentUsername{
    line-height: 40px;
    width: 80%;
    font-size: 1rem;
    font-weight: bold;
    position: relative;
    left: 10px;
    top: -10px;
  }
  .commentContent{
    font-size: 1rem;
    font-weight: normal;
  }
  .commentDate{
    display: inline-block;
    text-align: left;
    font-size: 0.4rem;
    font-weight: lighter;
    color: gray;
    width: 80%;
    position: relative;
    left: 50px;
    top: -20px;
  }
  .commentAvatars{
    margin: 0;
    padding: 0;
    border-radius: 50%;
    float: left;
    width: 42px;
    height: 42px;
  }
  .submitBtn{
    display: inline-block;
    height: 33px;
  }
  .inputComment{
    width: 60%;
    padding: 0 0 0 0;
    margin: 0;
    display: inline-block;
    padding-right: 0.6rem;
    padding-left: 0.6rem;
  }
  .dialog-footer{
    position: fixed;
    bottom: 0px;
    width: 100%;
    padding-top: 6px;
    text-align: left;
    height: 42px;
    background-color: rgba(255,255,255,0.8)
  }
</style>
