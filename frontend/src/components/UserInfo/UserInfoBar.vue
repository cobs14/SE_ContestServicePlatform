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

    <v-dialog v-model="showDialog" width="500">
      <v-card>
        <v-card-title class="headline grey lighten-2">
          与&nbsp;{{ info.username }}&nbsp;交谈
          <v-spacer></v-spacer>
          <v-btn class="info darken-2" @click="external('/user/' + info.id)">
            访问个人主页
          </v-btn>
        </v-card-title>

        <chat-box
          v-if="showDialog"
          :contactInfo="info"
          @showSnackbar="snackbar"
        ></chat-box>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
// 用户信息条
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import ChatBox from "@/components/MessageComponents/ChatBox.vue";
export default {
  components: { ChatBox },
  name: "UserInfoBar",
  mixins: [redirect, snackbar],
  methods: {
    // 显示用户信息等
    showUserInfo() {
      this.showDialog = true;
    },
    enableAvatar() {
      this.hasAvatar = true;
    },
  },
  props: {
    info: Object,
  },
  data() {
    return {
      hasAvatar: false,
      showDialog: false,
    };
  },
};
</script>