<template>
  <v-card class="ma-2 pa-2">
    <v-row>
      <v-col cols="12" sm="4">
        <v-hover>
          <template v-slot:default="{ hover }">
            <v-card elevation="0" max-width="220px" max-height="220px">
              <v-img
                src="https://cdn.vuetifyjs.com/images/john.jpg"
                alt="John"
                max-width="220px"
                max-height="220px"
              >
              </v-img>
              <v-fade-transition>
                <v-overlay v-if="hover" absolute color="#036358">
                  <v-btn>上传头像</v-btn>
                </v-overlay>
              </v-fade-transition>
            </v-card>
          </template>
        </v-hover>
      </v-col>
      <v-col cols="12" sm="8">
        <v-card-title>
          {{ info.username }}
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          学校：{{ info.school }}
          <br />
          邮箱：{{ info.email }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            class="info ma-2"
            v-if="info.userType === 'guest'"
            @click="showDialog = true"
          >
            验证身份
          </v-btn>
          <v-dialog v-model="showDialog" persistent max-width="600px">
            <v-card>
              <v-card-title>
                <span class="headline">学信网自动身份验证</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        label="学信网验证码"
                        v-model="xuexincode"
                        @input="$v.xuexincode.$touch()"
                        @blur="$v.xuexincode.$touch()"
                        :error-messages="codeErrors"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        label="学信网证件号码"
                        v-model="documentNumber"
                        @blur="$v.documentNumber.$touch()"
                        :error-messages="documentNumberErrors"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="showDialog = false"
                  :enabled="sendingForm"
                  :loading="sendingForm"
                >
                  取消验证
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="submitForVerification"
                  :enabled="sendingForm"
                  :loading="sendingForm"
                >
                  申请验证
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <v-btn class="info ma-2"> 修改密码 </v-btn>
        </v-card-actions>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
const codeChecker = (value) => /^[A-Z0-9]{16}$/.test(value);
export default {
  name: "UserCard",
  mixins: [redirect, snackbar, validationMixin, logState],
  computed: {
    codeErrors() {
      const errors = [];
      if (!this.$v.xuexincode.$dirty) return errors;
      !this.$v.xuexincode.codeChecker &&
        errors.push("请输入16位大写字母和数字");
      !this.$v.xuexincode.required && errors.push("请输入学信网在线验证码");
      return errors;
    },
    documentNumberErrors() {
      const errors = [];
      if (!this.$v.documentNumber.$dirty) return errors;
      !this.$v.documentNumber.required && errors.push("请输入学信网证件号码");
      return errors;
    },
  },
  validations: {
    xuexincode: { required, codeChecker },
    documentNumber: { required },
  },
  methods: {
    submitForVerification() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.snackbar("请完整填写正确的信息", "error");
        this.sendingForm = false;
      } else {
        this.sendingForm = true;
        requestPost(
          {
            url: "/qualification",
            data: {
              username: this.info.username,
              xuexincode: this.xuexincode,
              documentNumber: this.documentNumber,
            },
          },
          this.getUserJwt()
        )
          .then((res) => {
            this.sendingForm = false;
            console.log("ok", res, res.data, res.data.message, res.data.error);
            if (res.data.message != undefined) {
              this.$cookies.set("userType", "user");
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
  props: {
    info: Object,
  },
  data() {
    return {
      hover: false,
      showDialog: false,
      xuexincode: "",
      documentNumber: "",
      sendingForm: false,
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
