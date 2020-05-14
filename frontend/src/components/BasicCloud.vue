<template>
  <div class="basicCloudView">
    <svg id="basicCloudSvg">
    </svg>

  </div>
</template>

<script>
import * as d3 from 'd3'
import * as Cloud from '@/assets/js/cloud.js'
export default {
  name: 'BasicCloud',
  props: {
    msg: String
  },
  data() {
    return {

    }
  },
  watch: {

  },
  mounted() {
    d3.csv('test.csv').then(data => Cloud.testCloud(data))

  },
  methods: {

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.basicCloudView {
  text-align: center;
  height: 80vh;
  width: 90vw;
  margin: auto;
}
#basicCloudSvg {
  height: 100%;
  width: 100%;
}
</style>
