export const redirect = {
  methods: {
    redirect: function (url) {
      this.$router.push('/');
      this.$nextTick(() => this.$router.replace(url));
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