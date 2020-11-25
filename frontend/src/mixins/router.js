export const redirect = {
  methods: {
    redirect: function (url) {
      console.log('path', this.$route.path);
      if (this.$route.path != '/' && url != '/' && url != '') {
        this.$router.push('/');
      } else {
        this.$router.push("/pagenotfound");
      }
      this.$nextTick(() => this.$router.replace(url));
    },
    reload: function () {
      this.$router.go(0);
    },
    external: function (url) {
      window.open(url, '_blank');
    }
  }
}