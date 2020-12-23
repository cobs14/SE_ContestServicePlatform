// pages/certificate/certificate.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    isLoading: false,
    fetched: false,
    data: {
      contestInfo: Object,
      sponsorInfo: Object,
      participantInfo: Object,
    },
  },

  fetchCertificate: function () {
    var that = this;
    if (that.data.isLoading) {
      console.log('is already loading');
      return;
    }
    wx.scanCode({
      //onlyFromCamera: true, // 只允许从相机扫码
      success(res) {
        let verifyCode = res.result.split('/certificate/')[1];
        if (!(typeof verifyCode == 'string')) {
          app.showError('未找到有效信息');
          return;
        }
        app.showLoading('正在查询');
        that.setData({
          isLoading: true,
        })
        wx.request({
          url: 'https://contestplus.cn/api/certification/verify',
          method: 'POST',
          data: {
            verifyCode: verifyCode,
          },
          success: function (res) {
            console.log('success', res);
            if (res.data.error != undefined) {
              app.showError('未找到有效信息');
              return;
            }
            that.setData({
              fetched: true,
              data: res.data,
            })
          },
          fail: function () {
            app.showError('未找到有效信息');
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


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }

})