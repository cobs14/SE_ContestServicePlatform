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
  },
  data() {
    return {
      constRawContestFilter: {
        id: 0,
        sponsorId: 0,
        allowGroup: 'Any',
        censorStatus: 'Accept',
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