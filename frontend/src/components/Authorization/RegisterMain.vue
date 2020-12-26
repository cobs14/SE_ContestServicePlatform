<template>
  <v-card id="RegisterMain">
    <v-card-title class="font-weight-black" style="font-size: 1.6em">
      注册新用户
    </v-card-title>
    <v-tabs v-model="tab">
      <v-tab v-for="item in items" :key="item.tab">
        {{ item.tab }}
      </v-tab>
    </v-tabs>
    <v-divider> </v-divider>
    <v-tabs-items v-model="tab">
      <v-tab-item v-for="item in items" :key="item.tab">
        <v-container>
          <v-row>
            <v-card flat style="width: 70%">
              <v-col>
                <v-text-field
                  label="用户名"
                  v-model="username"
                  :error-messages="usernameErrors"
                  :counter="16"
                  @input="$v.username.$touch()"
                  @blur="$v.username.$touch()"
                ></v-text-field>
                <v-text-field
                  type="password"
                  label="密码"
                  v-model="password"
                  :error-messages="passwordErrors"
                  :counter="20"
                  @input="$v.password.$touch()"
                  @blur="$v.password.$touch()"
                ></v-text-field>
                <v-text-field
                  type="password"
                  label="再次输入密码"
                  v-model="confirmPassword"
                  :error-messages="confirmErrors"
                  @input="$v.confirmPassword.$touch()"
                  @blur="$v.confirmPassword.$touch()"
                ></v-text-field>
                <v-text-field
                  label="电子邮箱地址"
                  v-model="email"
                  :error-messages="emailErrors"
                  @input="$v.email.$touch()"
                  @blur="$v.email.$touch()"
                ></v-text-field>
                <v-tooltip right>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon
                    v-if="item.type == 1"
                      color="primary"
                      dark
                      v-bind="attrs"
                      v-on="on"
                    >
                      info
                    </v-icon>
                  </template>
                  <p>欲申请成为主办方请向平台管理员联系提交官方认证信息</p>
                  <p>管理员将在审核并录入信息后提供组织者邀请码</p>
                </v-tooltip>     
                <v-text-field
                  v-if="item.type == 1"
                  v-model="invitationCode"
                  label="组织者邀请码"                 
                >     
                </v-text-field>
              </v-col>

              <v-card-actions>
                <v-btn
                  class="info"
                  @click="submit()"
                  :loading="sendingForm"
                  :disabled="sendingForm"
                >
                  注册
                </v-btn>
                <v-spacer> </v-spacer>
                <!--v-btn
                  class="warning"
                  @click="redirect('404')"
                  v-if="item.type == 1"
                >
                  什么是邀请码
                </v-btn>
                <v-btn
                  class="success ml-3"
                  @click="snackbar('我们还没有写这个功能', 'success')"
                  v-if="item.type == 1"
                >
                  获取邀请码
                </v-btn-->
              </v-card-actions>
            </v-card>
            <v-card flat style="width: 30%">
              <v-card-subtitle class="text-h6">
                Contest+</br>
                一个提供一站式服务的竞赛平台
              </v-card-subtitle>
              <v-card-text>
                {{
                  item.type == 0
                    ? "本平台提供参赛用户的竞赛报名、在校身份验证及获奖后带防伪功能的电子获奖证书领取"
                    : "本平台提供竞赛举办方进行竞赛信息发布、报名管理、评奖等竞赛管理服务"
                }}
              </v-card-text>
            </v-card>
          </v-row>
        </v-container>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>

<script>
// 注册步骤1：输入基本信息
import merge from "webpack-merge";
import qs from "qs";
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { validationMixin } from "vuelidate";
import {
  required,
  maxLength,
  email,
  sameAs,
  minLength,
} from "vuelidate/lib/validators";
const usernameChecker = (value) => /^[a-zA-Z][a-zA-Z0-9_-]*$/.test(value);
export default {
  name: "RegisterMain",
  mixins: [redirect, snackbar, validationMixin],
  // 表单合法性检查
  computed: {
    checkboxErrors() {
      const errors = [];
      if (!this.$v.checkbox.$dirty) return errors;
      !this.$v.checkbox.checked && errors.push("您必须同意用户协议才能继续");
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !(this.$v.password.minLength && this.$v.password.maxLength) &&
        errors.push("密码长度应该介于6~20个字符");
      !this.$v.password.required && errors.push("请输入密码");
      return errors;
    },
    confirmErrors() {
      const errors = [];
      if (!this.$v.confirmPassword.$dirty) return errors;
      !this.$v.confirmPassword.required && errors.push("请再次输入密码以确认");
      !this.$v.confirmPassword.sameAsPassword &&
        errors.push("两次输入的密码不一致");
      return errors;
    },
    usernameErrors() {
      const errors = [];
      if (!this.$v.username.$dirty) return errors;
      !this.$v.username.required && errors.push("请输入用户名");
      !this.$v.username.usernameChecker &&
        errors.push("用户名只能包含字母、数字、下划线或连字符，且以字母开头");
      !(this.$v.username.minLength && this.$v.username.maxLength) &&
        errors.push("用户名长度应该介于4~16个字符");
      return errors;
    },
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
    username: {
      required,
      minLength: minLength(4),
      maxLength: maxLength(16),
      usernameChecker,
    },
    password: {
      required,
      minLength: minLength(6),
      maxLength: maxLength(20),
    },
    confirmPassword: {
      required,
      sameAsPassword: sameAs("password"),
    },
    email: { required, email },
  },
  methods: {
    // 验证表单的有效性，并发送经验证有效的表单
    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.$emit("update:email", "");
        this.snackbar("请完整填写正确的信息", "error");
        this.sendingForm = false;
      } else {
        this.sendingForm = true;
        requestPost({
          url: "/register/info",
          data: {
            username: this.username,
            password: this.$md5(this.password),
            email: this.email,
            userType: this.tab ? "sponsor" : "user",
            invitationCode: this.invitationCode,
          },
        })
          .then((res) => {
            this.sendingForm = false;
            if (res.data.message != undefined) {
              this.$emit("update:email", this.email);
              this.$router.replace({ path: "/register/emailcheck" });
            } else {
              this.snackbar("出错啦，错误原因：" + res.data.error, "error");
            }
          })
          .catch((err) => {
            this.snackbar("服务器开小差啦，请稍后再试", "error");
            this.sendingForm = false;
            console.log("error", err);
          });
      }
    },
  },
  data() {
    return {
      sendingForm: false,
      username: "",
      password: "",
      confirmPassword: "",
      invitationCode: "",
      email: "",
      tab: null,
      items: [
        { tab: "我是学生", type: 0 },
        { tab: "我是主办方", type: 1 },
      ],
    };
  },
};
</script>