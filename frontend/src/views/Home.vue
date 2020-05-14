<template>
  <div class="home">
    <BasicCloud/>
  </div>
</template>

<script>
// @ is an alias to /src
import BasicCloud from '@/components/BasicCloud.vue'

export default {
  name: 'Home',
  components: {
    BasicCloud
  }
}
</script>
<style lang="less">
.home {
  text-align: center;
}
</style>
