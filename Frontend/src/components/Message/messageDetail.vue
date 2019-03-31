<template>
  <el-container>
    <el-header>
      <i @click="goBack" class="el-icon-back"></i>
      <span v-text="this.$route.params.label"></span>
    </el-header>
    <el-card shadow="hover" class="messageCard" v-for="(key,item) in admireMessages" :key="item">
      <section class="top">
        <div class="avatarWrapper">
          <img @click="showUserDetails(users[key.uid]['username'])"
               :src="['data:Image/png;base64,'+ users[key.uid]['avatar']]" alt="">
        </div>
        <div class="nameWrapper">
          <span @click="showUserDetails(users[key.uid]['username'])" class="username">&nbsp;{{users[key.uid]['username']}}&nbsp;</span>
          <span>
            觉得很赞
          </span>
        </div>
      </section>
      <section class="contentCenter">
        <div class="descWrapper">
          <span @click="showUserDetails(me['username'])" class="username">&nbsp;{{me.username}}</span>
          <span>
            <b>: {{passages[key.pid]['desc']}}</b>
          </span>
        </div>
        <div class="imgWrapper">
          <img :src="['data:Image/png;base64,'+ passages[key.pid]['img']]" :preview=key.pid alt="">
        </div>
      </section>
    </el-card>
  </el-container>
</template>

<script>

  export default {
    data () {
      return {
        users: this.GLOBAL.MESSAGES_CONTENT['users'],
        passages: this.GLOBAL.MESSAGES_CONTENT['passages'],
        admireMessages: this.GLOBAL.MESSAGES['admire_messages'],
        me: this.GLOBAL.USER

      }
    },
    name: 'messageDetail',
    created: function () {
      this.changeMessageStatus(this.GLOBAL.MESSAGES[`${this.$route.name.slice(2)}_messages`])
      this.GLOBAL.COUNT = this.GLOBAL.initMessage(this.GLOBAL.MESSAGES)
      console.log('$store', this.$store.state.loading)
    },
    methods: {
      goBack: function () {
        this.$router.back()
      },
      showUserDetails: function (username) {
        this.$router.push(`/user/${username}`)
      },
      changeMessageStatus: function (totlaMessages) {
        let readList = []
        for (let i in totlaMessages) {
          if (totlaMessages[i]['m_status']) {
            totlaMessages[i]['m_status'] = false
            readList.push(totlaMessages[i]['mid'])
          }
        }
        if (readList) {
          let url = this.GLOBAL.BASE_URL + '/api/v1/put/message/status'
          this.$axios.put(url, readList).then(response => {
            console.log(response)
          })
        }
      }
    }
  }
</script>

<style scoped>
  .el-header {
    padding: 0 !important;
    margin: 0 !important;
    height: 2rem !important;
  }

  .el-header span {
    vvertical-align: center;
    display: inline-block;
    color: rgba(43, 43, 43, 0.93);
    width: 86%;
    text-align: center;
    font-size: 1.0rem;
    line-height: 2rem;
    font-weight: 700;
  }

  .el-icon-back {
    position: relative;
    width: 6%;
    line-height: 100%;
    padding-left: 1%;
    font-size: 1rem;
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
    max-width: 96%;
    border-radius: 4px;
  }

  .username {
    color: darkcyan;
    opacity: 0.6;
  }

  .username:hover {
    opacity: 1;
  }
</style>
