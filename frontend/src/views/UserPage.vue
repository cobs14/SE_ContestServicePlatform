<template>
  <v-container id="UserPage">
    <v-card-title>这是用户界面，ID是{{ userId }}，而不是用户中心</v-card-title>
    <v-card-text>当前用户名是：{{userInfo.username}}</v-card-text>
    <v-card-text> 在这儿加个聊天框、再加点个人信息就行了 </v-card-text>
  </v-container>
</template>

<script>
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "UserPage",
  mixins: [redirect, snackbar, logState],
  components: {},
  methods: {
    pageNotFound() {
      this.softReload("/pagenotfound");
      this.snackbar("您查找的用户不存在", "error");
    },
    fetchUserInfo() {
      console.log('user id', this.userId);
      requestPost(
        {
          url: "/user",
          data: {
            id: this.userId,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          if (res.data.error == undefined) {
            this.userInfo = res.data;
            console.log("Get User Info: ");
            console.log(this.userInfo);
          } else {
            this.snackbar("出错啦，错误原因：" + res.data.error, "error");
            this.redirect("/");
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
          this.redirect("/");
        });
    },
  },
  created() {
    this.userId = this.$route.params.userId;
    if (!/^\d+$/.test(this.userId)) {
      this.pageNotFound();
    }
    if (this.userId == this.getUserId()) {
      this.redirect("/user");
    } else {
      this.fetchUserInfo();
    }
  },
  data() {
    return {
      userId: 0,
      userInfo: Object,
    };
  },
  computed: {},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
