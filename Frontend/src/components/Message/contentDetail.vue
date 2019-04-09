<template>
  <el-container>
    <el-header>
      <i @click="goBack" class="el-icon-back"></i>
      <span>详 情</span>
    </el-header>
    <el-row>
      <section class="content">
        <div class="descWrapper">
          <span @click="showUserDetails(this.passage['username'])"
                class="username">&nbsp;&nbsp;&nbsp;{{this.username}}:</span>
          <span>
            <b>{{this.passage['desc']}}</b>
          </span>
        </div>
        <div class="imgWrapper">
          <img :src="this.passage['img']" :preview=this.passage.pid alt="">
        </div>
      </section>
      <section class="comment" v-loading="loading">
        <el-card class="commentCard" v-for="(key,item) in comments" :key="item">
          <el-row class="top">
            <div class="avatarWrapper">
              <img @click="showUserDetails(key['username'])" :src="key.avatar" alt="">
            </div>
            <div class="usernameWrapper">
              <span @click="showUserDetails(key['username'])">{{key.username}} ：</span>
            </div>
            <div class="dateWrapper">
              <span class="datetime" v-text="key.datetime"></span>
            </div>
          </el-row>
          <el-row class="bottom">
            <div class="commentWrapper">
              <span v-text="key.comments"></span>
            </div>
          </el-row>
        </el-card>
      </section>
      <section class="footer">
        <img class="commentAvatar" :src="this.GLOBAL.USER.avatar" alt="">
        <el-input class="inputComment" type="textarea" :autosize="{ minRows: 1, maxRows: 6 }" v-model="inputContent"
                  placeholder="添 加 评 论 ..."></el-input>
        <el-button class="submitBtn" :disabled="!this.inputContent" size="mini" type="primary" @click="submit">评 论
        </el-button>
      </section>
    </el-row>
  </el-container>
</template>

<script>
  export default {
    name: 'contentDetail',
    data () {
      return {
        passage: this.$route.params['passage'],
        username: this.$route.params['username'],
        loading: true,
        comments: [],
        inputContent: ''
      }
    },
    created: function () {
      this.getComment()
    },
    methods: {
      goBack: function () {
        this.$router.back()
      },
      showUserDetails: function (username) {
        this.$router.push(`/user/${username}`)
      },
      getComment: function () {
        let url = this.GLOBAL.BASE_URL + '/api/v1/comments'
        this.$axios.get(url, {
          params: {
            pid: `${this.passage.pid}`
          }
        }).then(function (response) {
          this.comments = response.data
          this.loading = false
        }.bind(this))
      },
      submit: function () {
        let url = this.GLOBAL.BASE_URL + '/api/v1/comments'
        let data = {
          pid: `${this.passage.pid}`,
          uid: `${this.GLOBAL.USER.uid}`,
          vid: `${this.passage['uid']}`,
          username: `${this.GLOBAL.USER.username}`,
          commit: `${this.inputContent}`
        }
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
  .el-header {
    padding: 0 !important;
    margin: 0 !important;
    height: 2rem !important;
    margin-bottom: 1rem;
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
    margin-left: 2%;
    font-size: 1rem;
  }

  .el-icon-back:hover {
    background-color: rgba(129, 129, 129, 0.2);
  }

  .content {
    display: block;
    width: 100%;
    margin-top: 0.6rem;
    background-color: rgba(132, 131, 130, 0.15);
    border-radius: 4px;
  }

  .comment {
    padding-bottom: 2.6rem;

  }

  .descWrapper span {
    font-size: 0.78rem;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  }

  .imgWrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 0.2rem;
    padding-bottom: 0.4rem;
  }

  .imgWrapper img {
    flex: 1;
    max-width: 94%;
    width: 94%;
    height: 52.875%;
    border-radius: 4px;
    object-fit: fill;
  }

  .username {
    color: darkcyan;
    opacity: 0.6;
  }

  .username:hover {
    opacity: 1;
  }

  .top, .bottom {
    width: 100%;
    font-size: 0.8rem;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  }

  .commentCard {
    margin-bottom: 4px;
    padding: 0px;
  }

  .dateWrapper {
    float: right;
    line-height: 2rem;
    display: inline-block;
    margin-right: 0.4rem;

  }

  .avatarWrapper, .usernameWrapper {
    display: inline-block;
    float: left;
    line-height: 2rem;
    margin-left: 0.4rem;
  }

  .avatarWrapper img {
    width: 10vw;
    height: 10vw;
    border-radius: 50%;
  }

  .commentWrapper {
    width: 100%;
    line-height: 2rem;
    background-color: rgba(129, 129, 129, 0.2);
    border-radius: 4px;
  }

  .commentWrapper span {
    display: inline-block;
    padding-left: 5%;
    padding-right: 5%;
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

  .submitBtn {
    display: inline-block;
    position: fixed;
    bottom: 0.6rem;
    right: 1rem;
    height: 1.6rem;
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

  .footer {
    position: fixed;
    bottom: 0px;
    width: 100%;
    padding-top: 0.5rem;
    padding-bottom: 0.4rem;
    text-align: left;
    height: 2rem;
    background-color: rgba(255, 255, 255, 0.8)
  }
</style>
