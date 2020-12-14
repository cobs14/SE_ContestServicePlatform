<template>
  <v-container id="NoticeManager">
    <v-card-title class="font-weight-black mb-3" style="font-size: 1.6em">
      管理{{ contestInfo.title }}的公告
    </v-card-title>

    <v-divider></v-divider>
    <v-card-subtitle> 创建新公告 </v-card-subtitle>
    <v-card class="mb-3" flat>
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
            :notice="{}"
            :editMode="false"
            :contestId="contestInfo.id"
            @onEditComplete="onEditComplete"
            @showSnackbar="snackbar"
          >
          </notice-editor>
        </div>
      </v-expand-transition>
    </v-card>
    <v-divider></v-divider>
    <v-card-subtitle> 管理已发布的公告 </v-card-subtitle>

    <v-skeleton-loader v-if="isLoading" type="list-item-avatar-three-line@3" />

    <v-expansion-panels
      flat
      accordion
      v-if="!isLoading && noticeList.length > 0"
    >
      <v-expansion-panel
        v-for="item in noticeList"
        :info="item"
        :key="item.noticeId"
      >
        <v-expansion-panel-header>{{ item.title }}</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-card>
            <notice-viewer
              v-if="editNoticeNumber != item.noticeId"
              class="py-2"
              :notice="item"
              @showSnackbar="snackbar"
            ></notice-viewer>
            <notice-editor
              v-if="editNoticeNumber == item.noticeId"
              class="py-2"
              :notice="item"
              :editMode="true"
              :contestId="contestInfo.id"
              @onEditComplete="onEditComplete"
              @showSnackbar="snackbar"
            >
            </notice-editor>
          </v-card>
          <v-card-actions class="pt-4" v-if="editNoticeNumber != item.noticeId">
            <v-btn @click="editNoticeNumber = item.noticeId" class="info">
              编辑内容</v-btn
            >
            <v-spacer></v-spacer>
            <v-btn
              @click="deleteNotice(item.noticeId)"
              class="error"
              :disabled="isDeleting"
              :loading="isDeleting"
            >
              删除该公告</v-btn
            >
          </v-card-actions>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-card-title v-if="!isLoading && noticeList.length == 0">
      您尚未发布过任何公告
    </v-card-title>

    <v-divider></v-divider>
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
      console.log("edit completed, edit mode enabled?", editMode);
      this.expand = false;
      this.editNoticeNumber = 0;
      if (!cancelled) {
        this.refreshList();
      }
    },
    deleteNotice(noticeId) {
      this.isDeleting = true;
      console.log("noticeId is", noticeId);
      requestPost(
        {
          url: "/notice/delete",
          data: {
            noticeId: noticeId,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isDeleting = false;
          switch (res.data.error) {
            case undefined:
              this.snackbar("删除成功", "success");
              this.onEditComplete(true, false);
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
          this.isDeleting = false;
        });
    },
    refreshList() {
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
          switch (res.data.error) {
            case undefined:
              this.noticeList = res.data.data;
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
          this.isLoading = false;
        });
    },
  },
  props: {
    contestInfo: Object,
  },
  created() {
    console.log("RECVED INFO", this.contestInfo);
    this.refreshList();
  },
  data() {
    return {
      params: Object,
      isLoading: false,
      isDeleting: false,
      noticeList: [],
      expand: false,
      editNoticeNumber: 0,
    };
  },
};
</script>