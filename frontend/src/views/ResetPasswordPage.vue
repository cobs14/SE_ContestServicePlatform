<template>
  <v-container id="ResetPasswordPage">
    <v-card-title class="font-weight-black" style="font-size: 1.6em">
      忘记密码
    </v-card-title>
    <v-stepper alt-labels :value="step">
      <v-stepper-header>
        <v-stepper-step step="1" :complete="1 < step">
          确认账号
        </v-stepper-step>
        <v-stepper-step step="2" :complete="2 < step">
          发送验证信
        </v-stepper-step>
        <v-stepper-step step="3"> 重置密码 </v-stepper-step>
      </v-stepper-header>
      <v-stepper-items>
        <v-stepper-content :step="1">
          <v-container>
            <v-row>
              <v-card flat style="width: 80%; margin: auto">
                <v-col>
                  <v-text-field
                    label="请输入绑定的电子邮箱地址"
                    v-model="email"
                    :error-messages="emailErrors"
                    @input="$v.email.$touch()"
                    @blur="$v.email.$touch()"
                  ></v-text-field>
                </v-col>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    class="info ma-2"
                    @click="sendResetEmail()"
                    :loading="sendingEmail"
                    :disabled="sendingEmail"
                  >
                    发送邮件
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-row>
          </v-container>
        </v-stepper-content>
        <v-stepper-content :step="2">
          <v-container>
            <v-row>
              <v-card flat style="width: 80%; margin: auto">
                <v-card-title
                  class="font-weight-black"
                  style="font-size: 1.6em"
                >
                  {{
                    valid
                      ? "我们已经发送重置密码链接到" + email
                      : "我们已经发送重置密码链接到您的邮箱地址"
                  }}
                </v-card-title>
                <v-divider> </v-divider>
                <v-card-subtitle
                  class="font-weight-medium"
                  style="font-size: 1.1em"
                >
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
                  <v-btn
                    class="warning darken-1 my-4 mx-5"
                    @click="softReload()"
                    >重新输入邮箱</v-btn
                  >
                  <v-spacer v-if="!isKnownHost"> </v-spacer>
                </v-card-actions>
              </v-card>
            </v-row>
          </v-container>
        </v-stepper-content>
        <v-stepper-content :step="3">
          <v-card>
            <v-container>
              <v-card-title style="font-weight: 800">
                重设{{ username }}的密码
              </v-card-title>
              <v-row>
                <v-card flat style="width: 80%; margin: auto">
                  <v-col>
                    <v-form ref="passwordForm">
                      <v-text-field
                        type="password"
                        label="设置新密码"
                        v-model="password"
                        :counter="20"
                        :rules="passwordRules"
                      ></v-text-field>
                      <v-text-field
                        type="password"
                        label="再次输入密码"
                        v-model="confirmPassword"
                        :counter="20"
                        :rules="confirmPasswordRules"
                      ></v-text-field>
                    </v-form>
                  </v-col>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      class="info ma-2"
                      @click="resetPassword()"
                      :loading="sendingForm"
                      :disabled="sendingForm"
                    >
                      确认修改
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-row>
            </v-container>
          </v-card>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </v-container>
</template>

<script>
// 重置密码页面
import merge from "webpack-merge";
import { hashtable } from "@/assets/constant.js";
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { validationMixin } from "vuelidate";
import { required, email } from "vuelidate/lib/validators";
export default {
  name: "ResetPasswordPage",
  inject: ["softReload"],
  mixins: [redirect, snackbar, validationMixin],
  data() {
    return {
      sendingEmail: false,
      sendingForm: false,
      email: "",
      step: 1,
      valid: false,
      verifyCode: "",
      isKnownHost: false,
      hostname: "",
      username: "",
      password: "",
      confirmPassword: "",
      passwordRules: [
        (v) => !!v || "请输入密码",
        (v) =>
          !v ||
          (6 <= v.length && v.length <= 20) ||
          "密码长度应该介于6~20个字符",
      ],
      confirmPasswordRules: [
        (v) => !!v || "请再次输入密码以确认",
        (v) => !v || v == this.password || "两次输入的密码不一致",
      ],
    };
  },
  created() {
    this.step = this.$route.params.verifycode ? 3 : 1;
    if (this.step == 3) {
      // 需要验证verifyCode的有效性
      this.verifyCode = this.$route.params.verifycode;
      requestPost({
        url: "/reset/code",
        data: {
          code: this.verifyCode,
        },
      })
        .then((res) => {
          if (res.data.error == undefined) {
            this.username = res.data.username;
          } else {
            this.snackbar("验证链接无效或已过期，请重试", "error");
            this.softReload("/resetpassword");
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再试", "error");
          this.softReload("/resetpassword");
        });
    }
  },
  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("输入的邮箱地址无效");
      !this.$v.email.required && errors.push("请输入邮箱地址");
      return errors;
    },
  },
  components: {},
  validations: {
    email: { required, email },
  },
  methods: {
    // 发送重置密码的邮件
    sendResetEmail() {
      this.$v.$touch();
      this.valid = !this.$v.$invalid;
      if (!this.valid) {
        this.snackbar("请填写正确的邮箱地址", "error");
        this.sendingEmail = false;
      } else {
        this.hostname = this.email.split("@")[1];
        this.hostname =
          this.hostname in hashtable ? hashtable[this.hostname] : undefined;
        this.isKnownHost = !!this.hostname;
        this.sendingEmail = true;
        requestPost({
          url: "/reset",
          data: {
            email: this.email,
          },
        })
          .then((res) => {
            this.sendingEmail = false;
            switch (res.data.error) {
              case undefined:
                this.step = 2;
                break;
              default:
                this.snackbar("这个邮件地址没有对应的账号", "error");
            }
          })
          .catch((err) => {
            this.snackbar("服务器开小差啦，请稍后再试", "error");
            this.sendingEmail = false;
            console.log("error", err);
          });
      }
    },
    // 重置密码页面
    resetPassword() {
      if (!this.$refs.passwordForm.validate()) {
        this.snackbar("请完整填写正确的信息", "error");
        this.sendingForm = false;
      } else {
        this.sendingForm = true;
        requestPost({
          url: "/reset/password",
          data: {
            code: this.verifyCode,
            password: this.$md5(this.password),
          },
        })
          .then((res) => {
            this.sendingForm = false;
            switch (res.data.error) {
              case undefined:
                this.snackbar("修改密码成功，请重新登录", "success");
                this.softReload("/login");
                break;
              default:
                this.snackbar("出错啦，错误原因：" + res.data.error, "error");
                this.softReload("/resetpassword");
            }
          })
          .catch((err) => {
            this.snackbar("服务器开小差啦，请稍后再试", "error");
            this.sendingForm = false;
            this.softReload();
            console.log("error", err);
          });
      }
    },
  },
};
</script>