<template>
  <div id="Register">
    <v-container>
      <v-row>
        <v-spacer> </v-spacer>
        <div style="width: 70%; margin-top: 5%">
          <register-main
            v-if="page == 'signup'"
            v-bind:email.sync="email"
            @showSnackbar="snackbar"
          >
          </register-main>
          <register-email
            v-if="page == 'emailcheck'"
            :email="email"
            @showSnackbar="snackbar"
          >
          </register-email>
          <register-verification
            v-if="page == 'verification'"
            @showSnackbar="snackbar"
          >
          </register-verification>
        </div>
        <v-spacer> </v-spacer>
      </v-row>
    </v-container>
  </div>
</template>

<script>
// 注册页面
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import RegisterMain from "@/components/Authorization/RegisterMain.vue";
import RegisterEmail from "@/components/Authorization/RegisterEmail.vue";
import RegisterVerification from "@/components/Authorization/RegisterVerification.vue";
export default {
  name: "RegisterPage",
  mixins: [redirect, snackbar],
  watch: {
    $route(val) {
      this.selectPage(val.params.option);
    },
  },
  components: { RegisterMain, RegisterEmail, RegisterVerification },
  methods: {
    selectPage(param) {
      this.page = !param || param == "" ? "signup" : param;
      if (!["signup", "emailcheck", "verification"].includes(this.page))
        this.redirect("/pagenotfound");
    },
  },
  created() {
    // 显示注册页面的组件
    this.selectPage(this.$route.params.option);
  },
  data() {
    return {
      page: "",
      email: "",
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
