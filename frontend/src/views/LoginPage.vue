<template>
  <div id="LoginPage">
    <v-container>
      <v-row>
        <v-spacer> </v-spacer>
        <div style="width: 70%; margin-top: 5%">
        <v-card id="LoginPanel">
            <v-card-title class="font-weight-black" style="font-size: 1.6em">
            用户登录
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
                    </v-col>

                    <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                            class="info ma-2"
                            @click="submit()"
                            :loading="sendingForm"
                            :disabled="sendingForm"
                            >
                            登入
                            </v-btn>    
                    </v-card-actions>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                        text
                        color="primary"
                        class="ma-1"
                        @click="redirect('/register')"
                        >
                        还没有账号？立即注册
                        </v-btn>
                        <v-btn
                        text
                        color="primary"
                        class="ma-1"
                        >
                        忘记密码？
                        </v-btn>
                        <!-- TODO: 忘记密码页面 -->
                    </v-card-actions>
                    </v-card>
                    <v-card flat style="width: 30%">
                    <v-card-subtitle>
                        请输入正确的账号密码登陆平台使用平台服务
                    </v-card-subtitle>
                    <v-card-text>
                        {{
                        item.type == 0
                            ? "学生具有很多优势，比如ABC"
                            : "组织者使用Contest+有123的好处。"
                        }}
                    </v-card-text>
                    </v-card>
                </v-row>
                </v-container>
            </v-tab-item>
            </v-tabs-items>
        </v-card>
        </div>
        <v-spacer> </v-spacer>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { validationMixin } from "vuelidate"
import {
    required,
    minLength,
    maxLength
} from "vuelidate/lib/validators"
const usernameChecker = (value) => /^[a-zA-Z][a-zA-Z0-9_-]*$/.test(value);
export default {
  name: "LoginPage",
  mixins: [redirect, snackbar, validationMixin],
  computed: {
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !(this.$v.password.minLength && this.$v.password.maxLength) &&
        errors.push("密码长度应该介于6~20个字符");
      !this.$v.password.required && errors.push("请输入密码");
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
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        // this.$emit("update:email", "");
        // this.snackbar("请完整填写正确的信息", "error");
        this.sendingForm = false;
        console.log("invalid");
      } else {
        // do your submit logic here
        this.sendingForm = true;
        console.log("in");
        // simulating sending forms
        setTimeout(() => {
          this.sendingForm = false;
          console.log("send");
          // this.$emit("update:email", this.email);
          // this.$router.replace({ path: "/register/emailcheck" });
        }, 1000);
      }
    },
  },
  data() {
    return {
      sendingForm: false,
      username: "",
      password: "",
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
