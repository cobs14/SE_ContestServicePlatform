<template>
  <v-card tile id="UserInfoBar" class="mx-auto my-3">
    <v-row>
      <v-spacer v-if="$vuetify.breakpoint.smAndUp"></v-spacer>
      <v-list-item-avatar class="ml-5">
        <v-avatar v-show="hasAvatar" @click="showUserInfo">
          <img :src="info.avatar" @load="enableAvatar" />
        </v-avatar>
        <v-avatar v-show="!hasAvatar" color="green darken-3">
          <span class="white--text headline">{{
            info.username.substr(0, 2)
          }}</span>
        </v-avatar>
      </v-list-item-avatar>

      <v-col cols="12" sm="6">
        <v-card-title>
          {{ info.username }}
        </v-card-title>
        <v-card-subtitle> {{ info.school }}，{{ info.major }} </v-card-subtitle>
      </v-col>
      <v-btn
        v-if="!$vuetify.breakpoint.smAndUp"
        dark
        class="green darken-2 ma-5"
        @click="showUserInfo"
        >详情</v-btn
      >
      <v-col cols="12" sm="3" v-if="$vuetify.breakpoint.smAndUp"> </v-col>
      <v-col cols="12" sm="2" v-if="$vuetify.breakpoint.smAndUp">
        <v-btn dark class="green darken-2 mt-5 mx-5" @click="showUserInfo"
          >详情</v-btn
        >
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
export default {
  name: "UserInfoBar",
  mixins: [redirect, snackbar],
  methods: {
    submit() {},
    showUserInfo() {},
    enableAvatar() {
      this.hasAvatar = true;
    },
  },
  props: {
    info: Object,
  },
  created() {
    console.log(this.info);
  },
  data() {
    return {
      hasAvatar: false,
    };
  },
};
</script>