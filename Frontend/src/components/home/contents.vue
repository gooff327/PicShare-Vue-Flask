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
      <div slot="title" class="commentTitle">
        <i @click="commentPanel=false" class="el-icon-back"></i>
        <span>&nbsp;&nbsp;评论</span>
      </div>
      <div v-if="this.comments.length === undefined || this.comments.length === 0" class="commentInfo">
        <h1 class="emptyContent" v-text="tips"></h1>
      </div>
      <div v-else v-for="comment in this.comments" class="commentInfo" :key="comment.cid">
        <img class="commentAvatars" :src="['data:Image/png;base64,'+comment.avatar]" alt="">
        <span class="commentUsername">{{comment.username}}: <span class="commentContent">{{comment.comments}}</span></span>
        <span class="commentDate">{{comment.datetime}}</span>

      </div>
      <div slot="footer" class="dialog-footer">
          <img class="commentAvatar" :src="['data:Image/png;base64,'+this.GLOBAL.USER.avatar]" alt="">
          <el-input class="inputComment" type="textarea" :autosize="{ minRows: 1, maxRows: 6 }" v-model="inputContent" placeholder="添加评论..."></el-input>
          <el-button class="submitBtn"  size="mini" type="primary"   @click="submit">发布</el-button>
  </div>
    </el-dialog>

    <el-dialog
      :visible.sync="updatePanel"
      :fullscreen="true"
      :show-close="false"
      width="100%">
      <div slot="title" class="updateTitle">
        <i @click="updatePanel=false" class="el-icon-back"></i>
        <span>&nbsp;&nbsp;新帖子</span>
      </div>
      <div class="image-uploader-box">
        <img v-if="imageUrl" :src="imageUrl" class="image">
        <i  v-else class="el-icon-plus image-uploader-icon"></i>
        <input style="opacity: 0" type="file" class="image-uploader">
      </div>
      <span slot="footer" class="dialog-footer">
    <el-button @click="updatePanel = false">取 消</el-button>
    <el-button type="primary" @click="updatePanel = false">确 定</el-button>
  </span>
    </el-dialog>

    <div class="footerbar">
      <el-button-group>
        <el-button size="small" class="function" :autofocus=true type="default" ><i class="fa fa-home"></i><p>主页</p></el-button>
        <el-button size="small" type="default" class="function"><i class="fa fa-handshake-o"></i><p>关注</p></el-button>
        <el-button size="small" class="plus" @click="updateEvent" type="default" ><i class="fa fa-plus-circle"></i></el-button>
        <el-button size="small" type="default" class="function" ><i class="fa fa-envelope"></i><p>消息</p> </el-button>
        <el-button size="small" type="default" class="function"><i class="fa fa-user-o"></i><p>我的</p> </el-button>
      </el-button-group>
    </div>
  </div>
</template>

<script>
    export default {
      data () {
        return {
          imageUrl: '',
          tips: '',
          updatePanel: false,
          emptyContent: true,
          inputContent: this.inputContent,
          commentPanel: false,
          activeName: '',
          passage: {},
          admire: {},
          comments: [],
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
          this.comments = []
          this.tips = '加载中...'
          this.commentPanel = true
          this.passage = passage
          let url = this.GLOBAL.BASE_URL + '/api/v1/comments'
          this.$axios.get(url, {
            params: {
                pid: `${this.passage.pid}`
            }
          }).then(function (response) {
            console.log(response)
            this.comments = response.data.reverse()
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
              document.body.scrollTo(0, 0)
             this.$message.success('评论成功！')
            }.bind(this))
          }
        },
        updateEvent: function () {
          this.updatePanel = true
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
  .emptyContent{
    display: block;
    text-align: center;
    width: 100;
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
    bottom: 0px;
    width: 100%;
    padding-top: 6px;
    text-align: left;
    height: 46px;
    background-color: rgba(255,255,255,0.8)
  }
  .commentAvatar{
    margin: 0;
    padding: 0;
    width: 33px;
    height: 33px;
    border-radius: 50%;
    float: left;
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
    top: -10px;
    margin: 0;
    margin-left: 0.8rem;
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
    top: -20px;
    right: -52px;
  }
  .commentAvatars{
    margin: 0;
    padding: 0;
    border-radius: 50%;
    float: left;
    width: 40px;
    height: 40px;
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
    position: fixed;
    width: 100%;
    bottom: 0;
    background-color: rgba(255,255,255,0.1);
  }
  .el-button-group{
    width: 100%;

  }
  .el-button{
    width: 20%;
    float: left;
    padding-left: 0;
    padding-right: 0;
    border: 0px;
    height: 46px;
  }
  .function .fa,.function.fa::before{
    font-size: 26px;
    padding: 0;
    margin: 0;
    position: relative;
    top: -6px;
    width: 100%;
  }
  .footerbar p {
    position: relative;
    font-size: smaller;
    top: -18px;
  }
  .plus .fa {
    padding: 0;
    font-size: 36px;
    position: relative;
    top: -4px;
    color: #34BE5B;
  }
  .image-uploader-box{
    width: 200px;
    height: 200px;
    border: 1px dashed  #d9d9d9;
  }
  .image-uploader{
    height: 100%;
    width: 100%;
    opacity: 0;
  }
  .image-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .image-uploader-box i {
    font-size: 100px;
    color: #8c939d;
    width: 200px;
    height: 200px;
    line-height: 200px;
    text-align: center;
  }
  .image {
    width: 200px;
    height: 200px;
    display: block;
  }
  .image-uploader-icon{

  }
  .moreInfo{
    margin-bottom: 60px;
  }
</style>
