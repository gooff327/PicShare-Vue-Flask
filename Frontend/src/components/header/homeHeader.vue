<template>
<div class="brand">
  <el-dropdown>
    <iframe class="icons" src="../../../static/icons/github.svg"  frameborder="0"></iframe>    <el-dropdown-menu slot="dropdown">
    <el-dropdown-item><a class="dropmenu" href="http://github.com/gooff327">Github</a></el-dropdown-item>
    <el-dropdown-item><p class="dropmenu" @click="toAdmin">Administor</p></el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
  <span class="centerText">Gooff's 技术杂货铺</span>
</div>
</template>

<script>
    export default {
      name: 'homeHeader',
      methods: {
        toAdmin () {
          this.$router.push({path: '/admin'})
        }
      }
    }
</script>

<style scoped>
.brand{
  height: 37px;
  display: block;
  border-bottom: 1px solid lightgrey;
}
.brand,a{
}
.centerText{
  font-family: "DejaVu Sans";
  position: absolute;
  right: 134px;
  top: 14px;

}
.dropmenu{
  text-decoration: none;
  color: grey;
}

.icons{
  /*position: absolute;*/
  /*top: 0;*/
  /*left: 150px;*/
  /*width: 48px;*/
  margin: 0;
  padding: 0;
  height: 30px;
  width: 30px;
  align-items: center;
  display: inline-block;
}

</style>
