<template>
  <div class="footerbar">
    <el-button-group class="buttonWrapper">
      <div>
      <el-button size="small" type="default" class="function homeBtn" @click="showHomePanel"><i class="fa fa-home"></i>
        <p>主 页</p></el-button>
      </div>
      <div>
      <el-button size="small" type="default" class="function" @click="showFollowingProduces"><i
        class="fa fa-handshake-o"></i>
        <p>关 注</p></el-button>
      </div>
      <div>
      <el-button size="small" type="default" class="plus" onclick="document.getElementById('image-uploader').click();">
        <i class="fa fa-plus-circle"></i></el-button>
      </div>
      <div>
      <el-button size="small" type="default" @click="showMessage" class="function">
        <el-badge :hidden="this.sumValue <= 0" :value="this.sumValue" :max="99" class="item">
          <i class="fa fa-envelope"></i>
        </el-badge>
        <p>消 息</p></el-button>
      </div>
      <div>
      <el-button size="small" type="default" @click="showPersonalData" class="function"><i class="fa fa-user-o"></i>
        <p>我 的</p></el-button>
      <input id="image-uploader" class="image-uploader" type="file" @change="updateEvent($event)">
      </div>
    </el-button-group>
  </div>
</template>
<script>
  export default {
    name: 'bottom',
    data () {
      return {
        newButtonBool: {},
        sumValue: '',
        requestList: {},
        returnReqContent: {}
      }
    },
    created: function () {
      this.getMessage()
    },
    methods: {
      updateEvent: function (event) {
        var file = event.target.files[0]
        if (file) {
          const isJPG = file.type === 'image/jpeg'
          const isLt8M = file.size / 1024 / 1024 < 8
          if (!isJPG) {
            this.$message.error('只能上传 JPG 格式!')
          }
          if (!isLt8M) {
            this.$message.error('大小不能超过 8MB!')
          }
          if (isJPG && isLt8M) {
            this.GLOBAL.UPLOAD_FILE = file
            this.$router.push('/create/details')
          }
        }
      },
      getMessage: function () {
        let url = this.GLOBAL.BASE_URL + '/api/v1/get/messages'
        this.$axios.get(url).then(function (response) {
          this.GLOBAL.MESSAGES = response.data['messages']
          this.GLOBAL.COUNT = this.GLOBAL.initMessage(this.GLOBAL.MESSAGES)
          this.sumValue = this.GLOBAL.COUNT.sum
          this.getUserAndPassage(this.GLOBAL.reqList)
          this.returnReqUsersAndPassages(this.requestList)
        }.bind(this))
      },

      returnReqUsersAndPassages: function (reqList) {
        let url = this.GLOBAL.BASE_URL + '/api/v1/messages/query'
        this.$axios.post(url, reqList).then(function (response) {
          this.GLOBAL.MESSAGES_CONTENT = response.data
        }.bind(this))
      },

      getUserAndPassage: function (reqList) {
        this.requestList['users'] = Array.from(new Set(reqList.users))
        this.requestList['passages'] = Array.from(new Set(reqList.passages))
      },
      showFollowingProduces: function () {
        if (this.$route.name !== 'following') {
          this.GLOBAL.showLoading({text: '好友动态加载中', lock: true})
          this.$router.push('/following')
        }
      },
      showHomePanel: function () {
        if (this.$route.name !== 'home') {
          this.GLOBAL.showLoading({text: '主页刷新中', lock: true})
          this.$router.push('/home')
        }
      },
      showMessage: function () {
        this.$router.push('/message')
        this.getMessage()
      },
      showPersonalData: function () {
        if (this.$route.name !== 'user') {
          this.GLOBAL.showLoading({text: '个人信息装填中', lock: true})
          this.$router.push(`/user/${this.GLOBAL.USER.username}`)
        }
      }
    },
    props: {
      selected: {
        type: String
      }
    }
  }
</script>

<style scoped>
  .footerbar {
    padding-top: 0.1rem;
    width: 100vw;
    position: fixed;
    bottom: 0;
    left: 0;
    background-color: rgb(255, 255, 255);
    z-index: 3;
  }

  .buttonWrapper{
    display: flex;
    justify-content: space-around;
    align-items: center;
    height: 10%;
  }
  /*.buttonWrapper {*/
    /*width: 100vw;*/
    /*background-color: rgb(255, 255, 255);*/
  /*}*/

  .el-button:hover span{
    color: #606266;
  }

  .function {
    border: 0px;
    padding: 0;
  }

  .function .fa, .function.fa::before {
    font-size: 26px;
    padding: 0;
    margin: 0;
  }

  .footerbar p {
    font-size: smaller;
    margin-top: 4px;
    margin-bottom: 2px;
  }

  .plus {
    height: 46px;
    border: 0px;
  }

  .plus .fa {
    padding: 0;
    font-size: 36px;
    position: relative;
    top: -4px;
    color: #34BE5B;
  }

  .image-uploader {
    height: 100%;
    width: 100%;
    display: none;
  }
</style>
