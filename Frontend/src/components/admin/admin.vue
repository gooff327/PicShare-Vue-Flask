<template>
  <form>
    <header class="adminHeaders">Administor Panel</header>
  </form>
</template>

<script>
  import form from './form'
    export default {
        name: 'admin',
  component: {
          'form': form
  }
    }
</script>

<style scoped>
  .adminHeaders{
    width: 100%;
    display: block;
    text-align: center;
  }
</style>
