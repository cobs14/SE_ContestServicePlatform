<template>
  <div id="LoginPage">
    <v-container>
      <v-row>
        <v-spacer> </v-spacer>
        <div style="width: 70%; margin-top: 5%">
          <login-main
          v-if="page == 'login'"
          >
          </login-main>
          <login-password
          v-if="page == 'password'"
          >
          </login-password>
        </div>
        <v-spacer> </v-spacer>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import LoginMain from "@/components/LoginMain.vue";
import LoginPassword from "@/components/LoginPassword.vue";
export default {
  name: "LoginPage",
  mixins: [redirect, snackbar],
  components: { LoginMain, LoginPassword },
  watch: {
    $route(val) {
      this.selectPage(val.params.option);
    },
  },
  methods: {
    selectPage(param) {
      this.page = !param || param == "" ? "login" : param;
      if (!["login", "password"].includes(this.page))
        this.redirect("/pagenotfound");
    },
  },
  created() {
    this.selectPage(this.$route.params.option);
  },
  data() {
    return {
      page: ""
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
