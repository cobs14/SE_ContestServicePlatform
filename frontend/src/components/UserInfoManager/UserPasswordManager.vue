<template>
  <v-card id="UserPasswordManager" class="ma-2 pa-2">
    <v-card-title v-if="!emailSent">重置密码</v-card-title>
    <v-card-subtitle v-if="!emailSent">
      如果您忘记了密码，可以点击下方按钮发送修改密码的链接。<br />
      我们将向您的下列邮箱发送重置密码邮件：
    </v-card-subtitle>
    <v-card-title v-if="!emailSent" style="font-weight: 800">
      {{ info.email }}
    </v-card-title>
    <v-card-title v-else style="font-weight: 800">
      已向 {{ info.email }} 发送邮件
    </v-card-title>
    <v-card-subtitle
      v-if="emailSent"
      class="font-weight-medium"
      style="font-size: 1em"
    >
      {{
        isKnownHost
          ? "请点击下方按钮跳转到您的邮箱进行密码重置"
          : "请前往邮箱点击链接进行密码重置"
      }}
      <br />
      {{ "如果您没能在收件箱里找到它，请检查垃圾箱或稍后再试。" }}
    </v-card-subtitle>
    <v-card-actions>
      <v-btn
        v-if="!emailSent"
        :loading="isSendingEmail"
        class="info ma-2"
        @click="sendEmail"
      >
        发送重置密码邮件
      </v-btn>
      <v-btn
        v-if="emailSent && isKnownHost"
        class="info ma-2"
        @click="external(hostname)"
        >前往{{ hostname.split("//")[1] }}
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn class="warning ma-2" @click="showPanel('passwordPanel', false)">
        关闭
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
// 用户重置密码组件（在个人中心）
import merge from "webpack-merge";
import { hashtable } from "@/assets/constant.js";
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "UserPasswordManager",
  inject: ["showPanel"],
  mixins: [redirect, snackbar, logState],
  methods: {
    // 发送重置密码的邮件
    sendEmail() {
      if (this.isSendingEmail || this.emailSent) return;
      this.hostname = this.info.email.split("@")[1];
      this.hostname =
        this.hostname in hashtable ? hashtable[this.hostname] : undefined;
      this.isKnownHost = !!this.hostname;
      this.isSendingEmail = true;
      requestPost({
        url: "/reset",
        data: {
          email: this.info.email,
        },
      })
        .then((res) => {
          this.isSendingEmail = false;
          switch (res.data.error) {
            case undefined:
              this.snackbar("发送成功，请在邮箱中查收邮件", "success");
              this.emailSent = true;
              break;
            default:
              this.snackbar("出错啦，错误原因：" + res.data.error, "error");
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再试", "error");
          this.isSendingEmail = false;
          console.log("error", err);
        });
    },
  },
  props: {
    info: Object,
  },
  data() {
    return {
      hostname: "",
      isKnownHost: false,
      emailSent: false,
      isSendingEmail: false,
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
