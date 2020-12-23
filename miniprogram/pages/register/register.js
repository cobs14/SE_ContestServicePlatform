// pages/register/register.js
const app = getApp()

Page({
  data: {
    selectedContest: -1,
    username: '',
    password: '',
    isLoading: false,
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

  addParticipant() {
    //TODO: add a participant
    var that = this;
    if (that.data.isLoading) {
      console.log('is already loading');
      return;
    }
    wx.scanCode({
      //onlyFromCamera: true, // 只允许从相机扫码
      success(res) {
        let verifyCode = res.result.split('/apply/')[1];
        if (!(typeof verifyCode == 'string')) {
          app.showError('未找到有效信息');
          return;
        }
        app.showLoading('正在查询');
        that.setData({
          isLoading: true,
        })
        console.log('what is sent?',  that.data.userInfo.session_id, that.data.selectedContest, verifyCode);
        wx.request({
          url: 'https://contestplus.cn/api/offline',
          method: 'POST',
          data: {
            session_id: that.data.userInfo.session_id,
            contestId: that.data.selectedContest,
            qrcode: verifyCode,
          },
          success: function (res) {
            console.log('success', res);
            if (res.data.error != undefined) {
              app.showError('操作失败');
              return;
            }
            app.showMessage('已将' + (res.data.trueName ? res.data.trueName : res.data.username) + '添加到竞赛', 'none');
          },
          fail: function () {
            app.showError('操作失败');
            return;
          },
          complete: function () {
            that.setData({
              isLoading: false,
            })
            app.hideLoading();
          }
        })
      }
    })
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

  showDetailed(event) {
    let that = this;
    let index = event.currentTarget.dataset.num;
    that.setData({
      selectedContest: that.data.userInfo.contestList[index].id == that.data.selectedContest ?
        -1 : that.data.userInfo.contestList[index].id,
    })
    return;
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