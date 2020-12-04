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
  },
  data() {
    return {
      constRawUserFilter: {
        username: "",
        school: "",
        major: "",
        studentNumber: "",
      },
      constRawContestFilter: {
        id: 0,
        sponsorId: 0,
        allowGroup: 'Any',
        censorStatus: 'Any',
        module: [],
        text: [],
        participator: [],
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