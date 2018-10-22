<template>
      <el-form ref="form" :model="form">
        <el-form-item label="Title">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
      </el-form>
</template>

<script>
    export default {
        name: 'form'
    }
</script>

<style scoped>

</style>
