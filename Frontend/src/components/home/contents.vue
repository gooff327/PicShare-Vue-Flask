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
    <span class="bottomText">{{key.pv}} 次浏览</span>
    <div class="bottomIcon">
      <i style="color: #EE4957" @click="likeEvent(key.pid)" v-if="admire[key.pid] ===true" class="fa fa-heart"  aria-hidden="true"></i>
      <i @click="likeEvent(key.pid)" v-else class="fa fa-heart-o"  aria-hidden="true"></i>
      <i @click="commentEvent(key.pid)" class="fa fa-comment-o" aria-hidden="true"></i>
      <i @click="shareEvent(key.pid)" class="fa fa-paper-plane-o" aria-hidden="true"></i>
    </div>
  </el-card>
    <i class="el-icon-loading moreInfo"></i><span>{{moreInfoText["1"]}}</span>
  </div>
   <el-footer  class="footerbar"><h1>what!</h1></el-footer>
  </div>
</template>

<script>
    export default {
      data () {
        return {
          activeName: '',
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
    display: inline-block;
    margin: 0;
    padding: 0;
    margin-bottom: 0.2rem;
    padding-left: 0.2rem;
  }
  .botttomIcon{
    display: inline-block;
  }
  .fa{
    padding-left: 0.2rem;
    padding-bottom: 0.4rem;
  }
  .contentImag,img{
    margin-top: 2%;
    border-radius: 4px;
  }
  .contentWrapper{

  }
  .item{
    border-radius: 10px;
    margin-top: 2px;
    margin-bottom: 2px;
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
