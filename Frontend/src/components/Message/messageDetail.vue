<template>
  <el-container class="wrapper">
    <el-header>
      <i @click="goBack" class="el-icon-back"></i>
      <span v-text="this.$route.params['label']"></span>
    </el-header>
    <el-row class="contentWrapper">
      <el-card shadow="hover" class="messageCard"
               v-for="(key,item) in messageType[this.$route.name]" :key="item">
        <section class="top">
          <div class="avatarWrapper">
            <img @click="showUserDetails(users[key.uid]['username'])"
                 :src="users[key.uid]['avatar']" alt="">
          </div>
          <div class="nameWrapper">
            <span @click="showUserDetails(users[key.uid]['username'])" class="username">{{users[key.uid]['username']}}&nbsp;</span>
            <span>
            {{key['m_content']}}
          </span>
          </div>
        </section>
        <section @click="contentDetail(key,passages[key.pid],me.username)" v-if="key['m_type']!== 3"
                 class="contentCenter">
          <div class="descWrapper">
            <span @click="showUserDetails(me['username'])" class="username">&nbsp; @{{me.username}}</span>
            <span>
            <b>: {{passages[key.pid]['desc']}}</b>
          </span>
          </div>
          <div class="imgWrapper">
            <img :src="passages[key.pid]['img']" :preview=key.pid alt="">
          </div>
        </section>
      </el-card>
    </el-row>
  </el-container>
</template>

<script>

  export default {
    data () {
      return {
        users: this.GLOBAL.MESSAGES_CONTENT['users'],
        passages: this.GLOBAL.MESSAGES_CONTENT['passages'],
        me: this.GLOBAL.USER,
        messageType: {
          m_admire: this.GLOBAL.MESSAGES['admire_messages'],
          m_forward: this.GLOBAL.MESSAGES['forward_messages'],
          m_follow: this.GLOBAL.MESSAGES['follow_messages'],
          m_comment: this.GLOBAL.MESSAGES['comment_messages']
        }
      }
    },
    name: 'messageDetail',
    created: function () {
      this.changeMessageStatus(`${this.$route.name.slice(2)}Count`, this.messageType[`${this.$route.name}`])
    },
    methods: {
      goBack: function () {
        this.$router.push('/message')
      },
      contentDetail: function (key, passage, username) {
        switch (key['m_type']) {
          case 3:
            break
          default:
            this.$router.push({name: 'content', params: {pid: passage.pid, passage: passage, username: username}})
        }
      },
      showUserDetails: function (username) {
        this.$router.push(`/user/${username}`)
      },
      changeMessageStatus: function (countType, messages) {
        let readList = []
        for (let ele in messages) {
          if (messages[ele]['m_status']) {
            readList.push(messages[ele].mid)
          }
        }
        if (readList) {
          let url = this.GLOBAL.BASE_URL + '/api/v1/put/message/status'
          this.$axios.put(url, readList).then(() => {
            this.GLOBAL.COUNT[countType] = 0
          })
        }
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
    vvertical-align: center;
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

  .el-card {
    margin-bottom: 2px;
  }

  .avatarWrapper {
    float: left;
    display: inline-block;
    width: 15%;
    height: 1.8rem;
  }

  .avatarWrapper img {
    display: inline-block;
    width: 1.8rem;
    height: 1.8rem;
    border-radius: 50%;
    float: left;
  }

  .nameWrapper {
    display: inline-block;
    width: 85%;
    height: 1.8rem;
    text-overflow: ellipsis;
  }

  .nameWrapper span {
    font-size: 0.8rem;
    height: auto;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  }

  .contentCenter {
    display: block;
    width: 100%;
    margin-top: 0.6rem;
    background-color: rgba(132, 131, 130, 0.15);
    border-radius: 4px;
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
    margin-top: 0.2rem;
  }

  .username {
    color: darkcyan;
    opacity: 0.6;
  }

  .username:hover {
    opacity: 1;
  }
</style>
