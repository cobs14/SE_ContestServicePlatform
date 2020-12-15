<template>
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
                  :loading="loggingIn"
                  :disabled="loggingIn"
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
                  @click="redirect('/resetpassword')"
                >
                  忘记密码？
                </v-btn>
              </v-card-actions>
            </v-card>
            <v-card flat style="width: 30%">
              <v-card-subtitle>
                请输入正确的账号密码登录平台使用平台服务
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
</template>

<script>
import encryptor from "@/network/encrypt.js";
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { validationMixin } from "vuelidate";
import { required, minLength, maxLength } from "vuelidate/lib/validators";
import LoginMain from "@/components/LoginMain.vue";
const usernameChecker = (value) => /^[a-zA-Z][a-zA-Z0-9_-]*$/.test(value);
export default {
  name: "LoginMain",
  mixins: [redirect, snackbar, validationMixin],
  inject:['softReload'],
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
        this.snackbar("请完整填写正确的信息", "error");
        this.loggingIn = false;
        console.log("invalid");
      } else {
        // do your submit logic here
        this.loggingIn = true;
        this.__userLogin({
          username: this.username,
          password: this.password,
        });
      }
    },

    __userLogin: function (params) {
      //Step 1. Get Pubkey
      //console.log('starting get key', params);
      requestPost({
        url: "/key",
        data: {
          username: params.username,
          email: params.email,
        },
      })
        .then((res) => {
          //console.log('got key', res.data);
          if (res.data.message != undefined) {
            //success
            this.$cookies.set("pubKey", res.data.message, "1d");
            this.__sendLoginRequest(params);
          } else {
            //Username or email is invalid
            this.loggingIn = false;
            this.snackbar("您输入了无效的用户名或邮箱地址", "error");
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          this.loggingIn = false;
          console.log("error", err);
        });
    },

    __sendLoginRequest: function (params) {
      let pubKey = this.$cookies.get("pubKey");
      if (pubKey != null) {
        //TODO: FIXME: Have trouble in encrypting
        let encryptedParams = { ...params };
        let aesKey = encryptor.AESgeneratekey();
        // let encryptedAesKey = encryptor.RSAencrypt(aesKey, pubKey);
        // encryptedParams["key"] = encryptedAesKey;
        encryptedParams["key"] = aesKey;
        //TODO: FIXME: why Base64 for password in document?
        // encryptedParams["password"] = encryptor.AESencrypt(
        //   encryptedParams["password"],
        //   aesKey
        // );
        console.log("encrypted login info", encryptedParams);
        requestPost({
          url: "/login",
          //TODO: load params here
          data: encryptedParams,
        })
          .then((res) => {
            this.loggingIn = false;
            if (res.data.message != undefined) {
              for (let key in res.data) {
                if (key == "id") {
                  this.$cookies.set("userId", res.data.id, "1d");
                } else if (key == "message") {

                } else {
                  this.$cookies.set(key, res.data[key], "1d");
                }
              }
              //提示登录成功
              this.snackbar(
                "登录成功。欢迎回来，" + res.data.username,
                "success"
              );
              this.softReload("/");
            } else {
              this.snackbar("登录失败啦，错误原因：" + res.data.error, "error");
              console.log("error", res);
            }
          })
          .catch((err) => {
            this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
            this.loggingIn = false;
            console.log("error", err);
          });
      } else {
        this.loggingIn = false;
        this.snackbar(
          "登录失败，无法访问cookie，请检查您的浏览器设置",
          "error"
        );
      }
    },
  },
  data() {
    return {
      loggingIn: false,
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