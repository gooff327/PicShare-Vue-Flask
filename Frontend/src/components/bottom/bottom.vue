<template>
  <div class="footerbar">
    <el-button-group>
      <el-button size="small" class="function homeBtn" @click="showHomePanel" type="default" ><i class="fa fa-home"></i><p>主 页</p></el-button>
      <el-button size="small"  type="default" class="function"><i class="fa fa-handshake-o"></i><p>关 注</p></el-button>
      <el-button size="small" class="plus"  onclick="document.getElementById('image-uploader').click();" type="default" ><i class="fa fa-plus-circle"></i></el-button>
      <el-button size="small"  type="default" class="function" ><i class="fa fa-envelope"></i><p>消 息</p> </el-button>
      <el-button size="small"  type="default" @click="showPersonalData" class="function"><i class="fa fa-user-o"></i><p>我 的</p> </el-button>
      <input id="image-uploader" class="image-uploader" type="file" @change="updateEvent($event)">
    </el-button-group>
  </div>
</template>
<script>
    export default {
        name: 'bottom',
      data () {
          return {
            newButtonBool: {}
          }
      },
      methods: {
        updateEvent: function (event) {
          var file = event.target.files[0]
          console.log(file)
          if (file) {
            const isJPG = file.type === 'image/jpeg'
            const isLt4M = file.size / 1024 / 1024 < 4
            if (!isJPG) {
              this.$message.error('只能上传 JPG 格式!')
            }
            if (!isLt4M) {
              this.$message.error('大小不能超过 4MB!')
            }
            console.log(isJPG, isLt4M)
            if (isJPG && isLt4M) {
              this.GLOBAL.UPLOAD_FILE = file
              this.$router.push('/create/details')
            }
          }
        },
        showHomePanel: function () {
          this.$router.push('/home')
        },
        showPersonalData: function () {
          this.$router.push(`/user/${this.GLOBAL.USER.username}`)
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
  .footerbar{
    position: fixed;
    width: 100%;
    bottom: 0;
    background-color: rgba(255,255,255,0.1);
  }
  .el-button-group{
    width: 100%;
    background-color: rgba(255,255,255,0.1);
  }
  .el-button:active,button:hover {
    background: #fff;
    color: #606266;
  }
  .function{
    position: relative;
    bottom: 2px;
    width: 20%;
    float: left;
    padding-left: 0;
    padding-right: 0;
    border: 0px;
    height: 46px;
  }
  .function .fa,.function.fa::before{
    font-size: 26px;
    padding: 0;
    margin: 0;
    position: relative;
    top: -6px;
    width: 100%;
  }
  .footerbar p {
    position: relative;
    font-size: smaller;
    top: -16px;
    margin-bottom: 0px;
  }
  .plus{
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
  .image-uploader{
    height: 100%;
    width: 100%;
    display: none;
  }
</style>
