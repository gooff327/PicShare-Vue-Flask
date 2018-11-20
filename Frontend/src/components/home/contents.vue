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
            <div class="imageDesc">{{key.desc}}</div>
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
    <comment ref="comment"></comment>
  </div>
</template>

<script>
  import comment from '../../components/Common/comment'
    export default {
      data () {
        return {
          updatePanel: false,
          emptyContent: true,
          refreshData: {},
          admire: {},
          moreInfoText: {
            1: '更多动态加载中...',
            2: '没有更多动态啦！',
            3: '你的网络好像出问题了...'
          }
        }
      },
      components: {
        'comment': comment
      },
      created: function () {
        this.getAdmireList()
      },
      methods: {
        getAdmireList: function () {
          var url = this.GLOBAL.BASE_URL + '/api/v1/admire'
          this.$axios.get(url).then(function (res) {
            console.log(res)
            if (res.data.code === 520) {
              this.admire = res.data.admire
            }
          }.bind(this))
        },
        likeEvent: function (pid) {
          this.admire[pid] === true ? this.admire[pid] = false : this.admire[pid] = true
          console.log(this.admire)
          let url = this.GLOBAL.BASE_URL + '/api/v1/admire'
          let data = JSON.stringify(this.admire)
          this.$axios.post(url, data, {headers: {'Content-Type': 'Application/json'}}).then(function (response) {
            console.log(response)
          })
        },
        commentEvent: function (object) {
          this.$refs.comment.commentEvent(object)
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
  .imageDesc{
    position: absolute;
    bottom: 0.5rem;
    color: white;
    background-color: rgba(0,0,0,0.4);
    width: 95%;
    text-align: center;
    max-height: 40%;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    font-size: 16px;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    padding-top: 0.1rem;
    padding-bottom: 0.1rem;
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
    width: 36px;
    height: 36px;
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
    position: relative;
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
  .fa-heart:hover{
    animation: admire 0.6s normal;
  }
  @keyframes admire {
    0% { transform: scale(1,1)}
    20% { transform: scale(2.4,2.4)}
    100% { transform: scale(1,1)}
  }
  .fa-heart-o:hover{
    transition: color 1.5s;
  }
  .item{
    border-radius: 10px;
    margin-top: 2px;
    margin-bottom: 2px;
  }
  .moreInfo{
    margin-bottom: 60px;
  }
</style>
