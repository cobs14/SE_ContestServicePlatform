<template>
  <v-app-bar
    app
    dark
    src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg"
  >
    <v-container>
      <v-row>
        <v-toolbar-title>Contest+ 探索竞赛</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn> Cobs </v-btn>
        <v-btn v-if='isLoggedIn' class="warning ml-2" @click="redirect('/register')">注册</v-btn>
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