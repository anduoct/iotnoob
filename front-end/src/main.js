import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import "bootstrap/dist/css/bootstrap.css"

Vue.config.productionTip = false

new Vue({
  e1:'#app',
  router,
  store,
  render: h => h(App),
  template:'<App/>'
}).$mount('#app')
