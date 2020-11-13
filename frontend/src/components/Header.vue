<template>
  <v-app-bar
    app
    dark
    src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg"
  >
    <v-container>
      <v-row class="align-center">
        <v-col>
          <v-card-title>Contest+</v-card-title>
          <v-card-subtitle>竞赛新发现</v-card-subtitle>
        </v-col>
        <v-spacer></v-spacer>
        <v-btn> Cobs </v-btn>
        <v-btn
          v-if="isLoggedIn"
          class="info ml-2"
          @click="redirect('/login')"
          >登录</v-btn
        >
        <v-btn class="ml-2"> 注销 </v-btn>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
import { redirect } from "@/mixins/router.js";
export default {
  mixins: [redirect],
  name: "v-header",
  data() {
    return {
      isLoggedIn: true,
    };
  },
};
</script>