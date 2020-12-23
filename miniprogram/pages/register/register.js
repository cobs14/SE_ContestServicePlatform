// pages/register/register.js
const app = getApp()

Page({
  data: {
    username: '',
    password: '',
    isLoggingIn: false,
    loggedIn: false,
    userInfo: {
      session_id: "",
      userType: "",
      qrcode: "",
      contestList: [],
    },
  },

  //事件处理函数
  onShow: function () {
    console.log('global data', app.globalData.userInfo, app.globalData.userInfo.session_id)
    this.setData({
      userInfo: app.globalData.userInfo,
      loggedIn: app.globalData.userInfo.session_id != '',
    })
  },
  onLoad: function () {

  },


  // 获取输入账号 
  usernameInput: function (e) {
    this.setData({
      username: e.detail.value
    })
  },

  // 获取输入密码 
  passwordInput: function (e) {
    this.setData({
      password: e.detail.value
    })
  },

  // 登录处理
  login: function () {
    var that = this;
    if (that.data.isLoggingIn || that.data.loggedIn) {
      console.log('nonoo', that.data.isLoggingIn, that.data.loggedIn);
      return;
    }
    if (this.data.username.length == 0 || this.data.password.length == 0) {
      wx.showToast({
        title: '账号或密码不能为空',
        icon: 'none',
        duration: 2000
      })
      return;
    } else {
      app.showLoading('登录中');
      that.setData({
        isLoggingIn: true,
      })
      wx.request({
        url: 'https://contestplus.cn/api/session',
        method: 'post',
        data: {
          username: that.data.username,
          password: that.data.password
        },
        success(res) {
          if (res.data.error != undefined) {
            app.showError('账号或密码错误');
            app.globalData.userInfo.session_id = "";
          } else {
            app.globalData.userInfo = res.data;
            that.setData({
              userInfo: res.data,
              loggedIn: true,
            })
            console.log('loggedin', res.data, app.globalData.userInfo);

          }
        },
        fail() {
          app.showError('账号或密码错误');
          app.globalData.userInfo.session_id = "";
        },
        complete() {
          app.hideLoading('登录中');
          that.setData({
            isLoggingIn: false,
          })
        },
      })
    }
  }
})