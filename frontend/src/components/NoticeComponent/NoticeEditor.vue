<template>
  <v-container id="NoticeEditor">
    <v-form ref="form" :disabled="isLoading">
      <v-text-field
        v-if="editMode"
        label="您正在编辑的公告ID"
        disabled
        v-model="updatedNotice.noticeId"
      />
      <v-switch
        v-model="updatedNotice.participantOnly"
        :label="`可见性：${
          updatedNotice.participantOnly ? '仅参赛者可见' : '所有人可见'
        }`"
      ></v-switch>
      <v-text-field
        label="公告标题"
        clearable
        :rules="titleRules"
        counter="128"
        v-model="updatedNotice.title"
      />
      <v-textarea
        label="公告正文"
        clearable
        :rules="contentRules"
        counter="512"
        v-model="updatedNotice.content"
      />
      <v-text-field
        label="附加链接（留空代表无链接）"
        clearable
        :rules="linkRules"
        counter="512"
        v-model="updatedNotice.link"
      >
      </v-text-field>
      <v-switch
        v-if="!editMode || !hasOriginalFile"
        v-model="hasNewFile"
        :label="`${hasNewFile ? '请选择新的附件' : '公告将不包含任何附件'}`"
      ></v-switch>
      <v-switch
        v-if="editMode && hasOriginalFile"
        v-model="hasNewFile"
        :label="`${hasNewFile ? '请选择新的附件' : '将保留原始附件'}`"
      ></v-switch>
      <v-file-input
        v-if="hasNewFile"
        v-model="selectedFile"
        :rules="fileRules"
        show-size
        placeholder="点击此处选择附件（留空将删除任何已有附件）"
        label="公告附件"
      >
      </v-file-input>
    </v-form>
    <v-card-actions disabled>
      <v-btn
        @click="submit"
        class="info"
        :loading="isLoading"
        :disabled="isLoading"
        >确认</v-btn
      >
      <v-btn @click="cancel" :disabled="isLoading">取消</v-btn>
    </v-card-actions>
  </v-container>
</template>

<script>
// 公告编辑器
import { requestPost, requestFormdata } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "NoticeEditor",
  mixins: [redirect, snackbar, filter, logState],
  methods: {
    // 提交编辑后的公告
    // 需要计算是否有新文件和新链接
    submit() {
      if (this.$refs.form.validate()) {
        this.isLoading = true;
        if (this.editMode) {
          this.updatedNotice.modifiedFile = this.hasNewFile;
        }
        if (this.hasNewFile && this.selectedFile instanceof File) {
          this.updatedNotice.fileKey = "file";
          this.updatedNotice.file = this.selectedFile;
        } else {
          this.updatedNotice.fileKey = "";
          delete this.updatedNotice.file;
        }
        requestFormdata(
          {
            url: this.editMode ? "/notice/modify" : "/notice/new",
            data: this.updatedNotice,
          },
          this.getUserJwt()
        )
          .then((res) => {
            this.isLoading = false;
            switch (res.data.error) {
              case undefined:
                this.snackbar("提交成功", "success");
                this.$emit("onEditComplete", this.editMode, false);
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
            this.isLoading = false;
            this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
            console.log("error", err);
          });
      } else {
        this.snackbar("您填写的表单有误，请更正", "warning");
      }
    },
    cancel() {
      this.$emit("onEditComplete", this.editMode, true);
    },
  },
  data() {
    return {
      isLoading: false,
      updatedNotice: Object,
      hasOriginalFile: false,
      hasNewFile: false,
      selectedFile: undefined,
      fileRules: [
        (value) =>
          !value || value.size < 500000000 || "您上传的文件大小最多为500MB.",
      ],
      titleRules: [
        (value) => !!value || "请不要输入空内容",
        (value) => !value || value.length < 128 || "标题最长为128个字符",
      ],
      contentRules: [
        (value) => !!value || "请不要输入空内容",
        (value) => !value || value.length < 512 || "正文最长为512个字符",
      ],
      linkRules: [
        (value) => !value || value.length < 512 || "链接最长为512个字符",
      ],
    };
  },
  // 根据不同的模式决定编辑器要显示的内容
  created() {
    if (this.editMode) {
      let { ...tmpNotice } = this.notice;
      this.updatedNotice = tmpNotice;
      this.hasOriginalFile = !!this.notice.hasFile;
    } else {
      delete this.updatedNotice.noticeId;
      this.updatedNotice.contestId = this.contestId;
    }
    this.updatedNotice = this.getNoticeFilter(this.updatedNotice);
    delete this.updatedNotice.hasFile;
  },
  props: {
    notice: Object,
    editMode: false,
    contestId: 0,
  },
};
</script>

<style>
</style>