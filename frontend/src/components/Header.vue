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
        <v-text-field
          class="mr-4"
          hide-details
          append-icon="mdi-magnify"
          single-line
          placeholder="输入名称、关键词以查找竞赛"
          v-model="contestFilter"
          @click:append="searchContests"
        ></v-text-field>
        <v-btn> Cobs </v-btn>
        <v-btn v-if="isLoggedIn" class="info ml-2" @click="redirect('/login')"
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
  methods: {
    searchContests() {
      this.redirect("/search/" + encodeURIComponent(this.contestFilter));
    },
  },
  data() {
    return {
      isLoggedIn: true,
      contestFilter: "",
    };
  },
};
</script>