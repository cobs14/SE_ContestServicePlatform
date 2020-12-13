<template>
  <div id="ContestGroupInfo">
    <v-card-title style="font-weight: 800"
      >{{ submitted ? "管理" : "提交" }}您的参赛作品</v-card-title
    >

    <v-card-text>
      <div class="grey--text">
        请按照竞赛主办方发布的要求提交参赛作品文件，<br />
        如果您需要提交多个文件，请将其打包为压缩包。
      </div>
    </v-card-text>

    <v-card-text>
      <div>提交状态</div>
      <div class="grey--text" v-if="!submitted">您当前未提交任何作品</div>
      <div class="grey--text" v-if="submitted">已提交</div>
      <div class="grey--text" v-if="submitted">
        文件名：{{ userSubmission.filename }}
      </div>
      <div class="grey--text" v-if="submitted">
        文件大小：{{ userSubmission.fileSize }}字节
      </div>
    </v-card-text>

    <v-card-text v-if="submitted">
      <div>管理作品</div>
      <v-row class="pa-2">
        <v-btn
          v-if="!needUploadFile"
          @click="setNeedUploadFile(true)"
          class="info mx-1"
          >修改文件</v-btn
        >
        <v-btn
          v-if="needUploadFile"
          @click="setNeedUploadFile(false)"
          class="warning mx-1"
          >取消修改</v-btn
        >
        <v-btn @click="downloadFile" class="info" :loading="isDownloading"
          >下载文件</v-btn
        >
        <v-spacer></v-spacer>
        <v-btn @click="submit(false)" class="error" dark>删除文件</v-btn>
      </v-row>
    </v-card-text>

    <v-card-text>
      <div v-if="needUploadFile">提交作品文件</div>
      <v-form ref="form">
        <v-file-input
          v-if="needUploadFile"
          v-model="selectedFile"
          :rules="fileRules"
          show-size
          label="点此选择要上传的文件"
        />
      </v-form>
    </v-card-text>

    <v-card-actions>
      <v-btn
        v-if="needUploadFile"
        class="info"
        @click="submit"
        :loading="isSubmitting"
      >
        提交
      </v-btn>
      <v-spacer />
      <v-btn depressed @click="closePage">关闭此页面</v-btn>
    </v-card-actions>
  </div>
</template>

<script>
import {
  requestPost,
  downloadFile,
  requestFormdata,
} from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "ContestGroupInfo",
  mixins: [redirect, snackbar, filter, logState],
  inject: ["softReload"],
  watch: {},
  methods: {
    setNeedUploadFile(needed = true) {
      this.needUploadFile = needed;
      if (!needed) {
        this.selectedFile = undefined;
      }
    },
    isProcessing() {
      return this.isSubmitting || this.isDownloading;
    },
    downloadFile() {
      if (this.isProcessing()) return;
      this.isDownloading = true;
      requestPost(
        {
          url: "/submit/download",
          data: {
            contestId: this.formParams.contestId,
            participantId: this.formParams.participantId,
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
              console.log(
                "downloaded file is",
                res,
                res.data,
                res.headers["content-disposition"].split(".")
              );
              // let suffix = res.headers["content-disposition"].split(".").pop();
              downloadFile(res.data, "", this.userSubmission.filename);
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
    submit(saveFile = true) {
      if (this.isProcessing()) return;
      if (!saveFile) {
        this.setNeedUploadFile(false);
      }
      if (this.$refs.form.validate()) {
        this.isSubmitting = true;
        if (this.selectedFile instanceof File) {
          this.formParams.fileKey = "file";
          this.formParams.file = this.selectedFile;
        } else {
          this.formParams.fileKey = "";
          delete this.formParams.file;
        }

        //TODO: FIXME: resume here
        // we need to send request here.
        console.log(
          "mode is",
          this.needUploadFile,
          " and we gonna send:",
          this.formParams
        );
        requestFormdata(
          {
            url: "/submit/upload",
            data: this.formParams,
          },
          this.getUserJwt()
        )
          .then((res) => {
            this.isSubmitting = false;
            switch (res.data.error) {
              case undefined:
                this.snackbar("提交成功", "success");
                this.softReload();
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
            this.isSubmitting = false;
            this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
            console.log("error", err);
          });
        console.log("yes! validate ", this.formParams);
      } else {
        this.snackbar("您填写的表单有误，请更正", "warning");
      }
    },
    closePage() {
      this.$emit("close");
    },
  },
  data() {
    return {
      formParams: {
        contestId: 0,
        participantId: 0,
        fileKey: "",
        file: undefined,
      },
      isDownloading: false,
      isSubmitting: false,
      submitted: false,
      needUploadFile: false,
      selectedFile: undefined,
      fileRules: [
        (v) => !!v || "请不要提交空文件",
        (v) => !v || v.size < 50000000 || "请勿提交超过大小50MB的文件",
      ],
    };
  },
  created() {
    this.submitted = this.userSubmission != undefined;
    this.needUploadFile = !this.submitted;
    this.formParams.participantId = this.getUserId();
    this.formParams.contestId = this.contestId;
  },
  props: {
    userSubmission: Object,
    contestId: Number,
  },
};
</script>

<style>
</style>