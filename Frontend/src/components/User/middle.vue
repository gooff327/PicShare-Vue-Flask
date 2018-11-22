<template>
    <el-row>
      <el-col :span="24" class="middle-tab-a">
        <div class="posts">
          <span class="quantity">1</span>
          <br>
          <span class="label">帖子</span>
        </div>
        <div class="followers">
          <span class="quantity">9</span>
          <br>
          <span class="followers">粉丝</span>
        </div>
        <div class="following">
          <span class="quantity">10</span>
          <br>
          <span class="following">关注</span>
        </div>
      </el-col>
      <el-col :span="24" class="middle-tab-b">
        <span class="fa fa-th"></span><span class="fa fa-navicon"></span>
      </el-col>
    </el-row>
</template>

<script>
    export default {
        name: 'Middle'
    }
</script>

<style scoped>
  .middle-tab-a{
    border-top: 1px solid gainsboro;
    padding: 0 !important;
  }
  .middle-tab-b{
    border-top: 1px solid gainsboro;
    border-bottom: 1px solid gainsboro;
    padding: 0 !important;
  }
  .middle-tab-a div{
    display: block;
    padding: 0;
    margin: 0;
    width: 33%;
    text-align: center;
    line-height: 2rem;
    float: left;
  }
  .middle-tab-b span{
    display: inline-block;
    padding: 0;
    margin: 0;
    width: 50%;
    text-align: center;
    line-height: 2rem;
  }

</style>
