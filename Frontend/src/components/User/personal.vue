<!--suppress ALL -->
<template>
  <el-container>
    <el-header>
      <span v-if="isSelf" class="fa fa-cog"></span>
      <span v-else class="el-icon-back" @click="back"></span>
      <span class="headTitle">个 人 主 页</span>
      <span class="fa fa-user-plus"></span>
    </el-header>
    <el-main>
      <transition name="fadein">
        <el-row v-show="topBody" v-cloak :gutter="20">
          <el-col :span="6">
            <div class="content-left">
              <img class="user-avatar" :src="['data:Image/jpg;base64,'+this.currentUser.avatar]" alt="">
            </div>
          </el-col>
          <el-col :span="18">
            <div class="content-right">
              <span class="user-username" v-text="this.currentUser.username"></span>
              <el-button v-show="isSelf" class="edit-btn" @click="editorVisible" size="mini">编辑主页</el-button>
              <el-button v-show="!isSelf" v-if="this.btnConcern" class="concern-btn" size="mini" @click="concernAction">
                取消关注
              </el-button>
              <el-button v-show="!isSelf" v-else class="concern-btn" size="mini" @click="concernAction">关 注</el-button>
              <el-dialog
                :visible.sync="editSelfPanel"
                :show-close="false"
                :fullscreen="true"
                width="100%">
                <div slot="title" class="commentTitle">
                  <i @click="editSelfPanel=false" class="el-icon-back"></i>
                  <span class="dialogTitle">编 辑 主 页</span>
                </div>
                <div class="edit-avatar">
              <span><img v-if="imageURL === ''||imageURL === undefined" class="avatar-preview"
                         :src="['data:Image/png;base64,'+this.GLOBAL.USER.avatar]" alt="">
              <img v-else class="avatar-preview" :src=imageURL alt=""></span>
                  <p onclick="document.getElementById('avatar-choose').click();">更换头像</p>
                  <input id="avatar-choose" class="avatar-choose" type="file" @change="avatarChoosed($event)">
                </div>
                <div class="informations">
                  <span>ID</span>
                  <el-input :disabled="true" v-model="this.GLOBAL.USER.uid"></el-input>
                  <span>用户名</span>
                  <el-input :disabled="true" v-model="username"></el-input>
                  <span>个人简介</span>
                  <el-input v-model="brief"></el-input>
                  <span>手机</span>
                  <el-input v-model="phone"></el-input>
                  <span>邮箱</span>
                  <el-input :disabled="true" v-model="email"></el-input>
                  <span>性别</span>
                  <el-select v-model="value" :placeholder="sex">
                    <el-option v-for="item in options"
                               :key="item.value"
                               :label="item.label"
                               :value="item.value"></el-option>
                  </el-select>
                  <br><br>
                  <el-button type="primary" class="submitChange" @click="submitChange"
                             :disabled="this.imageURL === '' &&this.imageURL !== undefined&& this.username === this.GLOBAL.USER.username && this.email === this.GLOBAL.USER.email && this.brief === this.GLOBAL.USER.brief && this.phone === this.GLOBAL.USER.phone && this.value === this.GLOBAL.USER.sex">
                    提 交
                  </el-button>
                </div>
              </el-dialog>
            </div>
          </el-col>
        </el-row>
      </transition>
      <middle-content @refresh="refresh" @loadData="loadData" @closeTop="closeTop" :uid="this.currentUser.uid"
                      :amounts="amounts"
                      :contents="contents"></middle-content>
    </el-main>
    <transition name="fadein">
      <nav-bottom v-show="topBody"></nav-bottom>
    </transition>
  </el-container>
</template>
<script>
  import navBottom from '../bottom/bottom'
  import middle from '../User/middle'
  import $ from 'jquery'

  export default {
    name: 'personal',
    components: {
      'navBottom': navBottom,
      'middleContent': middle
    },
    data () {
      return {
        isSelf: false,
        btnConcern: false,
        topBody: true,
        options: [{
          value: '未设置',
          label: '未设置'
        }, {
          value: '男',
          label: '男'
        }, {
          value: '女',
          label: '女'
        }],
        currentUser: {
          avatar: ''
        },
        avatar: '',
        value: this.GLOBAL.USER.sex,
        noChange: true,
        username: this.GLOBAL.USER.username,
        brief: this.GLOBAL.USER.brief,
        email: this.GLOBAL.USER.email,
        phone: this.GLOBAL.USER.phone,
        startIndex: 0,
        lastIndex: 12,
        sex: '',
        imageURL: '',
        editSelfPanel: false,
        avatarFile: '',
        amounts: {},
        contents: {},
        tempContents: {},
        dropDown: false,
        staus: '',
        followAmount: 0
      }
    },
    watch: {
      '$route' (to, from) {
        if (this.$route.params.username === this.GLOBAL.USER.username) {
          console.log(1)
          this.isSelf = true
          this.getData(this.GLOBAL.USER.username)
        }
        let username = this.$route.params.username
        this.contents = {}
        this.getData(username)
      }
    },
    created: function () {
      if (this.$route.params.username === this.GLOBAL.USER.username) {
        this.isSelf = true
        this.currentUser = this.GLOBAL.USER
      }
      let username = this.$route.params.username
      this.getData(username)
    },
    methods: {
      getData: function (username) {
        let url = this.GLOBAL.BASE_URL + '/api/v1/query/user'
        console.log(this.startIndex, this.lastIndex)
        this.$axios.get(url, {
          params: {
            username: username,
            startIndex: this.startIndex,
            lastIndex: this.lastIndex
          }
        }).then(function (response) {
          console.log('user-info', response.data)
          this.status = response.data.tips
          this.tempContents = this.contents
          this.contents = response.data.contents
          this.tempContents = $.extend(this.contents, this.tempContents)
          this.contents = this.tempContents
          this.currentUser = response.data.user
          this.amounts['produces'] = this.currentUser.produces
          this.amounts['following'] = Object.keys(this.currentUser.following).length
          this.amounts['followers'] = Object.keys(this.currentUser.followers).length
          this.isConcerned(this.currentUser.uid)
        }.bind(this))
      },
      closeTop: function (boolean) {
        this.topBody = boolean
      },
      refresh: function () {
        this.startIndex = 0
        this.lastIndex = 12
        let username = this.$route.params.username
        this.getData(username)
      },
      loadData: function () {
        this.startIndex += 12
        this.lastIndex += 12
        if (this.status !== 'All loaded!') {
          let username = this.$route.params.username
          this.getData(username)
        } else {
          this.$message.error('没有更多数据啦！')
        }
      },
      back: function () {
        this.$router.push('/home')
      },
      editorVisible: function () {
        this.editSelfPanel = true
      },
      // 关联btn的显示
      isConcerned: function (vid) {
        console.log('GLOBAL', this.GLOBAL.USER)
        this.btnConcern = this.GLOBAL.USER.following[vid]
      },
      concernAction: function () {
        this.btnConcern = !this.btnConcern
        let url = this.GLOBAL.BASE_URL + '/api/v1/concern/action'
        let data = new FormData()
        data.append('vid', this.currentUser.uid)
        data.append('status', this.btnConcern)
        console.log('user', this.GLOBAL.USER)
        console.log('concern-data', data)
        this.$axios.post(url, data).then(function (response) {
          if (response.data.tips !== 'Successed!') {
            this.$message.error('操作不成功！')
          } else {
            this.getData(this.currentUser.username)
            this.GLOBAL.USER.following[this.currentUser.uid] = this.btnConcern
          }
        }.bind(this))
      },
      avatarChoosed: function (event) {
        var file = event.target.files[0]
        if (file) {
          const isJPG = file.type === 'image/jpeg'
          const isLt2M = file.size / 1024 / 1024 < 2
          if (!isJPG) {
            this.$message.error('只能上传 JPG 格式!')
          }
          if (!isLt2M) {
            this.$message.error('大小不能超过 2MB!')
          }
          if (isJPG && isLt2M) {
            this.imageURL = (window.URL || window.webkitURL).createObjectURL(file)
            this.avatarFile = file
          }
        }
      },
      submitChange: function () {
        let data = new FormData()
        data.append('avatar', this.avatarFile)
        data.append('brief', this.brief)
        data.append('phone', this.phone)
        data.append('sex', this.value)
        let url = this.GLOBAL.BASE_URL + '/api/v1/edit/profile'
        this.$axios.post(url, data).then(function (response) {
          if (response.data.tips === 'Successed!') {
            this.$message({
              type: 'success',
              message: '修 改 成 功 ！',
              center: true,
              duration: 1000
            })
            this.GLOBAL.USER = response.data.user
            this.editSelfPanel = false
          }
        }.bind(this))
      }
    }
  }
</script>

<style scoped>
  .fadein-enter-active, .fadein-leave-active {
    transition: opacity .5s
  }

  .fadein-enter, .fadein-leave-to {
    opacity: 0
  }

  .el-row {
    width: 100% !important;
    margin: 0 !important;
    padding-top: 0.5rem !important;
  }

  [v-cloak] {
    display: none;
  }

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
  }

  .el-main {
    padding: 0;
  }

  .fa-cog, .el-icon-back {
    position: relative;
    width: 6%;
    line-height: 100%;
    padding-left: 1%;
    font-size: 1rem;
  }

  .headTitle {
    width: 80%;
    text-align: center;
    font-size: 1.0rem;
  }

  .fa-user-plus {
    width: 6%;
    float: right;
    padding-right: 10px;
    font-size: 1rem;
  }

  .user-avatar {
    width: 70px;
    height: 70px;
    border-radius: 50%;
  }

  .user-username {
    display: inline-block;
    width: 100%;
    font-size: 1.2rem;
    text-align: center;
    padding-bottom: 0.6rem;
  }

  .content-left {
    padding-bottom: 1rem;
  }

  .content-right .el-button {
    margin: 0;
    width: 100%;
  }

  .dialogTitle {
    display: inline-block;
    width: 86%;
    text-align: center;
  }

  .edit-avatar p {
    width: 100%;
    text-align: center;
    color: #409EFF;
    margin-top: 8px;
    margin-bottom: 8px;
  }

  .edit-avatar span {
    display: block;
    width: 100%;
    text-align: center;
  }

  .avatar-choose {
    display: none;
  }

  .edit-avatar span img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
  }

  .informations span {
    display: inline-block;
    width: 100%;
    line-height: 40px;
  }

  .el-icon-back {
    position: relative;
    font-size: larger;
    font-weight: bolder;
  }

  .nav-bottom {
    position: fixed;
    left: 0;
  }
</style>
