<template>
  <div id="Register">
    <v-container>
      <v-row>
        <v-spacer> </v-spacer>
        <v-card style="width: 70%; margin-top: 5%">
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
                      <v-text-field
                        v-if="item.type == 1"
                        label="组织者邀请码"
                      ></v-text-field>
                    </v-col>

                    <v-card-actions>
                      <v-btn class="info" @click="submit()"> 注册 </v-btn>
                      <v-spacer> </v-spacer>
                      <v-btn class="warning" @click="redirect('404')">
                        获取验证码
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                  <v-card flat style="width: 30%">
                    <v-list-item-subtitle>
                      {{
                        item.type == 0
                          ? "学生具有很多优势，比如ABC"
                          : "组织者使用Contest+有123的好处。"
                      }}
                    </v-list-item-subtitle>
                  </v-card>
                </v-row>
              </v-container>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
        <v-spacer> </v-spacer>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { redirect } from "@/mixins/router.js";
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
  name: "RegisterPage",
  mixins: [redirect, validationMixin],
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
    select: { required },
    checkbox: {
      checked(val) {
        return val;
      },
    },
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.submitStatus = "ERROR";
      } else {
        // do your submit logic here
        this.submitStatus = "PENDING";
        setTimeout(() => {
          this.submitStatus = "OK";
        }, 500);
      }
    },
  },
  data() {
    return {
      username: "",
      password: "",
      confirmPassword: "",
      email: "",
      tab: null,
      items: [
        { tab: "我是学生", type: 0 },
        { tab: "我是发布者", type: 1 },
      ],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
