<template>
  <div class="adminPanel">
    <header class="adminHeaders">Administor Panel</header>
    <el-collapse v-model="ActiveMode" @change="handleChange">
      <el-collapse-item title="Submit new passages" name="1">
        <br>
        <el-form ref="adminForm" :model="form" label-width="80px">
          <el-form-item label="Title">
            <el-input v-model="form.title"></el-input>
          </el-form-item>
          <el-form-item label="Library">
            <el-select v-model="form.cls" placeholder="Classify your passage">
              <el-option label="Tweaks" value="tweaks"></el-option>
              <el-option label="Skills" value="skills"></el-option>
              <el-option label="ProxyShare" value="proxy"></el-option>
              <el-option label="Wallpapers" value="wallpaper"></el-option>
              <el-option label="SexyGirls" value="sexy"></el-option>
              <el-option label="Admin'sword" value="admin"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="ImageSource">
            <el-input v-model="form.imgloc"></el-input>
          </el-form-item>
          <el-form-item label="Content">
            <el-input ref="content" type="textarea" autosize="{minRows:4, maxRows:10}" v-model="form.content"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit(form)">Submit</el-button>
            <el-button @click="onCancel">Cancel</el-button>
          </el-form-item>
        </el-form>
      </el-collapse-item>
      <el-collapse-item title="Manage your passages" name="2">
        <!--<ul><li v-for="item in posted" :key="item">-->
          <!--<p>{{item.title}}</p>-->
          <!--<p>{{item.date}}</p>-->
          <!--<p>{{item.pv}}</p>-->
        <!--</li></ul>-->
      </el-collapse-item>
      <el-collapse-item title="Change your password" name="3"></el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
    export default {
      data () {
        return {
          ActiveMode: '1',
          form: {
            title: '',
            cls: '',
            content: '',
            imgloc: ''
          }
          // posted: {}
        }
      },
        name: 'admin',
      methods: {
        onSubmit (form) {
          var adminUrl = `${this.GLOBAL.BASE_URL}+/api/v1/admin`
          this.$axios.post(adminUrl, {
            title: `${this.form.title}`,
            cls: `${this.form.cls}`,
            img: `${this.form.imgloc}`,
            content: `${this.form.content}`
          }).then(function (response) {
            this.$notify.info({
              title: '消息',
              message: `${response.data.tips}`
            })
          }.bind(this))
          this.$router.go(-1)
        },
        onCancel () {
          this.$router.go(-1)
        }
      }
    }
</script>

<style scoped>
  .adminHeaders{
    width: 100%;
    height: 40px;
    display: block;
    font-weight: bold;
    font-size: larger;
    font-family: "PingFang SC";
    padding: 20px 0 20px 0 ;
    text-align: center;
  }
  .adminPanel{
    padding: 0 20px 0 20px;
  }
</style>
