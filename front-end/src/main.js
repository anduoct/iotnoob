import Vue from 'vue'
import App from './App.vue'
import router from './router'
import "bootstrap/dist/css/bootstrap.css"

Vue.config.productionTip = false

new Vue({
  e1:'#app',
  router,
  render: h => h(App),
  template:'<App/>'
}).$mount('#app')
