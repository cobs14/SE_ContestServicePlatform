<template>
  <div id="NoticeViewer">
    <v-card-title>公告标题：{{ notice.title }} </v-card-title>
    <v-card-text>
      公告内容：{{ notice.content }}
      <div v-if="hasLink">
        <br />
        相关链接：<a :href="parsedLink" target="_blank">{{ notice.link }}</a>
      </div>
    </v-card-text>
    <v-card-actions v-if="hasFile || hasLink">
      <v-btn
        v-if="hasFile"
        @click="downloadNoticeFile"
        class="info mx-3"
        :disabled="isDownloading"
        :loading="isDownloading"
      >
        下载公告中的附件
      </v-btn>
      <v-btn v-if="hasLink" @click="external(parsedLink)" class="success mx-3">
        前往通知中的链接
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script>
// 公告浏览器
import { requestPost, downloadFile } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "NoticeViewer",
  mixins: [redirect, snackbar, filter, logState],
  methods: {
    // 下载公告中包含的文件（如果有）
    downloadNoticeFile() {
      this.isDownloading = true;
      requestPost(
        {
          url: "/notice/download",
          data: {
            noticeId: this.notice.noticeId,
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
              let suffix = res.headers["content-disposition"].split(".").pop();
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
    // 组件创建时自动解析对应的公告内容
    this.hasFile = this.notice.hasFile;
    this.parsedLink = this.notice.link ? this.notice.link.trim() : "";
    this.hasLink = this.parsedLink != "";
    if (this.hasLink && !this.parsedLink.startsWith("http")) {
      this.parsedLink = "http://" + this.parsedLink;
    }
  },
  props: {
    notice: Object,
  },
};
</script>

<style>
</style>