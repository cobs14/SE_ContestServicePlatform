// 组件：路由管理
// 实现了多种页面和路由操作
export const redirect = {
  methods: {
    // 重定向：加载到其它路由
    redirect: function (url) {
      console.log('path', this.$route.path);
      if (this.$route.path != '/' && url != '/' && url != '') {
        this.$router.push('/');
      } else {
        this.$router.push("/pagenotfound");
      }
      this.$nextTick(() => this.$router.replace(url));
    },
    // 强制刷新页面上的全部内容
    reload: function () {
      this.$router.go(0);
    },
    // 在新页面打开链接
    external: function (url) {
      window.open(url, '_blank');
    }
  }
}