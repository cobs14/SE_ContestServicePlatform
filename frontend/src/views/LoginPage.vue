<template>
  <div id="LoginPage">
    <v-container>
      <v-row>
        <v-spacer> </v-spacer>
        <div style="width: 70%; margin-top: 5%">
          <login-main @showSnackbar="snackbar" v-if="page == 'login'">
          </login-main>
        </div>
        <v-spacer> </v-spacer>
      </v-row>
    </v-container>
  </div>
</template>

<script>
// 登录页面
import { redirect } from "@/mixins/router.js";
import { logState } from "@/mixins/logState.js";
import { snackbar } from "@/mixins/message.js";
import LoginMain from "@/components/Authorization/LoginMain.vue";

export default {
  name: "LoginPage",
  mixins: [redirect, snackbar, logState],
  components: { LoginMain },
  watch: {
    $route(val) {
      this.selectPage(val.params.option);
    },
  },
  methods: {
    // 显示登录页面的组件
    selectPage(param) {
      this.page = !param || param == "" ? "login" : param;
      if (!["login", "password"].includes(this.page))
        this.redirect("/pagenotfound");
    },
  },
  created() {
    // 如果登录，则自动回到主页
    if (this.hasLogin()) {
      this.redirect("/");
    }
    this.selectPage(this.$route.params.option);
  },
  data() {
    return {
      page: "",
      email: "",
      passstep: this.$route.params.verifycode ? 3 : 1,
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
