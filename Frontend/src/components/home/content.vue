<template>
  <div class="contentWraper">
    <el-collapse v-model="ActiveName" @change="handleChange">
      <el-collapse-item v-for="item in content" :key="item" :title="item.title" :name="item.id">
          <p class="content">{{item.content}}<span><a href="#">link>></a></span></p>
          <div class="contentImg">
            <img :src="item.img" alt="">
          </div>
          <p class="cardBottom">{{item.date}}</p>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
    export default {
      data () {
        return {
          ActiveName: '1'
        }
      },
      methods: {
        handleChange (val) {
          console.log(val)
        }
      },
      props: {
        content: {
          type: Object
        }
      },
        name: 'content'
    }
</script>
<style scoped>
  .title{
    margin-bottom: 0;
    display: block;
  }
  .contentImg{
    display: inline-block;
    width: 100%;
    text-align: center;
  }
  .contentImg,img{
    border-radius: 6px;
  }
  .contentWraper{
    padding-left: 2rem;
    padding-right: 2rem;
  }
  .content{
    font-size: small;
    color: darkgrey;
  }
  .cardBottom{
    font-size: smaller;
    color: grey;
   }

</style>
