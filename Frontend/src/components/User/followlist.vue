<template>
  <el-container>
    <el-header>
      <i @click="goBack" class="el-icon-back"></i>
      <span v-text="isFollowers?'关 注':'粉 丝'"></span>
    </el-header>
    <div userBox>
      <ul v-for="(item,key) in userList" :key="key">
        <li class="userList">
          <el-row>
            <el-col :offset="1" :span="4"><img @click="showUserDetails(item.username)" class="smallPic"
                                               :src="item.avatar">
                                               <!--:src="['data:Image/png;base64,'+item.avatar]">-->
            </el-col>
            <el-col :span="14"><span class="usernameWrapper" v-text="item.username"></span>
            </el-col>
            <el-col :span="4">
              <el-button :disabled="isSelf(item.uid)" :autofocus="false" :round="false" size="mini"
                         v-if="isConcerned(item.uid)" type="default"
                         @click="concernAction(item.uid)">取 关
              </el-button>
              <el-button :disabled="isSelf(item.uid)" :autofocus="false" size="mini" :round="false" v-else type="primary"
                         @click="concernAction(item.uid)">关 注
              </el-button>
            </el-col>
          </el-row>
        </li>
      </ul>
    </div>
  </el-container>
</template>

<script>
  export default {
    name: 'followlist',
    data () {
      return {
        searchContent: '',
        isFollowers: true,
        userList: []
      }
    },
    created: function () {
      if (this.$route.name === 'followers') {
        this.isFollowers = false
        this.initFollowers()
      } else if (this.$route.name === 'followings') {
        this.isFollowers = true
        this.initFollowing()
      }
    },
    methods: {
      goBack: function () {
        this.$router.back()
      },
      initFollowers: function () {
        this.getUserlist('followers')
      },
      initFollowing: function () {
        this.getUserlist('followings')
      },
      getUserlist: function (type) {
        let uid = this.$route.query.uid
        let url = this.GLOBAL.BASE_URL + '/api/v1/get/users'
        this.$axios.get(url, {
          params: {
            uid: uid,
            type: type
          }
        }).then(function (response) {
          this.userList = response.data.userList
        }.bind(this))
      },
      isSelf: function (uid) {
        if (uid === this.GLOBAL.USER.uid) {
          return true
        } else {
          return false
        }
      },
      showUserDetails: function (username) {
        this.$router.push(`/user/${username}`)
      },
      isConcerned: function (vid) {
        return this.GLOBAL.USER.following[vid]
      },
      concernAction: function (vid) {
        this.GLOBAL.USER.following[vid] = !this.GLOBAL.USER.following[vid]
        let url = this.GLOBAL.BASE_URL + '/api/v1/concern/action'
        let data = new FormData()
        data.append('vid', vid)
        data.append('status', this.GLOBAL.USER.following[vid])
        this.$axios.post(url, data).then(function (response) {
          if (response.data.tips !== 'Successed!') {
            this.$message.error('操作不成功！')
          } else {
            this.getUserlist(this.$route.name)
          }
        }.bind(this))
      }
    }
  }
</script>

<style scoped>
  .el-header {
    padding: 0;
    margin-top: 10px;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px gainsboro solid;
    height: 2rem !important;
  }

  .el-header span {
    vertical-align: center;
    display: inline-block;
    color: rgba(43, 43, 43, 0.93);
    width: 86%;
    text-align: center;
    font-size: 1.0rem;
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

  .userList {
    margin-top: 1rem;
    display: block;
    line-height: 2.6rem;
  }

  .userList img {
    width: 2.6rem;
    height: 2.6rem;
    border-radius: 50%;
    vertical-align: top;
  }

  ul {
    padding: 0;
    margin: 0;
  }

  .userList div {
    line-height: 2rem !important;
  }

  .usernameWrapper {
    font-size: 0.9rem;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    line-height: 2.6rem;
    margin-left: 0.6rem;
  }

  .usernameWrapper {
  }

</style>
