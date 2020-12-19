<template>
  <v-container id="SubmissionManager">
    <v-card-title class="font-weight-black mb-3" style="font-size: 1.6em">
      提交作品管理与评分系统
    </v-card-title>
    <v-divider></v-divider>
    <v-card flat>
      <v-card-title>
        <v-btn class="info ml-2" @click="downloadFile">
          下载{{ selected && selected.length ? "选定" : "全部" }}文件
        </v-btn>
        <v-btn class="info ml-2" @click="downloadSheet"> 下载打分表 </v-btn>
        <v-btn class="info ml-2" @click="submitSheet"> 提交更改 </v-btn>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        v-model="selected"
        :headers="headers"
        :items="participantList"
        :search="search"
        item-key="participantId"
        :items-per-page="10"
        show-select
      >
        <template v-slot:item.actions="{ item }">
          <v-icon
            class="mr-2"
            @click="downloadFile(item.participantId, item.name)"
          >
            cloud_download
          </v-icon>
        </template>

        <!-- @save="save"
            @cancel="cancel"
            @open="open"
            @close="close" -->

        <template v-slot:item.grade="props">
          <v-edit-dialog :return-value.sync="props.item.grade">
            {{ props.item.grade == undefined ? "无成绩" : props.item.grade }}
            <template v-slot:input>
              <v-text-field
                v-model="props.item.grade"
                :rules="[max32chars]"
                label="设置成绩"
                single-line
                counter
              ></v-text-field>
            </template>
          </v-edit-dialog>
        </template>

        <template v-slot:item.mainAward="props">
          <v-edit-dialog :return-value.sync="props.item.mainAward">
            {{ props.item.mainAward || "无" }}
            <template v-slot:input>
              <v-text-field
                v-model="props.item.mainAward"
                :rules="[max32chars]"
                label="设置奖项名"
                single-line
                counter
              ></v-text-field>
            </template>
          </v-edit-dialog>
        </template>

        <template v-slot:item.submitted="{ item }">
          <v-chip :color="item.submitted ? 'success' : 'warning'" dark>
            {{ item.submitted ? "已提交" : "未提交" }}
          </v-chip>
        </template>

        <template v-slot:item.extraAward="props">
          <v-edit-dialog :return-value.sync="props.item.extraAward">
            {{ props.item.extraAward || "无" }}
            <template v-slot:input>
              <v-text-field
                v-model="props.item.extraAward"
                :rules="[max32chars]"
                label="设置奖项名"
                single-line
                counter
              ></v-text-field>
            </template>
          </v-edit-dialog>
        </template>

        <template v-slot:no-data>
          <v-container> 暂无参赛者信息 </v-container>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import merge from "webpack-merge";
import { requestPost, downloadFile } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "SubmissionManager",
  mixins: [redirect, snackbar, logState],
  methods: {
    getName(firstParticipant, count) {
      console.log("first part", firstParticipant, firstParticipant || "参赛者");
      return (
        (firstParticipant || "参赛者") +
        (count > 1 ? "等" + count + "人的" : "的")
      );
    },
    __generalDownloader(url, filename, params = {}, callback = undefined) {
      this.isDownloading = true;
      requestPost(
        {
          url: url,
          data: {
            contestId: this.contestInfo.id,
            ...params,
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
              console.log("downloaded file is", res, res.data);
              downloadFile(res.data, "", filename);
              !callback || callback();
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
          this.snackbar("服务器开小差啦，请稍后再试", "error");
          console.log("error", err);
          this.isDownloading = false;
        });
    },
    downloadFile(participantId = undefined, name = undefined) {
      let params = {
        count: 1,
        participantId: [participantId],
      };
      if (!participantId) {
        params.count = 0;
        if (this.selected.length < this.participantList.length) {
          params.participantId = this.selected.map((v) => v.participanId);
        }
      }
      console.log("selected", this.selected, params);
      this.__generalDownloader(
        "/submit/submissions",
        this.getName(
          name || (this.selected.length ? this.selected[0].name : undefined),
          params.count
        ) + "参赛作品.zip",
        params
      );
    },
    submitSheet() {},
    downloadSheet() {},
    fetchList() {
      this.isLoading = true;
      requestPost(
        {
          url: "/grade/sheet",
          data: {
            contestId: this.contestInfo.id,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isLoading = false;
          console.log(res);
          switch (res.data.error) {
            case undefined:
              if (!(res.data.data instanceof Array)) {
                this.listLength = 0;
                return;
              }
              this.participantList = res.data.data.map((v) => {
                //TODO: FIXME: certificate:
                return {
                  ...v,
                  actions: { submission: v.submitted, certificate: false },
                };
              });
              this.listLength = this.participantList.length;
              console.log("hahaha", res.data, this.participantList);
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
    this.fetchList();
  },
  data() {
    return {
      max32chars: (v) => v.length <= 32 || "请不要超过32个字符",
      //   isNumber: (v) => isNumber(v) || "请输入成绩",
      isLoading: true,
      participantList: [],
      selected: [],
      search: "",
      listLength: 0,
      headers: [
        { text: "编号", value: "participantId" },
        { text: "姓名", value: "name" },
        { text: "提交状态", value: "submitted" },
        { text: "分数", value: "grade" },
        { text: "主要奖项", value: "mainAward" },
        { text: "次要奖项", value: "extraAward" },
        { text: "操作", value: "actions" },
      ],
    };
  },
};
</script>