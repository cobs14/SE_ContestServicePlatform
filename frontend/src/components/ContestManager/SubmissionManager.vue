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
        <v-btn class="info ml-2" @click="showAwardGenerateDialog = true">
          批量填写奖项
        </v-btn>
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
        v-if="!tableRefresh"
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
            v-if="item.submission"
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
          <v-edit-dialog
            :return-value.sync="props.item.grade"
            @save="
              submitSheet('formGrade' + props.item.participantId, props.item)
            "
            large
            save-text="修改"
            cancel-text="取消"
          >
            {{ props.item.grade == "" ? "无成绩" : props.item.grade }}
            <template v-slot:input>
              <v-text-field
                :ref="'formGrade' + props.item.participantId"
                v-model="props.item.grade"
                :rules="[max6chars]"
                label="设置成绩"
                single-line
                :counter="6"
              ></v-text-field>
            </template>
          </v-edit-dialog>
        </template>

        <template v-slot:item.mainAward="props">
          <v-edit-dialog
            :return-value.sync="props.item.mainAward"
            @save="
              submitSheet(
                'formMainAward' + props.item.participantId,
                props.item
              )
            "
            large
            save-text="修改"
            cancel-text="取消"
          >
            {{ props.item.mainAward || "无" }}
            <template v-slot:input>
              <v-text-field
                :ref="'formMainAward' + props.item.participantId"
                v-model="props.item.mainAward"
                :rules="[max12chars]"
                label="设置奖项名"
                single-line
                :counter="12"
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
          <v-edit-dialog
            :return-value.sync="props.item.extraAward"
            @save="
              submitSheet(
                'formExtraAward' + props.item.participantId,
                props.item
              )
            "
            large
            save-text="修改"
            cancel-text="取消"
          >
            {{ props.item.extraAward || "无" }}
            <template v-slot:input>
              <v-text-field
                :ref="'formExtraAward' + props.item.participantId"
                v-model="props.item.extraAward"
                :rules="[max20chars]"
                label="设置次要奖项名"
                hint="以空格分开多个次要奖项"
                single-line
                :counter="20"
              ></v-text-field>
            </template>
          </v-edit-dialog>
        </template>

        <template v-slot:no-data>
          <v-container> 暂无参赛者信息 </v-container>
        </template>
      </v-data-table>
    </v-card>

    <v-row justify="center">
      <v-dialog v-model="showAwardGenerateDialog" persistent max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">批量设置主要奖项</span>
          </v-card-title>
          <v-card-subtitle class="my-2">
            请设置得分段和该段对应的奖项名称，我们将自动为您批量填写。<br />
            目前仅支持识别得分为数值的类型，可按需要选择是否对未提交作品用户设置奖项。
          </v-card-subtitle>
          <v-card-text>
            <v-range-slider
              v-model="scoreRange"
              :max="scoreMax"
              :min="scoreMin"
              hide-details
              class="align-center"
            >
              <template v-slot:prepend>
                <v-text-field
                  :value="scoreRange[0]"
                  class="mt-0 pt-0"
                  hide-details
                  single-line
                  type="number"
                  style="width: 60px"
                  @change="$set(scoreRange, 0, $event)"
                ></v-text-field>
              </template>
              <template v-slot:append>
                <v-text-field
                  :value="scoreRange[1]"
                  class="mt-0 pt-0"
                  hide-details
                  single-line
                  type="number"
                  style="width: 60px"
                  @change="$set(scoreRange, 1, $event)"
                ></v-text-field>
              </template>
            </v-range-slider>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="blue darken-1"
              text
              @click="showAwardGenerateDialog = false"
            >
              Close
            </v-btn>
            <v-btn
              color="blue darken-1"
              text
              @click="showAwardGenerateDialog = false"
            >
              Save
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
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
    submitSheet(ref = undefined, item = undefined, finalSubmit = false) {
      console.log("selected form", ref, item);
      let updatedList = [];
      if (ref) {
        if (!this.$refs[ref].validate()) {
          this.participantList[item.index] = { ...this.backupList[item.index] };
          this.tableRefresh = true;
          this.$nextTick(() => {
            this.tableRefresh = false;
          });
          console.log(
            "what is going on",
            item,
            this.backupList[0],
            this.participantList[0]
          );
          this.snackbar("请按要求填写参数", "warning");
          return;
        } else {
          // Update backup list
          this.backupList[item.index] = { ...this.participantList[item.index] };
          updatedList = [this.participantList[item.index]];
        }
      } else {
        // Update backup list
        for (let i in this.participantList) {
          this.backupList[i] = { ...this.participantList[i] };
        }
        updatedList = this.participantList;
      }

      if (this.isSubmitting) return;
      this.isSubmitting = true;
      requestPost(
        {
          url: "/grade/submitsheet",
          data: {
            contestId: this.contestInfo.id,
            publish: finalSubmit ? 1 : 0,
            data: updatedList,
            count: updatedList.length,
          },
          responseType: "blob",
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isSubmitting = false;
          switch (res.data.error) {
            case undefined:
              this.snackbar("修改成功", "success");
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
          this.isSubmitting = false;
        });
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
          params.participantId = this.selected.map((v) => v.participantId);
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
    uploadSheet() {},
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
              for (let i in this.participantList) {
                this.participantList[i].index = Number(i);
              }
              this.backupList = this.participantList.map((v) => {
                return { ...v };
              });
              this.listLength = this.participantList.length;
              console.log(
                "hahaha",
                res.data,
                this.participantList,
                this.backupList
              );
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
  beforeRouteLeave(to, from, next) {
    //流程页  人为点击保存跳转页面   新增
    console.log("dasdasdas");
    if (true || (this.processPage && !this.manToSave && this.type == "add")) {
      console.log("hahaha");
      let issave = confirm("当前页面没有保存,是否确定要离开?");
      if (issave) {
        //确定
        next(true);
      } else {
        //取消
        next(false);
      }

      //自己写的弹窗是否保存   不用了
      // this.initPagination(next);
    }
  },
  created() {
    //TODO: FIXME: 判断具体日期和可选操作

    let currentTime = new Date().getTime();
    this.judgeStart =
      this.contestInfo.state["contest"][1] * 1000 <= currentTime;
    this.judgeCompleted = this.contestInfo.judgeCompleted;
    console.log(
      "info",
      this.contestInfo,
      this.judgeStart,
      this.contestInfo.state["contest"][1] * 1000,
      currentTime
    );
    this.fetchList();
  },
  data() {
    return {
      // 得分相关
      scoreMax: 300,
      scoreMin: 0,
      scoreRange: [0, 100],

      // 编辑相关
      max20chars: (v) => v.length <= 20 || "请不要超过20个字符",
      max12chars: (v) => v.length <= 12 || "请不要超过12个字符",
      max6chars: (v) => v.length <= 6 || "请不要超过6个字符",
      //   isNumber: (v) => isNumber(v) || "请输入成绩",
      showAwardGenerateDialog: false,
      tableRefresh: false,
      isSubmitting: false,
      isUploading: false,
      isDownloading: false,
      isLoading: true,
      judgeStart: false,
      judgeCompleted: false,
      participantList: [],
      backupList: [],
      selected: [],
      search: "",
      listLength: 0,
      headers: [
        { text: "编号", value: "participantId" },
        {
          text: this.contestInfo.allowGroup ? "团队名" : "姓名",
          value: "name",
        },
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