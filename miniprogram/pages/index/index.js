//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    contestList: [],
    isLoading: false,
    selectedCard: -1,
  },
  //事件处理函数
  bindViewTap: function () {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    this.fetchContestList();
  },

  showDetailed(event) {
    let that = this;
    let index = event.currentTarget.dataset.num;
    that.setData({
      selectedCard: index == that.data.selectedCard ? -1 : index,
    })
    return;
  },

  fetchContestList() {
    let that = this;
    if (this.data.isLoading) {
      console.log('We are already fetching data');
      return;
    }
    this.setData({
      isLoading: true,
      contestList: [],
    });
    app.showLoading('正在加载');
    wx.request({
      url: 'https://contestplus.cn/api/contest/retrieve',
      method: 'POST',
      data: {
        params: {
          id: 0,
          sponsorId: 0,
          allowGroup: 'Any',
          module: [],
          text: [],
          participant: [],
          group: 0,
          censorStatus: 'Accept',
          state: {
            'apply': 0,
            'contest': 0,
            'review': 0,
          },
          detailed: 0,
        },
        pageNum: 1,
        pageSize: 15,
      },
      success: function (res) {
        console.log('success', res);
        if (res.data.error != undefined) {
          app.showError('加载失败');
          return;
        }

        console.log('what is recevied is', res.data, res.data.data.length),
          that.setData({
            contestList: res.data.data,
          })
      },
      fail: function () {
        app.showError('加载失败');
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