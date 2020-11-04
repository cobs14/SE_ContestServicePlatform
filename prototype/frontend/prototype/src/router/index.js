import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/views/HomePage'
import ManagePage from '@/views/ManagePage'
import ContestPage from '@/views/ContestPage'
import Register from '@/views/Register'
<<<<<<< Updated upstream
import Login from "@/views/Login"
import ContestManagePage from '@/views/ContestManagePage'
=======
import Login from '@/views/Login'
import Signup from '@/views/SignupPage'
import ShowAwards from '@/views/ShowAwardsPage'
>>>>>>> Stashed changes

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
      path: '/contest/:status',
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
    },
    {
<<<<<<< Updated upstream
      path: '/manage/contest/:id',
      name: 'ContestManagePage',
      component: ContestManagePage
    },
    {
      path: '/manage/contest/:id/:type',
      name: 'ContestManagePage',
      component: ContestManagePage
=======
      path: '/signup',
      name: 'Signup',
      component: Signup
    },
    {
      path: '/showAwards',
      name: 'ShowAwards',
      component: ShowAwards
>>>>>>> Stashed changes
    }
  ]
})
