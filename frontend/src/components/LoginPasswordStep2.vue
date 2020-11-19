<template>
  <v-container>
  <v-row>
  <v-card flat style="width: 80%; margin: auto">
      <v-card-title class="font-weight-black" style="font-size: 1.6em">
        {{ valid ? "我们已经发送重置密码链接到" + email : "我们已经发送重置密码链接到您的邮箱地址" }}
      </v-card-title>
      <v-divider> </v-divider>
      <v-card-subtitle class="font-weight-medium" style="font-size: 1.1em">
        {{
          valid
            ? "我们已向您的邮箱里发送了一封邮件，" +
              (isKnownHost
                ? "请点击下方按钮跳转到您的邮箱进行密码重置"
                : "请前往邮箱点击链接进行密码重置")
            : "我们无法找到您的邮箱地址，这可能是页面重新加载（如，手动刷新网页）导致的"
        }}
        <br />
        {{
          valid
            ? "如果您没能在收件箱里找到它，请检查垃圾箱或稍后再试。"
            : "但您仍然可以前往邮箱检查。如果您不确定自己是否注册过，也可以点击下方的按钮重新注册"
        }}
      </v-card-subtitle>
      <v-card-actions>
        <v-btn
          class="info my-4 mx-2"
          @click="external(hostname)"
          v-if="isKnownHost"
          >前往{{ hostname.split("//")[1] }}
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn class="warning darken-1 my-4 mx-5" @click="$emit('update:passstep', 1)"
          >重新输入邮箱</v-btn
        >
        <v-spacer v-if="!isKnownHost"> </v-spacer>
      </v-card-actions>
  </v-card>
  </v-row>
  </v-container>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { validationMixin } from "vuelidate";
import {
  required,
  email,
  minLength,
  maxLength,
  sameAs
} from "vuelidate/lib/validators";
export default {
  name: "LoginPasswordStep2",
  mixins: [redirect, snackbar, validationMixin],
  props: {
      email: String,
  },
  data() {
    return {
      valid: true,
      isKnownHost: false,
      hostname: "",
    };
  },
  computed: {},
  components: {},
  methods: {},
  mounted() {
    this.hostname = this.email.split("@")[1];
    this.hostname =
      this.hostname in hashtable ? hashtable[this.hostname] : undefined;
    this.isKnownHost = !!this.hostname;
  }
};

const hashtable = {
  "qq.com": "http://mail.qq.com",
  "vip.qq.com": "http://mail.qq.com",
  "gmail.com": "http://mail.google.com",
  "sina.com": "http://mail.sina.com.cn",
  "163.com": "http://mail.163.com",
  "126.com": "http://mail.126.com",
  "yeah.net": "http://www.yeah.net/",
  "sohu.com": "http://mail.sohu.com/",
  "tom.com": "http://mail.tom.com/",
  "sogou.com": "http://mail.sogou.com/",
  "139.com": "http://mail.10086.cn/",
  "hotmail.com": "http://www.hotmail.com",
  "live.com": "http://login.live.com/",
  "live.cn": "http://login.live.cn/",
  "live.com.cn": "http://login.live.com.cn",
  "189.com": "http://webmail16.189.cn/webmail/",
  "yahoo.com.cn": "http://mail.cn.yahoo.com/",
  "yahoo.cn": "http://mail.cn.yahoo.com/",
  "eyou.com": "http://www.eyou.com/",
  "21cn.com": "http://mail.21cn.com/",
  "188.com": "http://www.188.com/",
  "foxmail.com": "http://www.foxmail.com",
  "outlook.com": "http://www.outlook.com",
};
</script>