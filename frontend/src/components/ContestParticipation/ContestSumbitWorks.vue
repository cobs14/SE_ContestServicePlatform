<template>
  <div id="ContestGroupInfo">
    <v-card-title style="font-weight: 800">提交您的参赛作品</v-card-title>

    <v-card-text> 
        <div class="grey--text">
            请按照竞赛主办方发布的要求提交参赛作品文件，<br/>
            如果您需要提交多个文件，请将其打包为压缩包。
        </div>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn depressed @click="closePage"
        >关闭此页面</v-btn
      >
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
  created() {},
  props: {
    contestInfo: Object,
  },
};
</script>

<style>
</style>