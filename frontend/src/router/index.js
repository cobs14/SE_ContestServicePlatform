import Vue from 'vue'
import axios from 'axios'
import Router from 'vue-router'
import ErrPage from '@/views/ErrPage'
import LoginPage from '@/views/LoginPage'
import RegisterPage from '@/views/RegisterPage'
import HomePage from "@/views/HomePage"
import SearchPage from "@/views/SearchPage"
import UserPage from "@/views/UserPage"
import UserCenterPage from "@/views/UserCenterPage"
import AdminPage from "@/views/AdminPage"
import ManagementPage from "@/views/ManagementPage"
import ContestManagePage from "@/views/ContestManagePage"
import ContestDetailPage from "@/views/ContestDetailPage"
import ResetPasswordPage from "@/views/ResetPasswordPage"
import VueCookies from 'vue-cookies'

Vue.prototype.$axios = axios
Vue.use(Router)
Vue.use(VueCookies)

const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/contest/:contestId',
      name: 'ContestDetailPage',
      component: ContestDetailPage
    },
    {
      path: '/search',
      name: 'SearchPage',
      component: SearchPage
    },
    {
      path: '/search/:keyword',
      name: 'SearchSubPage',
      component: SearchPage
    },
    {
      path: '/register',
      name: 'RegisterPage',
      component: RegisterPage
    },
    {
      path: '/register/:option',
      name: 'RegisterSubPage',
      component: RegisterPage
    },
    {
      path: '/register/:option/:verifycode',
      name: 'RegisterVerifyPage',
      component: RegisterPage
    },
    {
      path: '/login',
      name: 'LoginPage',
      component: LoginPage
    },
    {
      path: '/resetpassword',
      name: 'ResetPasswordPage',
      component: ResetPasswordPage
    },
    {
      path: '/resetpassword/:verifycode',
      name: 'RestPasswordVerifyPage',
      component: ResetPasswordPage
    },
    {
      path: '/admin',
      name: 'AdminPage',
      component: AdminPage
    },
    {
      path: '/management',
      name: 'ManagementPage',
      component: ManagementPage
    },
    {
      path: '/management/:contestId',
      name: 'ContestManagePage',
      component: ContestManagePage,
    },
    {
      path: '/user/:userId',
      name: 'UserPage',
      component: UserPage
    },
    {
      path: '/user',
      name: 'UserCenterPage',
      component: UserCenterPage
    },
    {
      path: '*',
      name: 'ErrPage',
      component: ErrPage
    }
  ]
})
