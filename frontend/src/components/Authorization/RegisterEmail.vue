<template>
  <v-card id="RegisterEmail">
    <v-card-title class="font-weight-black" style="font-size: 1.6em">
      {{ valid ? "验证" + email + "是你的邮箱地址" : "验证你的邮箱地址" }}
    </v-card-title>
    <v-divider> </v-divider>
    <v-card-subtitle class="font-weight-medium" style="font-size: 1.1em">
      {{
        valid
          ? "我们已向你的邮箱里发送了一封邮件，" +
            (isKnownHost
              ? "请点击下方按钮跳转到你的邮箱进行验证"
              : "请前往邮箱进行验证")
          : "我们无法找到你的邮箱地址，这可能是页面重新加载（如，手动刷新网页）导致的"
      }}
      <br />
      {{
        valid
          ? "如果你没能在收件箱里找到它，请检查垃圾箱或稍后再试。你也可以重新注册来发送新的验证邮件"
          : "但你仍然可以前往邮箱进行验证。如果你不确定自己是否注册过，也可以点击下方的按钮重新注册"
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
      <v-btn class="warning darken-1 my-4 mx-5" @click="redirect('/register')"
        >重新注册账号</v-btn
      >
      <v-spacer v-if="!isKnownHost"> </v-spacer>
    </v-card-actions>
  </v-card>
</template>

<script>
// 注册步骤2：要求用户查看邮箱
import merge from "webpack-merge";
import { hashtable } from "@/assets/constant.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { validationMixin } from "vuelidate";
import { required, email } from "vuelidate/lib/validators";
export default {
  name: "RegisterEmail",
  mixins: [redirect, snackbar, validationMixin],
  computed: {},
  components: {},
  validations: {
    email: { required, email },
  },
  methods: {},
  props: {
    email: String,
  },
  data() {
    return {
      valid: false,
      isKnownHost: false,
      hostname: "",
    };
  },
  mounted() {
    // 计算邮箱后缀，帮助用户快速跳转到对应的界面
    this.$v.$touch();
    this.valid = !this.$v.$invalid;
    if (this.valid) {
      this.hostname = this.email.split("@")[1];
      console.log(this.hostname);
      this.hostname =
        this.hostname in hashtable ? hashtable[this.hostname] : undefined;
      console.log(this.hostname);
      this.isKnownHost = !!this.hostname;
    }
  },
};
</script>