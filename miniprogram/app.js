//app.js
App({

  showLoading(msg){
    wx.showLoading({
      title: msg,
    })
  },

  hideLoading(){
    wx.hideLoading()
  },

  showMessage(msg, type){
    wx.showToast({
      title: msg,
      icon: type, 
      duration: 2000, 
    })
  },

  showError(errMsg){
    wx.showToast({
      title: errMsg,
      image: '/static/images/error.png',
      duration: 2000, 
    })
  },

  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    
  },
  globalData: {
    userInfo: {
      session_id: "",
      userType: "",
      qrcode: "",
      contestList: [],
    },
  }
})