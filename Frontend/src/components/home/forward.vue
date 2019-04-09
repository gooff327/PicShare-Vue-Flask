<template>
  <el-container>
    <el-header>
      <i @click="goBack" class="el-icon-back"></i>
      <span>转 发</span>
    </el-header>
    <el-row>
      <section class="inputSection">
        <div class="inputWrapper">
          <el-input size="mini" :autosize="{ minRows: 1, maxRows: 4}" class="input" type="textarea" v-model="content"
                    placeholder="说点什么吧"></el-input>
        </div>
        <div class="btnWrapper">
          <el-button type="primary" class="submitBtn" size="mini" @click="submit">发 送</el-button>
        </div>
      </section>
      <section class="content">
        <div class="imgWrapper">
          <img :src="this.passage['img']" :preview=this.passage.pid alt="">
        </div>
      </section>
    </el-row>
  </el-container>

</template>

<script>
  export default {
    name: 'forward',
    data () {
      return {
        passage: this.$route.params['passage'],
        content: ''
      }
    },
    methods: {
      goBack: function () {
        this.$router.go(-1)
      },
      submit: function () {
        let url = this.GLOBAL.BASE_URL + '/api/v1/forward'
        let data = {
          uid: this.GLOBAL.USER.uid,
          author: this.GLOBAL.USER.username,
          vid: this.passage.uid,
          pid: this.passage.pid,
          content: this.content
        }
        this.$axios.post(url, data).then((response) => {
          if (response.status === 200) {
            this.GLOBAL.showLoading({text: '转发成功，跳转中', background: 'rgba(255,250,250,0.8)', lock: true})
            this.$router.back()
          } else {
            this.$message({
              type: 'error',
              message: '转发失败，服务器逻辑错误',
              center: true,
              duration: 1000
            })
          }
        }, reject => {
          this.$message({
            type: 'error',
            message: '转发失败，服务器请求未成功',
            center: true,
            duration: 1000
          })
        })
      }
    }
  }
</script>

<style scoped>
  .el-header {
    padding: 0 !important;
    margin: 0 !important;
    height: 2rem !important;
    margin-bottom: 1rem;
  }

  .el-header span {
    vertical-align: center;
    display: inline-block;
    color: rgba(43, 43, 43, 0.93);
    width: 80%;
    text-align: center;
    font-size: 1.0rem;
    line-height: 2rem;
    font-weight: 700;
  }

  .el-icon-back {
    position: relative;
    display: inline-block;
    width: 2rem;
    height: 1.2rem;
    border-radius: 4px;
    line-height: 1.2rem;
    text-align: center;
    margin-left: 2%;
    font-size: 1rem;
  }

  .el-icon-back:hover {
    background-color: rgba(129, 129, 129, 0.2);
  }

  .content {
    display: block;
    width: 100%;
    margin-top: 0.6rem;
    border-radius: 4px;
  }

  .imgWrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 0.2rem;
    padding-bottom: 0.4rem;
  }

  .imgWrapper img {
    flex: 1;
    max-width: 94%;
    width: 94%;
    height: 52.875%;
    border-radius: 4px;
    object-fit: fill;
  }

  .inputSection {
    margin-top: 1rem;
    line-height: 2rem;
    display: flex;
  }

  .inputWrapper {
    flex: 1;
    display: inline-block;
    line-height: 2rem;
    justify-content: center;
    align-items: center;
    vertical-align: center;

  }

  .inputWrapper .input {
    width: 90%;
    margin-left: 0.6rem;
    line-height: 2rem;
  }

  .btnWrapper {
    line-height: 2rem;
  }

  .submitBtn {
    display: inline-block;
    margin-right: 0.6rem;
    width: 80%;
  }
</style>
