import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
Vue.use(Vuetify)
// 引用图标
export default new Vuetify({
  icons: {
    iconfont: 'mdi' // default - only for display purposes
  }
})
