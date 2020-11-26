import Vue from 'vue'
import axios from 'axios'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import ErrPage from '@/views/ErrPage'
import LoginPage from '@/views/LoginPage'
import RegisterPage from '@/views/RegisterPage'
import HomePage from "@/views/HomePage";
import SearchPage from "@/views/SearchPage";
import ManagementPage from "@/views/ManagementPage"
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
      path: '/login/:option',
      name: 'LoginSubPage',
      component: LoginPage
    },
    {
      path: '/login/:option/:verifycode',
      name: 'LoginVerifyPage',
      component: LoginPage
    },
    {
      path: '/management',
      name: 'ManagementPage',
      component: ManagementPage
    },
    {
      path: '*',
      name: 'ErrPage',
      component: ErrPage
    }
  ]
})
