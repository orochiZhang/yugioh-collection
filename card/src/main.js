import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
Vue.prototype.$axios = axios    //全局注册，使用方法为:this.$axios

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')

