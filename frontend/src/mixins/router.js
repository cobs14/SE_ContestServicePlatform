export const redirect = {
  methods: {
    redirect: function (url) {
      this.$router.push("/");
      this.$nextTick(() => this.$router.push(url));
    },
    reload: function () {
      this.$router.go(0);
    }
  }
}