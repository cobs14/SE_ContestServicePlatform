export const filter = {
  methods: {
    getContestFilter: function (params) {
      let { ...filter } = this.constRawContestFilter;
      for (let key in params) {
        filter[key] = params[key];
      }
      // console.log('copy result', params, filter,
      //   this.constRawContestFilter);
      return filter;
    },
    getUserFilter: function (params) {
      let { ...filter } = this.constRawUserFilter;
      for (let key in params) {
        filter[key] = params[key];
      }
      return filter;
    },
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