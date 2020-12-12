<template>
  <div id="ContestGroupInfo">
    <v-card-title style="font-weight: 800">查看团队信息 </v-card-title>
    <v-card-text>
      todo
      <div class="grey--text">{{ group.groupName }}</div>
    </v-card-text>
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
  name: "ContestRegister",
  mixins: [redirect, snackbar, filter, logState],
  inject: ["softReload"],
  watch: {},
  methods: {
    closePage() {
      this.$emit("close");
    },
  },
  data() {
    return {};
  },
  created() {
    console.log("group info", this.userGroup);
  },
  props: {
    userGroup: Object,
  },
};
</script>

<style>
</style>