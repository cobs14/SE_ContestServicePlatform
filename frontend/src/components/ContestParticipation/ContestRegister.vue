<template>
  <div id="ContestRegister">
    <v-card-title>报名参加</v-card-title>
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
  methods: {
    downloadNoticeFile() {
      //TODO: FIXME: download files here
      this.isDownloading = true;
      console.log("we are gonna download,", this.notice);
      requestPost(
        {
          url: "/notice/download",
          data: {
            noticeId: this.notice.noticeId,
          },
          responseType: 'blob',
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isDownloading = false;
          switch (res.data.error) {
            case undefined:
              this.snackbar("获取文件成功，即将保存到本地", "success");
              console.log('downloaded file is', res, res.data, res.headers['content-disposition'].split('.'));
              let suffix = res.headers['content-disposition'].split('.').pop();
              downloadFile(res.data, suffix);
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
  },
  data() {
    return {
      isDownloading: false,
      hasLink: false,
      hasFile: 0,
      parsedLink: "",
    };
  },
  created() {
   
  },
  props: {
    notice: Object,
  },
};
</script>

<style>
</style>