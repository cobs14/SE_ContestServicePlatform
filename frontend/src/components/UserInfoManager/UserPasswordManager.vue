<template>
  <v-card id="UserPasswordManager" class="ma-2 pa-2">
    <v-card-title>重置密码</v-card-title>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn class="info ma-2" @click="showPanel('passwordPanel', false)">
        取消修改
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "UserPasswordManager",
  inject: ["showPanel"],
  mixins: [redirect, snackbar, logState],
  methods: {},
  props: {
    info: Object,
  },
  data() {
    return {};
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
