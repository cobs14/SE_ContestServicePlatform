<template>
  <v-card class="ma-2 pa-2">
    <v-container>
      <v-col>
        <v-radio-group v-model="type" row>
          <v-radio label="文字" value="text"></v-radio>
          <v-radio label="图片" value="picture"></v-radio>
        </v-radio-group>
      </v-col>
      <v-container v-if="type === 'text'">
        <v-text-field
          label="详情标题"
          outlined
          v-model="descriptionTitle"
          :counter="64"
          :error-messages="descriptionTitleErrors"
          @input="$v.descriptionTitle.$touch()"
          @blur="$v.descriptionTitle.$touch()"
        >
        </v-text-field>
        <v-textarea
          label="详情内容"
          outlined
          v-model="descriptionContent"
          :counter="2048"
          :error-messages="descriptionContentErrors"
          @input="$v.descriptionContent.$touch()"
          @blur="$v.descriptionContent.$touch()"
        ></v-textarea>
      </v-container>
      <v-container v-if="type === 'picture'">
        <v-file-input
          v-model="descriptionPicture"
          :rules="pictureRules"
          required
          show-size
          accept="image/*"
          placeholder="点击此处选择要上传的图片"
          label="详细信息图片"
          prepend-icon="mdi-camera"
        >
        </v-file-input>
      </v-container>
      <v-row>
        <v-spacer></v-spacer>
        <v-btn class="error ma-2" @click="deleteDescription()">删除</v-btn>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { validationMixin } from "vuelidate";
import { required, maxLength } from "vuelidate/lib/validators";
export default {
  name: "DescriptionCard",
  validations: {
    descriptionTitle: {
      required,
      maxLength: maxLength(64),
    },
    descriptionContent: {
      required,
      maxLength: maxLength(2048),
    },
  },
  computed: {
    descriptionTitleErrors() {
      const errors = [];
      if (!this.$v.descriptionTitle.$dirty) return errors;
      !this.$v.descriptionTitle.required && errors.push("请输入详情标题");
      !this.$v.descriptionTitle.maxLength &&
        errors.push("详情标题至多64个字符");
      return errors;
    },
    descriptionContentErrors() {
      const errors = [];
      if (!this.$v.descriptionContent.$dirty) return errors;
      !this.$v.descriptionContent.required && errors.push("请输入详情内容");
      !this.$v.descriptionContent.maxLength &&
        errors.push("详情内容至多2048个字符");
      return errors;
    },
  },
  watch: {
    type: function (newVal, oldVal) {
      this.$emit("content-change", {
        index: this.index,
        type: this.type,
        title: this.descriptionTitle,
        content: this.descriptionContent,
        selectedPicture: this.descriptionPicture,
      });
    },
    descriptionTitle: function (newVal, oldVal) {
      this.$emit("content-change", {
        index: this.index,
        type: this.type,
        title: this.descriptionTitle,
        content: this.descriptionContent,
        selectedPicture: this.descriptionPicture,
      });
    },
    descriptionContent: function (newVal, oldVal) {
      this.$emit("content-change", {
        index: this.index,
        type: this.type,
        title: this.descriptionTitle,
        content: this.descriptionContent,
        selectedPicture: this.descriptionPicture,
      });
    },
    descriptionPicture: function (newVal, oldVal) {
      this.$emit("content-change", {
        index: this.index,
        type: this.type,
        title: this.descriptionTitle,
        content: this.descriptionContent,
        selectedPicture: this.descriptionPicture,
      });
    },
  },
  methods: {
    deleteDescription() {
      this.$emit("delete-description", { index: this.index });
    },
  },
  props: {
    index: Number,
  },
  data() {
    return {
      type: "text",
      descriptionTitle: "",
      descriptionContent: "",
      descriptionPicture: [],
      pictureRules: [
        (value) => !!value || "您不能上传空文件",
        (value) => value.size < 5000000 || "您上传的图片大小最多为5MB.",
      ],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
