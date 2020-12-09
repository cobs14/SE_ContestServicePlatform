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
        v-if="editMode"
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
        prepend-icon="mdi-camera"
        @change="showFile"
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
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { filter } from "@/mixins/filter.js";
export default {
  name: "NoticeEditor",
  mixins: [redirect, filter, redirect],
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
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

        console.log("yes! validate ", this.updatedNotice);
      } else {
        console.log("nono!! not validate");
      }
    },
    cancel() {
      console.log("todo: we will cancel this later");
    },
    showFile() {
      console.log("show file", this.selectedFile);
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
          !value || value.size < 50000000 || "您上传的文件大小最多为50MB.",
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
  created() {
    if (this.editMode) {
      let { ...tmpNotice } = this.notice;
      console.log();
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