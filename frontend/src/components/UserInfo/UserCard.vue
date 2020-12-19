<template>
  <v-card id="UserCard" class="ma-2 pa-2">
    <v-row>
      <v-col cols="12" sm="3">
        <v-hover>
          <template v-slot:default="{ hover }">
            <v-card
              elevation="0"
              max-width="220px"
              max-height="220px"
              class="pl-5 pt-5"
            >
              <v-img
                v-if="avatar && avatar != ''"
                :src="avatar"
                @error="avatar = undefined"
                max-width="220px"
                max-height="220px"
              >
              </v-img>
              <v-img
                v-else
                :src="defaultHead"
                max-width="220px"
                max-height="220px"
              >
              </v-img>
              <v-fade-transition>
                <v-overlay v-if="hover" absolute color="#036358" class="ml-5 mt-5">
                  <v-file-input
                    :disabled="isUploadingAvatar"
                    v-model="selectedAvatar"
                    hide-input
                    accept="image/*"
                    prepend-icon="mdi-camera"
                    @change="uploadAvatar"
                  />
                </v-overlay>
              </v-fade-transition>
            </v-card>
          </template>
        </v-hover>
      </v-col>
      <v-col cols="12" sm="9">
        <v-card-title style="font-weight: 800" class="text-h5">
          {{ info.username }}
        </v-card-title>
        <v-card-text>
          <div>已验证的身份信息</div>
          <div class="grey--text">真实姓名：{{ info.trueName || "暂无" }}</div>
          <div class="grey--text">就读院校：{{ info.school || "暂无" }}</div>
          <div class="grey--text">就读专业：{{ info.major || "暂无" }}</div>
          <div class="grey--text">
            学生编号：{{ info.studentNumber || "暂无" }}
          </div>
        </v-card-text>
        <v-card-text>
          <div>联系方式</div>
          <div class="grey--text">电子邮箱：{{ info.email || "暂无" }}</div>
          <div class="grey--text">联系电话：{{ info.mobile || "暂无" }}</div>
          <div class="grey--text">联系地址：{{ info.address || "暂无" }}</div>
          <div class="grey--text">
            个人简介：{{ info.description || "暂无" }}
          </div>
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

          <v-btn class="info ma-2" @click="showPanel('infoPanel', true)">
            修改个人信息
          </v-btn>
          <v-btn class="info ma-2" @click="showPanel('passwordPanel', true)">
            修改密码
          </v-btn>
        </v-card-actions>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { requestPost, requestUploadPictures } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
const codeChecker = (value) => /^[A-Z0-9]{16}$/.test(value);
export default {
  name: "UserCard",
  inject: ["showPanel", 'headerReload'],
  mixins: [redirect, snackbar, validationMixin, logState],
  watch:{
    info: function(newVal){
      this.avatar = newVal.avatar;
      this.$cookies.set('avatar', this.avatar);
      this.headerReload();
    }
  },
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
    __uploadContestPictures(avatarPicId) {
      this.isUploadingAvatar = true;
      let formData = {
        config: [
          {
            pictureId: avatarPicId,
            type: "avatar",
            contentId: this.info.id,
            fileKey: "file",
          },
        ],
        file: this.selectedAvatar,
      };

      console.log("what is sent?", formData);

      requestUploadPictures({
        data: formData,
      })
        .then((res) => {
          this.isUploadingAvatar = false;
          switch (res.data.error) {
            case undefined:
              console.log("modify ok", res.data);
              this.snackbar("上传头像成功", "success");
              this.softReload();
              break;
            case "login":
              this.clearLogInfo();
              break;
            default:
              this.snackbar(
                "哎呀，出错了，错误原因：" + res.data.error,
                "error"
              );
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再试", "error");
          this.isUploadingAvatar = false;
          console.log("error", err);
        });
    },
    __reservePicCount() {
      this.snackbar("正在上传头像，请稍候", "info");
      requestPost(
        {
          url: "/handlepic/reserve",
          data: {
            count: 1,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isUploadingAvatar = false;
          switch (res.data.error) {
            case undefined:
              console.log("reserved pics:", res.data);
              this.__uploadContestPictures(res.data.pictureId[0]);
              break;
            case "login":
              this.clearLogInfo();
              break;
            default:
              this.snackbar(
                "哎呀，出错了，错误原因：" + res.data.error,
                "error"
              );
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再试", "error");
          this.isUploadingAvatar = false;
          console.log("error", err);
        });
    },
    uploadAvatar() {
      console.log("i am triggered", this.selectedAvatar);
      if (this.selectedAvatar != undefined) {
        if (!this.selectedAvatar.type.startsWith("image")) {
          this.snackbar("请选择有效的图片文件", "error");
          this.selectedAvatar = undefined;
          return;
        }
        if (this.selectedAvatar.size > 10000000) {
          this.snackbar("图片过大，请不要超过10MB", "error");
          this.selectedAvatar = undefined;
          return;
        }
        this.isUploadingAvatar = true;
        this.__reservePicCount();
      }
    },
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
              this.snackbar("恭喜您，验证成功", "success");
              this.$cookies.set("userType", "user");
              this.softReload();
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
      avatar: "",
      isUploadingAvatar: false,
      selectedAvatar: undefined,
      defaultHead: require("../../../static/images/defaultHead.jpg"),
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
