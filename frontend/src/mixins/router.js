export const redirect = {
  methods: {
    redirect: function (url) {
      this.$router.push(url);
      this.$router.go(0);
    },
    reload: function () {
      this.$router.go(0);
    },
    external: function (url) {
      console.log('mail address', url);
      window.open(url, '_blank');
    }
  }
}