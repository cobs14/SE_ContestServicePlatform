<template>
  <div id="ContestAwardPanel">
    <v-card-title style="font-weight: 800"> 获奖信息查询 </v-card-title>
    <div v-if="isLoading" id="skeleton_loaders">
      <v-skeleton-loader type="heading" class="my-2"></v-skeleton-loader>
      <v-skeleton-loader type="list-item-avatar-three-line@3">
      </v-skeleton-loader>
    </div>
    <div v-else>
      <v-card-text v-if="hasAward">
        <div>恭喜您，您在竞赛中获得下列奖项：</div>
        <v-card-title style="font-weight: 800">
          {{ mainAward + " " + extraAward }}
        </v-card-title>
      </v-card-text>
      <v-card-text v-else>
        <div>很遗憾，您没能获奖。请不要气馁，再接再厉~</div>
      </v-card-text>
    </div>

    <v-card-actions>
      <div v-if="!isLoading && hasAward">
        <v-btn
          depressed
          class="success mx-2"
          @click="downloadCertificate"
          :loading="isDownloading"
          >下载证书</v-btn
        >
        <v-btn
          depressed
          class="info mx-2"
          @click="external('/certificate/' + this.data.verifyCode)"
          >查看详情</v-btn
        >
      </div>
      <v-spacer />
      <v-btn depressed @click="closePage">关闭此页面</v-btn>
    </v-card-actions>
  </div>
</template>

<script>
import { requestPost, downloadFile } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "ContestAwardPanel",
  mixins: [redirect, snackbar, logState],
  inject: ["softReload"],
  watch: {},
  methods: {
    closePage() {
      this.$emit("close");
    },
    downloadCertificate() {
      if (this.isDownloading) return;
      this.isDownloading = true;
      requestPost(
        {
          url: "/certification/getmy",
          data: {
            contestId: this.contestId,
          },
          responseType: "blob",
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isDownloading = false;
          switch (res.data.error) {
            case undefined:
              this.snackbar("获取文件成功，即将保存到本地", "success");
              downloadFile(res.data, "", "获奖证书.zip");
              break;
            case "login":
              this.clearLogInfo();
              break;
            default:
              this.snackbar(
                "哎呀，出错了，错误原因：" + res.data.error,
                "error"
              );
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
          this.softReload();
          this.isDownloading = false;
        });
    },
    fetchAwardState() {
      requestPost(
        {
          url: "/certification/award",
          data: {
            contestId: this.contestId,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          switch (res.data.error) {
            case undefined:
              if (res.data.isUser) {
                this.data = res.data;
                this.hasAward = this.data.verifyCode != "";
              }
              break;
            case "login":
              this.clearLogInfo();
              break;
            default:
              this.snackbar(
                "哎呀，出错了，错误原因：" + res.data.error,
                "error"
              );
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，暂时无法获取您的状态", "error");
          console.log("error", err);
        });
    },
  },
  data() {
    return {
      data: {
        mainAward: "",
        extraAward: "",
        verifyCode: "",
      },
      hasAward: false,
      isLoading: false,
      isDownloading: false,
    };
  },
  created() {
      this.fetchAwardState();
  },
  props: {
    contestId: Number,
  },
};
</script>

<style>
</style>