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
                    @click="submit()"
                    :loading="sendingForm"
                    :disabled="sendingForm"
                  >
                    确认
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
              <v-row>
                <v-card flat style="width: 80%; margin: auto">
                  <v-col>
                    <v-text-field
                      label="用户名"
                      v-model="username"
                      readonly
                    ></v-text-field>
                    <v-text-field
                      type="password"
                      label="密码"
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
import merge from "webpack-merge";
import { logState } from "@/mixins/logState.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { validationMixin } from "vuelidate";
import { required, email } from "vuelidate/lib/validators";
export default {
  name: "ResetPasswordPage",
  mixins: [redirect, snackbar, validationMixin],
  data() {
    return {
      sendingForm: false,
      email: "",
      step: this.$route.params.verifycode ? 3 : 1,
      valid: false,
      isKnownHost: false,
      hostname: "",
      username: "",
      password: "",
      confirmPassword: "",
      passwordRules: [
        //TODO: FIXME: RESUME HERE
      ],
      confirmPasswordRules: [],
    };
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
    submit() {
      this.$v.$touch();
      this.valid = !this.$v.$invalid;
      if (this.valid) {
        // TODO: 检查邮箱是否已经注册
        this.hostname = this.email.split("@")[1];
        console.log(this.hostname);
        this.hostname =
          this.hostname in hashtable ? hashtable[this.hostname] : undefined;
        console.log(this.hostname);
        this.isKnownHost = !!this.hostname;
      }

      if (this.$v.$invalid) {
        // this.$emit("update:email", "");
        // this.snackbar("请完整填写正确的信息", "error");
        this.sendingForm = false;
      } else {
        // do your submit logic here
        this.sendingForm = true;
        // simulating sending forms
        setTimeout(() => {
          this.sendingForm = false;
          this.step = 2;
          // this.$emit("update:email", this.email);
          // this.$router.replace({ path: "/register/emailcheck" });
        }, 1000);
      }
    },
    resetPassword() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        // this.$emit("update:email", "");
        // this.snackbar("请完整填写正确的信息", "error");
        this.sendingForm = false;
      } else {
        // do your submit logic here
        this.sendingForm = true;

        // simulating sending forms
        setTimeout(() => {
          this.sendingForm = false;
          // this.$emit("update:email", this.email);
          // this.$router.replace({ path: "/register/emailcheck" });
        }, 1000);
      }
    },
  },
};

const hashtable = {
  "qq.com": "http://mail.qq.com",
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
  "foxmail.com": "http://mail.qq.com",
  "outlook.com": "http://www.outlook.com",
};
</script>