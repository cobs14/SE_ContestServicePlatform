<template>
  <div id="ContestGroupInfo">
    <v-card-title style="font-weight: 800">查看团队信息 </v-card-title>
    <v-card-text>
      <div>团队信息</div>
      <div class="grey--text">团队名：{{ userGroup.groupName }}</div>
      <div class="grey--text">团队描述：{{ userGroup.description }}</div>
    </v-card-text>
    <v-card-text>
      <div>团队成员</div>
    </v-card-text>
    <v-list-item v-for="(item, i) in userGroup.data" :key="i">
      <v-list-item-avatar v-show="item.avatar">
        <img :src="item.avatar" />
      </v-list-item-avatar>
      <v-list-item-avatar v-show="!item.avatar" color="green darken-3">
        <span class="white--text headline">{{
          item.username.substr(0, 2)
        }}</span>
      </v-list-item-avatar>
      <v-list-item-content class="ml-4">
        <v-list-item-title v-html="item.username"></v-list-item-title>
        <v-list-item-subtitle
          v-html="
            (item.school ? item.school : '未知学校') +
            '，' +
            (item.major ? item.major : '未知专业')
          "
        ></v-list-item-subtitle>
      </v-list-item-content>
      <v-btn
        :class="userId == item.id ? 'orange' : 'green'"
        dark
        @click="redirect('/user/' + item.id)"
      >
        {{ userId == item.id ? "您自己" : "他的主页" }}
      </v-btn>
    </v-list-item>
    <v-card-actions>
      <v-spacer />
      <v-btn depressed @click="closePage">关闭此页面</v-btn>
    </v-card-actions>
  </div>
</template>

<script>
import { requestPost, downloadFile } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "ContestGroupInfo",
  mixins: [redirect, snackbar, filter, logState],
  inject: ["softReload"],
  watch: {},
  methods: {
    closePage() {
      this.$emit("close");
    },
  },
  data() {
    return {
      userId: 0,
    };
  },
  created() {
    console.log("group info", this.userGroup);
    this.userId = this.getUserId();
  },
  props: {
    userGroup: Object,
  },
};
</script>

<style>
</style>