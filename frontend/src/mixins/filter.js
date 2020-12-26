// 组件：筛选器
// 可供任何位置的函数快速创建满足API需求的参数
// 而且当API变动时，只需要在此修改对应的参数即可
// 避免了霰弹式修改
export const filter = {
  methods: {
    // 竞赛参数生成器
    getContestFilter: function (params) {
      let { ...filter } = this.constRawContestFilter;
      for (let key in params) {
        filter[key] = params[key];
      }
      return filter;
    },
    // 用户参数生成器
    getUserFilter: function (params) {
      let { ...filter } = this.constRawUserFilter;
      for (let key in params) {
        filter[key] = params[key];
      }
      return filter;
    },
    // 公告参数生成器
    getNoticeFilter: function (params) {
      let { ...filter } = this.constRawNoticeFilter;
      for (let key in params) {
        filter[key] = params[key];
      }
      return filter;
    }
  },
  data() {
    return {
      constRawNoticeFilter: {
        participantOnly: false,
        title: "",
        content: "",
        link: "",
        fileKey: "file",
        file: [],
      },
      constRawUserFilter: {
        username: "",
        school: "",
        major: "",
        studentNumber: "",
        userType: "user",
        getMe: 0,
      },
      constRawContestFilter: {
        id: 0,
        sponsorId: 0,
        allowGroup: 'Any',
        censorStatus: 'Any',
        module: [],
        text: [],
        participant: [],
        group: 0,
        state: {
          apply: 0,
          contest: 0,
          review: 0,
        },
        detailed: false
      },
    }
  },
}