<!--suppress ALL -->
<template>
  <div class="wrapper">
  <div class="inputWrapper">
      <el-form :model="loginForm" hide-required-asterisk status-icon :rules="rules" ref="loginForm"
               class="demo-loginForm">
        <el-form-item v-if="regVisible" prop="Avatar">
          <el-upload
            class="avatar-uploader"
            :on-success="this.handleSuccess"
            :auto-upload="false"
            :on-change="setPreview"
            ref="uploadAvatar"
            :data="this.loginForm"
            :show-file-list="false">
            <img v-if="imageUrl" :src=imageUrl class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </el-form-item>
        <el-form-item label="用户名" prop="username" :rules="[
     {required:true,message:'Username can not be empty!',trigger:'blur'},
     {min:5,max:18,message:'Username\'s length is between 5 and 18!',trigger:'blur'}
     ]">
          <el-input v-model="loginForm.username" placeholder="用户名至少6位"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="pass" :rules="[
      {required:true,message:'Password can not be empty!',trigger:'blur'},
      {min: 5,max: 18,message:'Password is between 5 to 18',trigger:'blur'}
     ]">
          <el-input type="password" v-model="loginForm.pass" placeholder="请输入密码"></el-input>
        </el-form-item>

        <el-form-item v-if='regVisible' label="确认密码" prop="checkPass">
          <el-input class="reg" type="password" v-model="loginForm.checkPass" placeholder="请重复输入密码"></el-input>
        </el-form-item>

        <el-form-item v-if="regVisible" label="电子邮箱" prop="email" :rules="[
     {required: true,message:'Email地址不能为空',trigger:'blur'}
     ]">
          <el-input class="reg" type="email" v-model="loginForm.email" placeholder="example@gamil.com"></el-input>
        </el-form-item>
        <br>
        <div class="btnGroup">
          <el-button type="info" plain v-if="logBtn" @click="regVisible=!regVisible,btnSwitch = !btnSwitch"
                     class="logbtn">
            {{btnSwitch ? '取 消' : '注 册'}}
          </el-button>
          <br>
          <br>
          <el-button type="primary" @click="submitUser('loginForm')" v-if="logBtn" class="logbtn">{{btnSwitch ? '提 交' :
            '登录'}}
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
  import headers from './header/homeHeader'
  import store from '../vuex/user'

  export default {
    name: 'Login',
    components: {
      'v-header': headers
    },
    data () {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('Please inssert password'))
        } else {
          if (this.loginForm.checkPass !== '') {
            this.$refs.loginForm.validateField('checkPass')
          }
          callback()
        }
      }
      var validatePass2 = (rule, value, callbacks) => {
        if (value === '') {
          callbacks(new Error('Please insert password!'))
        } else if (value !== this.loginForm.pass) {
          callbacks(new Error('Password do not match!'))
        } else {
          callbacks()
        }
      }
      return {
        imageUrl: '',
        imageFile: '',
        loginForm: {
          avatar: '',
          pass: '',
          username: '',
          email: '',
          checkPass: '',
          openfullscreen: false
        },
        datas: '',
        btnSwitch: false,
        regVisible: false,
        logBtn: true,
        rules: {
          pass: [
            {validator: validatePass, trigger: 'blur'}
          ],
          checkPass: [
            {validator: validatePass2, trigger: 'blur'}]
        }
      }
    },
    methods: {
      reUpload: function (url, data, Form) {
        this.GLOBAL.uploadImageToPicbed(this.imageFile).then(resolve => {
          if (resolve['data']['url']) {
            data['avatar'] = resolve['data']['url']
            this.$axios.post(url, data).then(function (response) {
              var code = response.data.err_code
              switch (code) {
                case 200:
                  this.$notify({
                      title: 'Messages:',
                      message: `${this.loginForm.username},you can log in now!`,
                      position: 'bottom',
                      type: 'success'
                    }
                  )
                  this.$refs.uploadAvatar.submit()
                  this.$router.go(0)
                  break
                case 402:
                  this.$notify.error({
                    title: 'Messages:',
                    message: 'This username is unaviliable',
                    position: 'bottom',
                    type: 'error'
                  })
                  this.$refs[Form].resetFields()
                  break
                case 403:
                  this.$notify.error({
                    title: 'Messages:',
                    message: 'This email has signed!',
                    position: 'bottom',
                    type: 'error'
                  })
                  this.$refs[Form].resetFields()
                  break
              }
            }.bind(this))
          } else {
            this.$notify.error({
              title: 'Error:',
              message: 'Avatar upload failed!',
              position: 'bottom',
              type: 'error'
            })
          }
        })
      },
      loginReq: function (url, data, Form) {
        this.$axios.get(url, data).then(function (response) {
          this.GLOBAL.USER = response.data.user
          var token = response.data.token
          store.commit('ADD_TOKEN', token)
          this.$router.push('/home')
          this.$message({
            dangerouslyUseHTMLString: true,
            center: true,
            duration: 1500,
            message: 'Welcome!' + '<b>' + `${this.loginForm.username}` + '</b>',
            type: 'success'
          })
        }.bind(this))
          .catch(function (error) {
            console.log(error)
            this.$store.commit('REMOVE_TOKEN', this.$store.state.token)
            this.$notify.error({
              title: 'Warning:',
              message: 'Wrong username or password!',
              position: 'bottom',
              type: 'error'
            })
          }.bind(this))
      },
      submitUser (Form) {
        this.GLOBAL.showLoading()
        this.$refs[Form].validate((valid) => {
            if (this.btnSwitch === false) {
              var logurl = this.GLOBAL.BASE_URL + '/api/v1/login'
              var data = {
                'auth': {
                  username: this.loginForm.username,
                  password: this.loginForm.pass
                }
              }
              this.loginReq(logurl, data, Form)
            } else {
              let regurl = this.GLOBAL.BASE_URL + '/api/v1/register'
              let regdata = {
                username: this.loginForm.username,
                password: this.loginForm.pass,
                email: this.loginForm.email
              }
              this.reUpload(regurl, regdata, Form)
            }
          }
        )
      },
      setPreview (file) {
        const isJPG = file.raw.type === 'image/jpeg'
        const isLt2M = file.size / 1024 / 1024 < 2
        if (!isJPG) {
          this.$message.error('只能上传 JPG 格式!')
        }
        if (!isLt2M) {
          this.$message.error('大小不能超过 2MB!')
        }
        this.imageFile = file.raw
        this.imageUrl = (window.URL || window.webkitURL).createObjectURL(file.raw)
        return isJPG && isLt2M
      }
    }
  }
</script>

<style scoped>
  .wrapper{
    margin: 0;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background-image: url("https://img.xjh.me/random_img.php?type=bg&ctype=nature&return=302&device=mobile");
    /*filter: blur(15px);*/
    background-size: cover;
    width: 100%;
    height: 97vh;
    z-index: 1;

  }
  .inputWrapper {
    width: 70vw;
    padding: 0vw 5vw 5vw 5vw;
    background-color: rgba(19,19,14,0.9);
    border-radius: 6px;
  }

  .demo-loginForm {
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  }

  .demo-loginForm {
    align-items: center;
  }

  .btnGroup {
    align-items: center;
  }

  .logbtn {
    width: 100%;
  }

  .avatar-uploader {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
  }

  .avatar-uploader .el-upload {
    border: 1px dot-dot-dash #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    overflow: hidden;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }

  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 6rem;
    height: 6rem;
    line-height: 6rem;
    text-align: center;
  }

  .avatar {
    border-radius: 50%;
    width: 6rem;
    height: 6rem;
    display: block;
  }
</style>
