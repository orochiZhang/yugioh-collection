import Vue from 'vue'
import App from './App.vue'
import Pack from './components/Pack.vue'
import Main from './components/Main.vue'
import axios from 'axios'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

Vue.prototype.$axios = axios    //全局注册，使用方法为:this.$axios

Vue.config.productionTip = false

Vue.use(VueRouter)

const routes = [
  { path: '/pack', component: Pack },
  { path: '/', component: Main }
]

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = new VueRouter({
  routes // short for `routes: routes`
})

// 4. Create and mount the root instance.
// Make sure to inject the router with the router option to make the
// whole app router-aware.
new Vue({
  render: h => h(App), router
}).$mount('#app')

