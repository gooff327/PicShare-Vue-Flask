<!--suppress ALL -->
<template>
   <el-form :model="loginForm" hide-required-asterisk status-icon :rules="rules" ref="loginForm" class="demo-loginForm">
     <v-header></v-header>
     <el-form-item label="Username"  prop="username" :rules="[
     {required:true,message:'Username can not be empty!',trigger:'blur'},
     {min:5,max:18,message:'Username\'s length is between 5 and 18!',trigger:'blur'}
     ]">
      <el-input v-model="loginForm.username" placeholder="Username more than 6 chars"></el-input>
     </el-form-item>

     <el-form-item label="Password" prop="pass" :rules="[
      {required:true,message:'Password can not be empty!',trigger:'blur'},
      {min: 5,max: 18,message:'Password is between 5 to 18',trigger:'blur'}
     ]">
       <el-input type="password" v-model="loginForm.pass" placeholder="Your unique keys"></el-input>
     </el-form-item>

     <el-form-item v-if='regVisible' label="Repeat" prop="checkPass">
       <el-input class="reg" type="password" v-model="loginForm.checkPass" placeholder="Type it once more"></el-input>
     </el-form-item>

     <el-form-item v-if="regVisible" label="Email" prop="email" :rules="[
     {required: true,message:'Email adress can not be empty',trigger:'blur'}
     ]">
       <el-input class="reg" type="email" v-model="loginForm.email" placeholder="NO Gmail!"></el-input>
     </el-form-item>
     <br>
      <div class="btnGroup">
        <el-button type="info" plain v-if="logBtn" @click="regVisible=!regVisible,btnSwitch = !btnSwitch" class="logbtn">{{btnSwitch ? 'Cancel' : 'Register'}}</el-button>
        <br>
        <br>
        <el-button type="primary" @click="submitUser('loginForm')" v-if="logBtn"  class="logbtn">{{btnSwitch ? 'Submit' :  'Log in'}}</el-button>
      </div>
    </el-form>
</template>

<script>
  import headers from './header/header'
  import store from '../vuex/user'
  export default {
  name: 'Login',
    components: {
    'v-header': headers
    },
    data (
    ) {
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
      } else { callbacks() }
      }
    return {
      loginForm: {
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
          { validator: validatePass, trigger: 'blur' }
        ],
        checkPass: [
      {validator: validatePass2, trigger: 'blur'}]
    }}
    },
    methods: {
      submitUser (Form) {
        this.$refs[Form].validate((valid) => {
          if (this.btnSwitch === false) {
            var logurl = 'http://127.0.0.1:5000/api/v1/login'
            var data = {
              'auth': {
                username: this.loginForm.username,
                  password: this.loginForm.pass
              }
            }
            this.$axios.get(logurl, data).then(function (response) {
              console.log(response)
              var token = response.data.token
              console.log(token)
              store.commit('ADD_TOKEN', token)
              this.$router.push('/home')
              this.$notify({
                title: 'Messages:',
                message: 'Welcome !' + `  ${this.loginForm.username}`,
                position: 'bottom',
                type: 'success'
              })
            }.bind(this))
              .catch(function (error) {
                console.log(error)
                this.store.commit('REMOVE_TOKEN', this.store.state.token)
                this.$notify.error({
                  title: 'Warning:',
                  message: 'Wrong username or password!',
                  position: 'bottom',
                  type: 'error'
                })
              }.bind(this))
          } else {
            var regurl = 'http://127.0.0.1:5000/api/v1/register'
            var regdata = {
              username: this.loginForm.username,
              password: this.loginForm.pass,
              email: this.loginForm.email
            }
            this.$axios.post(regurl, regdata).then(function (response) {
              var code = response.data.err_code
              console.log(typeof code)
              switch (code) {
                case 200:
                  this.$notify({
                  title: 'Messages:',
                  message: `${this.loginForm.username},you can log in now!`,
                  position: 'bottom',
                  type: 'success'
                })
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
              console.log(response)
              }.bind(this))
          }
          }
        )
      }
    }
    }
</script>

<style scoped>
  .demo-loginForm{
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  }
  .demo-loginForm{
    align-items: center;
  }
  .btnGroup{
    align-items: center;
  }
  .logbtn{
    width: 100%;
  }
</style>
