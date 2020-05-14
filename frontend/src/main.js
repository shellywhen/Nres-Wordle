import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import $ from 'jquery'
import * as d3 from 'd3'
Vue.use(ElementUI);
Vue.config.productionTip = false
window.$ = $
window.jQuery = $
window.d3 = d3
Vue.prototype.$hostname = 'http://localhost:1111'
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
