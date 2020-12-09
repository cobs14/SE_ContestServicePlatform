<template>
  <v-container id="NoticeManager">
    <v-card class="ma-3">
      <v-card-actions @click="expand = !expand">
        <v-btn color="blue lighten-2" text @click.stop="expand = true">
          点击此处以创建新公告...
        </v-btn>
        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon>{{ expand ? "mdi-chevron-up" : "mdi-chevron-down" }}</v-icon>
        </v-btn>
      </v-card-actions>

      <v-expand-transition>
        <div v-show="expand">
          <v-divider></v-divider>
          <notice-editor
            class="py-2"
            :notice="{
              noticeId: 5,
              title: '请交报名费',
              content: 'TODO: 一会儿从这儿继续开始',
              link: 'baidu.com',
              hasFile: 1,
            }"
            :editMode="false"
            :contestId="this.contestInfo.id"
            @onEditComplete="onEditComplete"
            @showSnackbar="snackbar"
          >
          </notice-editor>
        </div>
      </v-expand-transition>
    </v-card>

    <notice-viewer
      :notice="{
        title: '请交报名费',
        content: 'TODO: 一会儿从这儿继续开始',
        link: 'baidu.com',
        hasFile: 1,
      }"
    ></notice-viewer>

    <v-skeleton-loader v-if="isLoading" type="list-item-avatar-three-line@3" />
    <div v-if="!isLoading && noticeList.length > 0">
      <v-card
        class="ma-3"
        v-for="item in noticeList"
        :info="item"
        :key="item.noticeId"
        @showSnackbar="snackbar"
      >
        <v-card-title>
          {{ item.title }}
        </v-card-title>
        <v-card-text>
          {{ item.content }}
        </v-card-text>
        <v-card-actions>
          <v-btn text class="blue--text"> 编辑公告 </v-btn>
        </v-card-actions>
      </v-card>
    </div>
    <v-card-title v-if="!isLoading && noticeList.length == 0">
      您尚未发布过任何公告
    </v-card-title>
  </v-container>
</template>

<script>
import merge from "webpack-merge";
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import { logState } from "@/mixins/logState.js";
import NoticeViewer from "../NoticeComponent/NoticeViewer.vue";
import NoticeEditor from "../NoticeComponent/NoticeEditor.vue";
export default {
  components: { NoticeViewer, NoticeEditor },
  name: "NoticeManager",
  mixins: [redirect, snackbar, filter, logState],
  methods: {
    onEditComplete(editMode, cancelled = false) {
      //TODO: FIXME: close panels and so on
      console.log("edit completed, edit mode enabled?", editMode);
      if(cancelled){//or !cancelled, it depends
          //TODO: FIXME: cancel logic here
      }
    },
    refreshList(resetPage = false) {
      this.isLoading = true;
      console.log("notice params", this.contestInfo, this.contestInfo.id);
      requestPost(
        {
          url: "/notice/browse",
          data: {
            contestId: this.contestInfo.id,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isLoading = false;
          if (res.data.error == "login") {
            this.clearLogInfo();
          } else {
            this.noticeList = res.data.data;
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
          this.softReload();
          this.isLoading = false;
        });
    },
  },
  props: {
    contestInfo: Object,
  },
  created() {
    console.log("RECVED INFO", this.contestInfo);
    this.refreshList(true);
  },
  data() {
    return {
      params: Object,
      isLoading: false,
      noticeList: [],
      expand: false,
    };
  },
};
</script>