<!--suppress ALL -->
<template>
  <div class="container">
  <div class="contentWrapper">
  <el-card shadow="hover" :body-style="{padding: '6px' }" class="item" v-for="(key,item) in contents" :key="item" :title="key.title" :name="key.id">
          <div class="headbar">
            <img class="avatar" :src="['data:Image/png;base64,'+key.uavatar]" alt="">
            <span class="username">{{key.author}}</span>
            <i class="el-icon-more-outline"></i>
          </div>
          <div class="contentImage">
            <img  class="innerPic" :src="['data:Image/png;base64,'+key.img]" :preview="key.pid" alt="">
          </div>
    <div class="bottom">
      <span class="bottomText">{{key.pv}} 次浏览</span>
      <span class="botttomIcon">
        <i style="color: #EE4957" @click="likeEvent(key.pid)" v-if="admire[key.pid] ===true" class="fa fa-heart"  aria-hidden="true"></i>
        <i @click="likeEvent(key.pid)" v-else class="fa fa-heart-o"  aria-hidden="true"></i>
        <i @click="commentEvent(key)" class="fa fa-comment-o" aria-hidden="true"></i>
        <i @click="shareEvent(key.pid)" class="fa fa-paper-plane-o" aria-hidden="true"></i>
      </span>
    </div>
  </el-card>
    <i class="el-icon-loading moreInfo"></i><span>{{moreInfoText["1"]}}</span>
  </div>
    <el-dialog
      :visible.sync="commentPanel"
      :fullscreen="true"
      :show-close="false">
      <div slot="title">
        <i @click="commentPanel=false" class="el-icon-back"></i>
        <span>&nbsp;&nbsp;评论</span>
      </div>
      <div slot="footer" class="dialog-footer">
          <img class="commentAvatar" :src="['data:Image/png;base64,'+this.GLOBAL.USER.avatar]" alt="">
          <el-input class="inputComment" type="textarea" :autosize="{ minRows: 1, maxRows: 6 }" v-model="inputContent" placeholder="添加评论..."></el-input>
          <el-button class="submitBtn"  size="mini" type="primary"   @click="submit">发布</el-button>
  </div>
    </el-dialog>
   <el-footer  class="footerbar"><h1>what!</h1></el-footer>
  </div>
</template>

<script>
    export default {
      data () {
        return {
          emptyContent: true,
          inputContent: this.inputContent,
          commentPanel: false,
          activeName: '',
          passage: {},
          admire: {},
          moreInfoText: {
            1: '更多动态加载中...',
            2: '没有更多动态啦！',
            3: '你的网络好像出问题了...'
          }
        }
      },
      created: function () {
        var url = this.GLOBAL.BASE_URL + '/api/v1/admire'
        this.$axios.get(url).then(function (res) {
          if (res.data.code === 520) {
            this.admire = res.data.admire
          }
        }.bind(this))
      },
      methods: {
        likeEvent: function (pid) {
          this.admire[pid] === true ? this.admire[pid] = false : this.admire[pid] = true
          console.log(this.admire)
          let url = this.GLOBAL.BASE_URL + '/api/v1/admire'
          let data = JSON.stringify(this.admire)
          this.$axios.post(url, data, {headers: {'Content-Type': 'Application/json'}}).then(function (response) {
            console.log(response)
          })
        },
        commentEvent: function (passage) {
          this.commentPanel = true
          this.passage = passage
          let url = this.GLOBAL.BASE_URL + '/api/v1/comments'
          this.$axios.get(url, {
            params: {
                pid: `${this.passage.pid}`
            }
          }).then(function (response) {
            console.log(response)
          })
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
              console.log(response)
            })
          }
        }
      },
      props: {
        contents: {
          type: Object
        }
      },
        name: 'contents'
    }
</script>
<style scoped>
  .headbar{
    display: inline-block;
    vertical-align: top;
    height: 20%;
    font-size: 20%;
    padding-bottom: 0.2rem;
    width: 100%;
    float: left;
  }
  .username{
    display: inline-block;
    max-width: 70%;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    font-size: 0.8rem;
    padding-top: 0.8rem;
    padding-left: 0.4rem;
  }
  .avatar{
    width: 10%;
    height: 10%;
    border-radius: 50%;
    float: left;
  }
  .el-icon-more-outline{
    display: inline-block;
    height: 20%;
    float: right;
    padding-top: 4%;
    padding-right: 6%;
  }
  .bottomText{
    font-size: 0.8rem;
    color: gray;
    margin: 0;
    padding: 0;
  }
  .botttom{
    vertical-align: top;
  }
  .botttomIcon{
    display: inline-block;
    float: right;
    padding-right: 0.4rem;
    margin-bottom: 0.4rem;
  }
  .fa{
    padding-right: 0.4rem;
    padding-left: 0.4rem;
    padding-bottom: 0.4rem;
  }
  .contentImage{
    margin-top: 0.2rem;
    max-width: 100%;
    max-height: 50%;
    padding-bottom: 0.2rem;
  }
  .innerPic{
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
    border-radius: 4px;
  }
  .item{
    border-radius: 10px;
    margin-top: 2px;
    margin-bottom: 2px;
  }
  .dialog-footer{
    position: fixed;
    bottom: 10px;
    width: 100%;
    text-align: left;
  }
  .commentAvatar{
    margin: 0;
    padding: 0;
    width: 33px;
    height: 33px;
    border-radius: 50%;
    float: left;
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
  .footerbar{
    height: 20%;
    display: block;
    position: fixed;
    bottom: 0px;
    color: black;
    background: rgba(255,250,250);
    width: 100%;
  }
  .moreInfo{
    margin-bottom: 60px;
  }
</style>
