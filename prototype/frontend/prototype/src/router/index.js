import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/views/HomePage'
import ManagePage from '@/views/ManagePage'
import ContestPage from '@/views/ContestPage'
import Register from '@/views/Register'
import Login from "@/views/Login"

Vue.use(Router)

export default new Router({
  // Todo: 与后端配合时，请参考下列网址（以解决可能的404问题）
  // https://router.vuejs.org/zh/guide/essentials/history-mode.html#%E5%90%8E%E7%AB%AF%E9%85%8D%E7%BD%AE%E4%BE%8B%E5%AD%90
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/manage',
      name: 'ManagePage',
      component: ManagePage
    },
    {
      path: '/manage/:type',
      name: 'ManagePage',
      component: ManagePage
    },
    {
      path: '/contest',
      name: 'ContestPage',
      component: ContestPage
    },
    {
      path: '/contest/:type',
      name: 'ContestPage',
      component: ContestPage
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})
