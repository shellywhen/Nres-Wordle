<template>
  <div class="create">
    <Form/>
  </div>
</template>
<script>
// @ is an alias to /src
import Form from '@/components/Form.vue'
export default {
  name: 'Create',
  components: {
    Form
  }
}
</script>
<style lang="less">
.create {
  text-align: center;
}
</style>
