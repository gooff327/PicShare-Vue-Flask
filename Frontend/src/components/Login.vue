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
        var actions = 'login'
        if (this.btnSwitch === false) {
          actions = 'login'
        } else {
          actions = 'register'
        }
        this.$refs[Form].validate((valid) => {
            if (valid) {
              var data = ({
                // username: this.loginForm.username,
                // password: this.loginForm.pass,
                // email: this.loginForm.email
                auth: {
                  username: `${this.loginForm.username}`,
                  password: `${this.loginForm.pass}`
                },
                email: this.loginForm.email
              })
              console.log(data)
              const path = 'http://127.0.0.1:5000/api/v1/' + actions
              this.$axios.get(path, data)
                .then(function (res) {
                  console.log(res)
                  var sflag = res.data.flag
                  if (actions === 'login') {
                  if (sflag === -1) {
                  this.$notify.error({
                    title: 'Warning',
                    message: 'Username or password error',
                    position: 'bottom',
                    type: 'error'
        })
        } else {
           this.$router.push({path: '/home'})
           this.$notify({
                    title: 'System notifications:',
                    message: 'You are welcom!',
                    position: 'bottom',
                    type: 'success'
        })
        }
        } else {
          if (sflag === 2) {
          }
        }
        }.bind(this))
            } else {
              this.$notify.error({
          title: 'Warning:',
          message: 'Please check the form!',
          position: 'bottom',
          type: 'error'
        })
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
