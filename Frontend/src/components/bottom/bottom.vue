<template>
  <div class="el-container">
    <el-button-group>
      <el-button size="small" :autofocus=true type="default" ><i class="fa fa-home"></i> </el-button>
      <el-button size="small" type="default" ><i class="fa fa-handshake-o"></i> </el-button>
      <el-button size="small" v-on:click="update" type="default" ><i class="fa fa-plus-circle"></i> </el-button>
      <el-button size="small" type="default" ><i class="fa fa-envelope"></i> </el-button>
      <el-button size="small" type="default" ><i class="fa fa-user-o"></i> </el-button>
    </el-button-group>
  </div>
</template>

<script>
import GLOBAL from '../../../config/global'
    export default {
        name: 'bottom',
      methods: {
          update: function () {
            GLOBAL.UPDATE = true
            console.log(GLOBAL.UPDATE)
          }
      }
    }
</script>

<style scoped>
  .row{
    width: 100%;
  }
  .el-container{
    position: fixed;
    width: 100%;
    bottom: 0;
    background-color: rgba(255,255,255,1);
  }
  .el-button-group{
    width: 100%;
    padding-right: 1rem;
  }
  .el-button{
    width: 20%;
    float: left;
    border: 0px;
    height: 46px;
  }
  .fa{
    color: gray;
    font-size: 30px;
    margin-bottom: 0.3rem;
  }
</style>
