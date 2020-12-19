<template>
  <v-card id="RegisterVerification">
    <div v-if="!received">
      <v-card-title class="font-weight-black" style="font-size: 1.6em">
        正在验证您的邮箱
      </v-card-title>
      <v-divider> </v-divider>
      <v-skeleton-loader
        class="mx-auto"
        type="article, actions"
      ></v-skeleton-loader>
    </div>
    <div v-if="received">
      <v-card-title class="font-weight-black" style="font-size: 1.6em">
        {{ valid ? "验证成功，欢迎加入Contest+" : "无效的验证链接" }}
      </v-card-title>
      <v-divider> </v-divider>
      <v-card-subtitle
        v-if="valid"
        class="font-weight-medium"
        style="font-size: 1.1em"
      >
        我们将在3秒内为您跳转到登录页面
        <br />
        如果页面没有跳转，您也可以手动点击下方按钮进入登录页面
      </v-card-subtitle>
      <v-card-subtitle
        v-if="!valid"
        class="font-weight-medium"
        style="font-size: 1.1em"
      >
        我们无法确认这是一个有效的验证链接，这也许是下列原因导致的：
        <br />
        · 链接已过期
        <br />
        · 您重新注册了账户，但没有使用最新的验证链接
        <br />
        · 您输入了错误的链接地址或没有完整复制它
        <br />
        如果您不知道该怎么做，也可以点击下方的按钮重新注册
      </v-card-subtitle>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          class="warning darken-1 my-4 mx-5"
          @click="redirect('/register')"
          v-if="!valid"
        >
          重新注册账号
        </v-btn>
        <v-btn
          class="success my-4 mx-2"
          @click="redirect('/login')"
          v-if="valid"
        >
          探索Contest+
        </v-btn>
        <v-spacer> </v-spacer>
      </v-card-actions>
    </div>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { requestPost } from "@/network/request.js";
export default {
  name: "RegisterVerification",
  mixins: [redirect, snackbar],
  computed: {},
  components: {},
  methods: {
    verify() {
      //todo: 在这里发送请求和修改valid值即可。
      requestPost({
        url: "register/verifymail",
        data: {
          code: this.$route.params.verifycode,
        },
      })
        .then((res) => {
          this.received = true;
          console.log("ok", res, res.data, res.data.message, res.data.error);
          if (res.data.message != undefined) {
            this.valid = true;
            setTimeout(() => {
              this.redirect("/login");
            }, 3000);
            //TODO: Back to login page
          } else {
            this.valid = false;
            this.snackbar("出错啦，错误原因：" + res.data.error, "error");
          }
        })
        .catch((err) => {
          this.received = true;
          this.valid = false;
          this.snackbar("服务器开小差啦，请稍后再试", "error");
          console.log("error", err);
        });
    },
  },
  props: {
    email: String,
  },
  data() {
    return {
      valid: false,
      received: false,
    };
  },
  mounted() {
    this.verify();
    console.log("verifycode is ", this.$route.params.verifycode);
  },
};
</script>