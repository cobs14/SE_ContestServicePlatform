// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
//document for Vuelidate:
//https://vuelidate.js.org/#sub-installation
import Vuelidate from 'vuelidate'
import router from './router'
import Vuetify from 'vuetify'
import vuetify from '@/plugins/vuetify'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import axios from 'axios'
import md5 from 'js-md5'
import qs from 'qs'

Vue.prototype.$qs = qs;
Vue.prototype.$axios = axios;
Vue.prototype.$md5 = md5;

Vue.use(Vuetify)
Vue.use(Vuelidate)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  vuetify,
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
