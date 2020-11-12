<template>
  <div id="Register">
    <v-container>
      <v-btn class="warning ml-2" @click="snackbar('email:'+email)">显示邮件地址</v-btn>
      <v-row>
        <v-spacer> </v-spacer>
        <register-main v-bind:email.sync="email" @showSnackbar='snackbar'> </register-main>
        <v-spacer> </v-spacer>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import RegisterMain from "@/components/RegisterMain.vue";
export default {
  name: "RegisterPage",
  mixins: [redirect, snackbar],
  computed: {},
  components: { RegisterMain },
  methods: {},
  data() {
    return {
      email: "",
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
