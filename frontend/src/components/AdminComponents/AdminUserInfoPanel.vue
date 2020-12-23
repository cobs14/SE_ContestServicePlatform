<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      {{ info.username }}
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-card-text>
        用户名：{{ info.username }}<br />
        用户ID：{{ info.userId }}
      </v-card-text>
      <v-switch
        v-model="params.valid"
        inset
        color="indigo"
        value="indigo"
        :label="`验证结果：${params.valid ? '通过' : '拒绝'}`"
      ></v-switch>
      <v-form ref="form">
        <v-text-field
          v-model="params.comment"
          label="审核意见"
          placeholder="请在此填写审核意见"
          :rules="maxLengthRules"
          single-line
          :counter="64"
        />
        <div v-if="params.valid">
          <v-card-subtitle>请在下方填写用户实名信息</v-card-subtitle>
          <v-text-field
            v-model="params.trueName"
            label="真实姓名"
            placeholder="请在此填写真实姓名"
            :rules="maxLengthRules"
            single-line
            :counter="64"
          />

          <v-text-field
            v-model="params.school"
            label="就读院校"
            placeholder="请在此填写就读院校"
            :rules="maxLengthRules"
            single-line
            :counter="64"
          />

          <v-text-field
            v-model="params.major"
            label="主修专业"
            placeholder="请在此填写主修专业"
            :rules="maxLengthRules"
            single-line
            :counter="64"
          />

          <v-text-field
            v-model="params.documentId"
            label="证件号码"
            placeholder="请在此填写证件号码"
            :rules="maxLengthRules"
            single-line
            :counter="64"
          />
        </div>
      </v-form>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="info mx-3" @click="downloadFile" :loading="isDownloading">
          获取验证文件
        </v-btn>
        <v-btn
          :class="params.valid ? 'success' : 'error'"
          @click="sendForm"
          :loading="isSubmitting"
        >
          提交审核结果
        </v-btn>
      </v-card-actions>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import { requestPost, downloadFile } from "@/network/request.js";
import { snackbar } from "@/mixins/message.js";
import { redirect } from "@/mixins/router.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "AdminContestPanel",
  mixins: [snackbar, redirect, logState],
  components: {},
  methods: {
    downloadFile() {
      if (this.isDownloading) return;
      this.isDownloading = true;
      requestPost(
        {
          url: "/qualification/file",
          data: {
            userId: this.info.userId,
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
              downloadFile(
                res.data,
                "",
                this.info.userId +
                  "_" +
                  this.info.username +
                  "_" +
                  this.info.filename +
                  "_" +
                  this.info.fileType
              );
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
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
          this.isDownloading = false;
        });
    },
    sendForm(status) {
      if (this.isSubmitting) return;
      if (!this.$refs.form.validate()) {
        this.snackbar("请填写正确的信息", "error");
        return;
      }
      this.isSubmitting = true;
      requestPost(
        {
          url: "/qualification/verify",
          data: this.params,
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isSubmitting = false;
          switch (res.data.error) {
            case undefined:
              this.snackbar("提交成功", "success");
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
          this.isSubmitting = false;
        });
    },
  },
  created() {
    this.params.userId = this.info.userId;
  },
  props: {
    info: Object,
  },
  data() {
    return {
      params: {
        comment: "",
        userId: "",
        valid: 0,
        trueName: "",
        school: "",
        major: "",
        documentId: "",
      },
      isDownloading: false,
      isSubmitting: false,
      maxLengthRules: [(v) => !v || v.length <= 64 || "请勿超过64个字符"],
    };
  },
  computed: {},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
