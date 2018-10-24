<template>
  <div class="contentWraper">
    <div class="cardWraper" v-for="item in content" :key="item">
        <el-card body-style="padding: 0">
          <h3 class="title">{{item.title}}</h3>
          <div class="contentImg">
          <img :src="item.img" alt="">
          </div>
          <p class="date">{{item.date}}</p>
        </el-card>
      </div>
  </div>
</template>

<script>
    export default {
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
    display: block;
    text-align: center;
  }
  .contentImg{
    display: inline-block;
    width: 100%;
    text-align: center;
  }
  .cardWraper{
    align-items: center;
    align-content: center;
  }

</style>
