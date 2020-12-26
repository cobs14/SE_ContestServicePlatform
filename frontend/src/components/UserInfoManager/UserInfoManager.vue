<template>
  <v-card id="UserInfoManager" class="ma-2 pa-2">
    <v-card-title>修改您的个人信息</v-card-title>
    <v-card-subtitle>
      您可以修改自己的联系方式等信息。<br />
      已验证的身份信息从学信网获得，不可编辑。如果您有疑问，请联系管理员。
    </v-card-subtitle>
    <v-container class="pa-4">
      <v-form ref="form">
        <v-text-field
          v-model="params.mobile"
          label="手机号"
          placeholder="在此处输入您的手机号"
          :rules="mobileRules"
          :counter="32"
        />
        <v-text-field
          v-model="params.address"
          label="联系地址"
          placeholder="在此处输入您的联系地址"
          :rules="addressRules"
          :counter="128"
        />
        <v-textarea
          v-model="params.description"
          label="个人简介"
          placeholder="在此处输入您的个人简介"
          :rules="descriptionRules"
          :counter="256"
        />
      </v-form>
    </v-container>
    <v-card-actions>
      <v-btn :loading="isSubmitting" class="info ma-2" @click="submit">
        确认修改
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn class="warning ma-2" @click="showPanel('infoPanel', false)">
        关闭
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
// 用户信息编辑器（在个人中心）
import merge from "webpack-merge";
import { hashtable } from "@/assets/constant.js";
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "UserInfoPanel",
  inject: ["showPanel"],
  mixins: [redirect, snackbar, logState],
  methods: {
    // 提交修改后的表单信息
    submit() {
      if (this.isSubmitting) return;
      if (!this.$refs.form.validate()) {
        this.snackbar("请按要求填写全部信息", "warning");
        return;
      }
      this.isSubmitting = true;
      requestPost(
        {
          url: "/user/information",
          data: { ...this.params },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isSubmitting = false;
          switch (res.data.error) {
            case undefined:
              this.snackbar("修改个人信息成功", "success");
              this.softReload();
              break;
            default:
              this.snackbar("出错啦，错误原因：" + res.data.error, "error");
          }
        })
        .catch((err) => {
          this.isSubmitting = false;
          this.snackbar("服务器开小差啦，请稍后再试", "error");
          console.log("error", err);
        });
    },
  },
  created() {
    // 预填写用户已有的信息
    this.params.mobile = this.info.mobile;
    this.params.address = this.info.address;
    this.params.description = this.info.description;
  },
  props: {
    info: Object,
  },
  data() {
    return {
      params: {
        mobile: "",
        address: "",
        description: "",
      },
      // 表单验证规则
      mobileRules: [
        (v) => !!v || "手机号不能为空",
        (v) => !v || v.length <= 32 || "手机号不能超过32个字符",
      ],
      addressRules: [
        (v) => !!v || "联系地址不能为空",
        (v) => !v || v.length <= 128 || "联系地址不能超过128个字符",
      ],
      descriptionRules: [
        (v) => !!v || "个人简介不能为空",
        (v) => !v || v.length <= 256 || "个人简介不能超过256个字符",
      ],
      isSubmitting: false,
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
