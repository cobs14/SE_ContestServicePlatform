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
          <v-card id="LoginPassword" v-if="page == 'password'">
            <v-card-title class="font-weight-black" style="font-size: 1.6em">
            忘记密码
            </v-card-title>
            <v-divider> </v-divider>
            <v-stepper alt-labels :value="passstep">
            <v-stepper-header>
              <v-stepper-step step="1" :complete="1 < passstep">
                确认账号
              </v-stepper-step>
              <v-stepper-step step="2" :complete="2 < passstep">
                发送验证信
              </v-stepper-step>
              <v-stepper-step step="3">
                重置密码
              </v-stepper-step>
            </v-stepper-header>
            <v-divider></v-divider>
            <v-stepper-items>
              <v-stepper-content
              :step = "1"   
              >
                <password-step-1
                :passstep.sync="passstep"
                :email.sync="email"
                >
                </password-step-1>
              </v-stepper-content>
              <v-stepper-content
              :step = "2"
              >
                <password-step-2
                v-if="passstep == 2"
                :passstep.sync="passstep"
                :email="email"
                >
                </password-step-2>
              </v-stepper-content>
              <v-stepper-content
              :step = "3"
              >
                <password-step-3>
                </password-step-3>
              </v-stepper-content>
            </v-stepper-items>
            </v-stepper>
          </v-card>
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
import PasswordStep1 from "@/components/LoginPasswordStep1.vue"
import PasswordStep2 from "@/components/LoginPasswordStep2.vue"
import PasswordStep3 from "@/components/LoginPasswordStep3.vue"

export default {
  name: "LoginPage",
  mixins: [redirect, snackbar],
  components: { LoginMain, PasswordStep1, PasswordStep2, PasswordStep3 },
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
