<template>
  <v-container id="SubmissionManager">
    <v-card-title class="font-weight-black mb-3" style="font-size: 1.6em">
      管理 {{ contestInfo.title }} 的作品提交情况与获奖信息
    </v-card-title>
    <v-divider></v-divider>

    <div v-if="isLoading" id="skeleton_loaders">
      <v-skeleton-loader type="image" class="my-5"></v-skeleton-loader>
      <v-skeleton-loader type="heading" class="my-2"></v-skeleton-loader>
      <v-skeleton-loader type="list-item-avatar-three-line@3">
      </v-skeleton-loader>
    </div>
    <div v-else>
      <div v-if="participantList.length > 0">
        <v-card flat>
          <v-card-title>
            <v-file-input
              v-show="false"
              v-model="selectedCSV"
              accept=".csv"
              @change="uploadSheet"
              id="csvScoreUploader"
            />
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="输入信息以查找参赛者"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-card-title>
            <v-btn outlined :color="judgeCompleted ? 'success' : 'warning'">
              {{ judgeCompleted ? "竞赛已评奖" : "竞赛待评奖" }}</v-btn
            >
            <v-spacer></v-spacer>
            <v-btn
              class="info ml-2"
              @click="downloadFile(undefined, undefined, false)"
            >
              下载{{ selected && selected.length ? "选定" : "全部" }}作品
            </v-btn>
            <v-btn
              v-if="judgeCompleted"
              class="info ml-2"
              @click="downloadFile(undefined, undefined, true)"
            >
              下载{{ selected && selected.length ? "选定" : "全部" }}获奖证书
            </v-btn>
            <v-btn class="info ml-2" @click="downloadSheet"> 下载打分表 </v-btn>
            <v-btn
              v-if="!judgeCompleted"
              class="info ml-2"
              :loading="isUploading"
              @click="__triggerCSVUploader"
            >
              上传打分表
            </v-btn>
            <v-btn
              v-if="!judgeCompleted"
              class="info ml-2"
              @click="showAwardGenerateDialog = true"
            >
              批量填写奖项
            </v-btn>

            <v-btn
              v-if="judgeStart && !judgeCompleted"
              class="warning ml-2"
              @click="showPublishDialog = true"
            >
              发布成绩
            </v-btn>
          </v-card-title>
          <v-data-table
            :loading="isDownloading"
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
                v-if="item.actions.submission"
                class="mr-2"
                @click="downloadFile(item.participantId, item.name, false)"
              >
                cloud_download
              </v-icon>

              <v-icon
                v-if="item.actions.certificate"
                class="mr-2"
                @click="downloadFile(item.participantId, item.name, true)"
              >
                military_tech
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
                  submitSheet(
                    'formGrade' + props.item.participantId,
                    props.item
                  )
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
                    :readonly="judgeCompleted"
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
                    :readonly="judgeCompleted"
                    label="设置奖项名"
                    single-line
                    :counter="12"
                  ></v-text-field>
                </template>
              </v-edit-dialog>
            </template>

            <template v-slot:item.submitted="{ item }">
              <v-chip
                small
                :color="item.submitted ? 'success' : 'warning'"
                dark
              >
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
                    :readonly="judgeCompleted"
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
          <v-dialog
            v-model="showAwardGenerateDialog"
            persistent
            max-width="600px"
          >
            <v-card>
              <v-card-title>
                <span class="headline">批量设置主要奖项</span>
              </v-card-title>
              <v-card-subtitle class="my-2">
                请设置得分段和该段对应的奖项名称，我们将自动为您批量修改。<br />
                目前仅支持识别得分为数值的类型，可按需要选择是否对未提交作品用户设置奖项。<br />
                您可以依次对不同区间进行设置不同奖项。
              </v-card-subtitle>
              <v-card-text>
                <div>滑动下方的滑块以调整评分区间</div>
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

                <v-form ref="dialogAwardNameForm" class="mt-2">
                  <v-text-field
                    v-model="awardName"
                    :counter="12"
                    :rules="[max12chars]"
                    label="奖项名称"
                    placeholder="请输入奖项名称，留空代表删除奖项"
                  />
                </v-form>

                <v-switch
                  v-model="scoreForUnsubmitted"
                  inset
                  color="indigo"
                  :label="`${
                    scoreForUnsubmitted
                      ? '将为所有参赛者评分'
                      : '仅对提交文件的参赛者评分'
                  }`"
                ></v-switch>

                <div class="grey--text">
                  简而言之，您将进行如下更改：<br />
                  · 将得分在 {{ scoreRange[0] }} 到 {{ scoreRange[1] }} 之间的
                  {{ scoreForUnsubmitted ? "所有人" : "已提交文件的参赛者" }}
                  的主要奖项{{ awardName ? "设为" + awardName : "清空" }}<br />
                  · 不会影响其他参赛者的奖项设置
                </div>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="grey darken-1"
                  text
                  @click="showAwardGenerateDialog = false"
                >
                  取消
                </v-btn>

                <v-btn
                  color="info"
                  text
                  @click="applyScoreRules"
                  :loading="isSubmitting"
                >
                  确认修改
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-row>

        <v-row justify="center">
          <v-dialog v-model="showPublishDialog" persistent max-width="600px">
            <v-card>
              <v-card-title class="warning">
                <span class="headline white--text">发布最终成绩</span>
              </v-card-title>
              <v-card-text class="my-2">
                您将要最终发布该竞赛的成绩。一旦发布，您将不能再修改。<br />
                确实要发布吗？
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="grey darken-1"
                  text
                  @click="showPublishDialog = false"
                >
                  取消
                </v-btn>

                <v-btn
                  elevation="0"
                  color="error"
                  @click="submitSheet(undefined, undefined, true)"
                  :loading="isSubmitting"
                >
                  确认发布
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-row>
      </div>

      <v-card-title v-else> 该竞赛还没有参赛者 </v-card-title>
    </div>
  </v-container>
</template>

<script>
import merge from "webpack-merge";
import {
  requestPost,
  downloadFile,
  requestFormdata,
} from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "SubmissionManager",
  mixins: [redirect, snackbar, logState],
  methods: {
    getName(firstParticipant, count) {
      console.log("first part", firstParticipant, firstParticipant || "参赛者");
      if (count <= 0) {
        count = this.participantList.length;
        firstParticipant = this.participantList[0].name;
      }
      return (
        (firstParticipant || "参赛者") +
        (count > 1 ? "等" + count + "人的" : "的")
      );
    },
    applyScoreRules() {
      if (this.isSubmitting) return;
      if (!this.$refs.dialogAwardNameForm.validate()) {
        this.snackbar("您的参数不符合要求，请检查", "warning");
        return;
      }
      for (let i in this.participantList) {
        let score = this.participantList[i].grade;
        if (this.scoreRange[0] <= score && score <= this.scoreRange[1]) {
          if (this.scoreForUnsubmitted || this.participantList[i].submitted) {
            this.participantList[i].mainAward = this.awardName;
          }
        }
      }
      this.submitSheet();
    },
    submitSheet(ref = undefined, item = undefined, finalSubmit = false) {
      if (this.judgeCompleted) {
        this.snackbar("您不能修改已发布的竞赛成绩", "error");
        return;
      }
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
          updatedList = [this.participantList[item.index]];
        }
      } else {
        updatedList = this.participantList;
      }

      // if (this.isSubmitting) return;

      console.log("selected form", this.participantList, this.updatedList);
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
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isSubmitting = false;
          console.log("what is received after modified?", res.data);
          switch (res.data.error) {
            case undefined:
              this.snackbar("修改成功", "success");
              // Update backup list
              if (!ref) {
                for (let i in this.participantList) {
                  this.backupList[i] = { ...this.participantList[i] };
                }
              } else {
                this.backupList[item.index] = {
                  ...this.participantList[item.index],
                };
              }
              this.showAwardGenerateDialog = false;
              this.showPublishDialog = false
              break;
            case "login":
              this.clearLogInfo();
              break;
            default:
              this.snackbar("竞赛已发布成绩，修改失败", "error");
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再试", "error");
          console.log("error", err);
          this.isSubmitting = false;
        });
    },
    __generalDownloader(url, filename, params = {}, callback = undefined) {
      if (this.isDownloading) return;
      this.isDownloading = true;
      this.snackbar("正在从服务器获取文件，请稍候", "info");
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
          switch (res.data.error) {
            case undefined:
              this.snackbar("获取文件成功，即将保存到本地", "success");
              console.log("downloaded file is", res, res.data);
              downloadFile(res.data, "", filename);
              !callback || callback();
              this.isDownloading = false;
              break;
            case "login":
              this.clearLogInfo();
              break;
            default:
              this.snackbar(
                "哎呀，出错了，错误原因：" + res.data.error,
                "error"
              );
              this.isDownloading = false;
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再试", "error");
          console.log("error", err);
          this.isDownloading = false;
        });
    },
    downloadFile(
      participantId = undefined,
      name = undefined,
      isCertificate = false
    ) {
      if (this.isDownloading) return;
      let params = {
        count: 1,
        participantId: [participantId],
      };
      if (!participantId) {
        params.count = 0;
        delete params.participantId;
        if (this.selected.length < this.participantList.length) {
          params.participantId = this.selected.map((v) => v.participantId);
          params.count = params.participantId.length;
        }
      }
      console.log("selected", this.selected, params);
      this.__generalDownloader(
        isCertificate ? "/certification/get" : "/submit/submissions",
        this.getName(
          name || (this.selected.length ? this.selected[0].name : undefined),
          params.count
        ) + (isCertificate ? "获奖证书.zip" : "参赛作品.zip"),
        params
      );
    },
    __triggerCSVUploader() {
      if (this.isLoading || this.isUploading) return;
      document.getElementById("csvScoreUploader").click();
    },
    uploadSheet() {
      console.log("yes, and i am triggered", this.selectedCSV);
      if (this.selectedCSV.name.split(".").pop() != "csv") {
        this.snackbar("请选择有效的CSV文件", "error");
        this.selectedCSV = undefined;
        return;
      }
      if (this.selectedCSV.size > 2000000) {
        this.snackbar("CSV文件过大，请不要超过2MB", "error");
        this.selectedCSV = undefined;
        return;
      }
      this.isUploading = true;
      requestFormdata(
        {
          url: "/grade/upload",
          data: {
            contestId: this.contestInfo.id,
            fileKey: "file",
            file: this.selectedCSV,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isUploading = false;
          switch (res.data.error) {
            case undefined:
              this.snackbar("提交成功，正在刷新页面", "success");
              this.fetchList();
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
          this.isUploading = false;
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
        });
    },
    downloadSheet() {
      this.__generalDownloader(
        "/grade/download",
        this.contestInfo.title + "的打分表.csv"
      );
    },
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
                  actions: {
                    submission: v.submitted,
                    certificate:
                      this.judgeCompleted &&
                      (v.mainAward != "" || v.extraAward != ""),
                  },
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
  created() {
    let currentTime = new Date().getTime();
    this.judgeStart =
      this.contestInfo.state["contest"][1] * 1000 <= currentTime;
    this.judgeCompleted = !!this.contestInfo.judgeCompleted;
    console.log(
      "info",
      this.contestInfo,
      this.judgeStart,
      this.contestInfo.state["contest"][1] * 1000,
      currentTime,
      this.judgeCompleted
    );
    this.fetchList();
  },
  data() {
    return {
      // 发布相关
      showPublishDialog: false,
      selectedCSV: undefined,

      // 得分相关
      scoreMax: 300,
      scoreMin: 0,
      scoreRange: [0, 100],
      showAwardGenerateDialog: false,
      scoreForUnsubmitted: false,
      awardName: "",

      // 编辑相关
      max20chars: (v) => v.length <= 20 || "请不要超过20个字符",
      max12chars: (v) => v.length <= 12 || "请不要超过12个字符",
      max6chars: (v) => v.length <= 6 || "请不要超过6个字符",
      //   isNumber: (v) => isNumber(v) || "请输入成绩",

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