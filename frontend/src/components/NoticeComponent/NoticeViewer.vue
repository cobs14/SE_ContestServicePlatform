<template>
  <div id="NoticeViewer">
    <v-card-title> {{ notice.title }} </v-card-title>
    <v-card-text>
      {{ notice.content }}
      <div v-if="hasLink">
        <br />
        相关链接：<a :href="parsedLink" target="_blank">{{ notice.link }}</a>
      </div>
    </v-card-text>
    <v-card-actions v-if="hasFile || hasLink">
      <v-btn v-if="hasFile" @click="downloadNoticeFile" class="info mx-3">
        下载文件
      </v-btn>
      <v-btn v-if="hasLink" @click="external(parsedLink)" class="success mx-3">
        前往通知中的链接
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script>
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
export default {
  name: "NoticeViewer",
  mixins: [redirect],
  methods: {
    downloadNoticeFile() {
      //TODO: FIXME: download files here
      console.log("we are gonna download,", this.notice);
    },
  },
  data() {
    return {
      hasLink: false,
      hasFile: 0,
      parsedLink: "",
    };
  },
  created() {
    console.log("from notice viewer,", this.notice, this.hasLink, this.hasFile);
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