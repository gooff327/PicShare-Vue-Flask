<template>
  <el-dialog
    :visible.sync="updatePanel"
    :fullscreen="true"
    :show-close="false"
    width="100%">
    <div slot="title" class="updateTitle">
      <i @click="cancelUpload" class="el-icon-back"></i>
      <span class="dialogTitle">新 帖 子</span>
      <a class="uploadeBtn" icon="el-icon-upload2" size="mini" type="primary" @click="readyToUpload">发 布</a>
    </div>
    <img v-if="imageURL" :src="imageURL" class="image">
    <el-input class="inputDesc" :autosize="{ minRows: 1, maxRows: 6 }" type="textarea" placeholder="添加照片说明..." v-model="imageDescription"></el-input>
  </el-dialog>
</template>

<script>
    export default {
        name: 'editor',
      data () {
          return {
            updatePanel: true,
            imageURL: '',
            imageDescription: ''
          }
      },
      created: function () {
        this.imageURL = (window.URL || window.webkitURL).createObjectURL(this.GLOBAL.UPLOAD_FILE)
      },
      methods: {
          cancelUpload: function () {
            this.updatePanel = false
            this.$router.back()
          },
          readyToUpload: function () {
          var data = new FormData()
          data.append('imageFile', this.GLOBAL.UPLOAD_FILE)
          data.append('imageDescription', this.imageDescription)
          let config = {headers: {'Content-Type': 'mutipart/form-data'}}
          let url = this.GLOBAL.BASE_URL + '/api/v1/post/newpassage'
          this.$axios.post(url, data, config).then(function (response) {
            if (response.data.tips === 'Successed!') {
              this.GLOBAL.UPLOAD_FILE = ''
              this.updatePanel = false
              this.$router.back()
              this.$message({
                type: 'success',
                message: '发 布 成 功 ！',
                center: true,
                duration: 1000})
              this.refreshContent()
              this.updatePanel = false
            }
          }.bind(this))
        }
      }
    }
</script>

<style scoped>
  .el-icon-back{
    position: relative;
    font-size: larger;
    font-weight: bolder;
  }
  .dialogTitle{
    display: inline-block;
    position: relative;
    left: 36%;
  }
  .image{
    max-width: 100%;
    border-radius: 6px;
  }
  .uploadeBtn{
    color: #409EFF;
    display: inline-block;
    float: right;
  }
  .inputDesc{
    padding-top: 0.5rem;
  }
</style>
