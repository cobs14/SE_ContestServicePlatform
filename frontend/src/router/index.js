import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import ErrPage from '@/views/ErrPage'
import LoginPage from '@/views/LoginPage'
import RegisterPage from '@/views/RegisterPage'

Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/login',
      name: 'LoginPage',
      component: LoginPage
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
      path: '*',
      name: 'ErrPage',
      component: ErrPage
    }
  ]
})
