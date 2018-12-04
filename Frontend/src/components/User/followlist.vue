<template>
  <el-container>
    <el-header>
      <i @click="goBack" class="el-icon-back"></i>
      <span v-text="isFollowers?'关注':'粉丝'"></span>
    </el-header>
    <el-input
      :placeholder="isFollowers?'搜索你关注的用户...':'搜索粉丝...'"
      prefix-icon="el-icon-search" v-model="searchContent"></el-input>
    <div userBox>
      <ul v-for="(item,key) in userList" :key="key">
        <li class="userList">
          <el-row>
            <el-col :offset="1" :span="4"><img class="smallPic" :src="['data:Image/png;base64,'+item.avatar]"></el-col>
            <el-col :span="14"><span class="usernameWrapper" v-text="item.username"></span><span class="briefWrapper" v-text="item.brief"></span></el-col>
            <el-col :span="4">
              <el-button :round="true" size="mini" v-if="isConcerned(item.uid)" type="default">取关</el-button>
              <el-button size="mini" :round="true" v-else type="primary">关注</el-button>
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
        userList: {}
      }
    },
    created: function () {
      if (this.$route.name === 'followers') {
        this.isFollowers = false
        this.initFollowers()
      } else if (this.$route.name === 'following') {
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
        this.getUserlist('following')
      },
      getUserlist: function (type) {
        let uid = this.$route.query.uid
        console.log(uid)
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
      isConcerned: function (vid) {
        return this.GLOBAL.USER.following[vid]
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
    height: 30px !important;
  }

  .el-header span {
    vertical-align: center;
    display: inline-block;
    color: rgba(43, 43, 43, 0.93);
    width: 90%;
    text-align: center;
    font-size: 1.0rem;
  }

  .el-icon-back {
    position: relative;
    width: 6%;
    line-height: 100%;
    padding-left: 1%;
    font-size: 1rem;
  }

  .userList {
    margin-top: 1rem;
    display: block;
    line-height: 60px;
  }

  .userList img {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    vertical-align: top;
  }

  ul {
    padding: 0;
    margin: 0;
  }

  .userList div {
    line-height: 40px !important;
  }
  .usernameWrapper,.briefWrapper{
    display: block;
    width: 100%;
    line-height: 14px;
    font-size: 0.4rem;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  }
  .usernameWrapper{
    margin-top: 10px;
  }
  .briefWrapper{
    color: #606266;
  }
</style>
