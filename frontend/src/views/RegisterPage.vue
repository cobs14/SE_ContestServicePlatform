<template>
  <div id="Register">
    <v-container>
      <v-btn class="warning ml-2" @click="snackbar('email:' + email)"
        >显示邮件地址(DEBUG)
      </v-btn>
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
            :email='email'
            @showSnackbar="snackbar"
          >
          </register-email>
        </div>
        <v-spacer> </v-spacer>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import RegisterMain from "@/components/RegisterMain.vue";
import RegisterEmail from "@/components/RegisterEmail.vue";
export default {
  name: "RegisterPage",
  mixins: [redirect, snackbar],
  watch: {
    $route(val) {
      this.selectPage(val.params.option);
    },
  },
  components: { RegisterMain, RegisterEmail },
  methods: {
    selectPage(param) {
      this.page = !param || param == "" ? "signup" : param;
      if (!["signup", "emailcheck", "verification"].includes(this.page))
        this.redirect("/pagenotfound");
    },
  },
  created() {
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
