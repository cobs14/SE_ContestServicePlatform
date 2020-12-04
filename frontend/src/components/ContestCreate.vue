<template>
  <div id="ContestCreate">
    <v-container>
      <v-stepper alt-labels :value="createStep">
        <v-stepper-header>
          <v-stepper-step step="1"> 竞赛基本信息 </v-stepper-step>
          <v-stepper-step step="2"> 完善详细信息 </v-stepper-step>
          <v-stepper-step step="3"> 竞赛创建成功 </v-stepper-step>
        </v-stepper-header>
        <v-divider></v-divider>
        <v-stepper-items>
          <v-stepper-content :step="1">
            <v-row>
              <v-spacer> </v-spacer>
              <v-divider> </v-divider>
              <v-container>
                <v-card flat style="width: 100%">
                  <v-col>
                    <v-form ref="contestForm" v-model="validContestInfo">
                      <v-text-field
                        label="竞赛名称"
                        outlined
                        v-model="contestInfo.title"
                        :counter="64"
                        :rules="titleRules"
                        required
                      >
                      </v-text-field>
                      <v-select
                        v-model="contestInfo.module"
                        :items="moduleItems"
                        chips
                        label="竞赛模块"
                        multiple
                        outlined
                      >
                      </v-select>
                      <v-textarea
                        label="竞赛简介"
                        outlined
                        v-model="contestInfo.abstract"
                        :counter="1024"
                        :rules="abstractRules"
                        required
                      ></v-textarea>
                      <v-row>
                        <v-col>
                          <v-radio-group v-model="contestInfo.allowGroup" row>
                            <v-radio label="个人赛" :value="false"></v-radio>
                            <v-radio label="团体赛" :value="true"></v-radio>
                          </v-radio-group>
                        </v-col>
                        <v-col>
                          <v-text-field
                            label="队伍人数下限"
                            outlined
                            :disabled="!contestInfo.allowGroup"
                            type="number"
                            v-model="contestInfo.minGroupMember"
                            :rules="minMemberRules"
                          >
                          </v-text-field>
                        </v-col>
                        <span class="text">_</span>
                        <v-col>
                          <v-text-field
                            label="队伍人数上限"
                            outlined
                            :disabled="!contestInfo.allowGroup"
                            type="number"
                            v-model="contestInfo.maxGroupMember"
                            :rules="maxMemberRules"
                          >
                          </v-text-field>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col>
                          <v-radio-group v-model="contestCharge" row>
                            <v-radio label="免费" :value="false"></v-radio>
                            <v-radio label="收费" :value="true"></v-radio>
                          </v-radio-group>
                        </v-col>
                        <v-col>
                          <v-text-field
                            label="报名费（单位：分）"
                            outlined
                            :disabled="!contestCharge"
                            type="number"
                            v-model="contestInfo.chargeFee"
                            :rules="moneyRules"
                          >
                          </v-text-field>
                        </v-col>
                      </v-row>

                      <v-timeline dense>
                        <v-timeline-item
                          v-for="(select, index) in timeSelect"
                          :key="index"
                        >
                          <v-menu
                            ref="menu"
                            v-model="dateMenu[index]"
                            :close-on-content-click="false"
                            :return-value.sync="date"
                            transition="scale-transition"
                            offset-y
                            min-width="290px"
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <!--
                              <v-checkbox
                                v-if="index == 2"
                                label="开始比赛后仍允许报名"
                              >
                              </v-checkbox>
                              -->
                              <v-text-field
                                v-model="date[index]"
                                :disabled="lastDate[index] === undefined"
                                :label="select.text"
                                :rules="dateRules"
                                prepend-icon="event"
                                readonly
                                v-bind="attrs"
                                v-on="on"
                              ></v-text-field>
                            </template>

                            <v-date-picker
                              v-model="date[index]"
                              :min="lastDate[index]"
                              :max="allowDate[index]"
                              @input="dateMenu[index] = false"
                              no-title
                              scrollable
                            >
                              <v-spacer></v-spacer>
                            </v-date-picker>
                          </v-menu>
                        </v-timeline-item>
                      </v-timeline>
                    </v-form>
                    <v-row>
                      <v-spacer></v-spacer>
                      <v-btn
                        class="info ma-1"
                        @click="createBasicContestInfo"
                        :loading="sendingForm"
                        :disabled="sendingForm"
                      >
                        下一步
                      </v-btn>
                      <v-btn class="warning ma-1"> 重置 </v-btn>
                    </v-row>
                  </v-col>
                </v-card>
              </v-container>
              <v-spacer> </v-spacer>
            </v-row>
          </v-stepper-content>
          <v-stepper-content :step="2">
            <v-file-input
              v-model="contestPicture"
              :rules="pictureRules"
              required
              show-size
              accept="image/*"
              placeholder="点击此处选择要上传的图片"
              label="竞赛背景图"
              prepend-icon="mdi-camera"
              @change="updateForm"
            >
            </v-file-input>
            <description-card
              v-for="(info, index) in description"
              :key="index"
              :index="index"
              @showSnackbar="snackbar"
              v-on:content-change="updateDescription"
              v-on:delete-description="deleteDescription"
              :type="info.type"
              :descriptionTitle="info.title"
              :descriptionContent="info.content"
              :descriptionPicture="info.selectedPicture"
            >
            </description-card>
            <v-row>
              <v-spacer></v-spacer>
              <!-- <v-btn class="info ma-2" @click="gotoContestMain">上一页</v-btn> -->
              <v-btn
                class="secondary ma-2"
                @click="
                  description.push({ title: '', content: '' });
                  emptyDescription = true;
                "
                >增加详情</v-btn
              >
              <v-btn
                class="success ma-2"
                @click="submitContest"
                :loading="sendingForm"
                :disabled="emptyDescription || sendingForm"
                >提交创建申请</v-btn
              >
              <v-spacer></v-spacer>
            </v-row>
          </v-stepper-content>
          <v-stepper-content :step="3">
            <v-card flat style="width: 80%; margin: auto">
              <v-card-title class="font-weight-black" style="font-size: 1.6em">
                创建申请已经送出
              </v-card-title>
              <v-divider> </v-divider>
              <v-card-subtitle
                class="font-weight-medium"
                style="font-size: 1.1em"
              >
                您的竞赛创建申请已经送出，请静待管理员的审核。
                <br />
              </v-card-subtitle>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  class="info ma-2"
                  @click="external('/contest/' + contestId)"
                  >预览竞赛页面</v-btn
                >
                <v-btn class="success ma-2" @click="$emit('goto-list')"
                  >前往竞赛列表</v-btn
                >
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-container>
  </div>
</template>

<script>
import merge from "webpack-merge";
import { requestPost, requestUploadPictures } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import DescriptionCard from "@/components/ContestDescriptionCard.vue";
import * as dateParser from "@/assets/datetime.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "ContestCreate",
  mixins: [redirect, snackbar, logState],
  components: {
    DescriptionCard,
  },
  computed: {
    lastDate() {
      const date = [];
      date.push("0");
      for (let i = 0; i < 5; ++i) {
        date.push(this.date[i]);
      }
      return date;
    },
    allowDate() {
      const date = [];
      for (let i = 1; i < 6; ++i) {
        date.push(this.date[i]);
      }
      return date;
    },
  },
  methods: {
    hasEmptyDescriptionEntry() {
      //TODO: 加头图
      let res = false;
      if(!(this.contestPicture instanceof File))
      {
        return true;
      }
      for (let i in this.description) {
        let item = this.description[i];
        if (item.type == "picture" && !(item.selectedPicture instanceof File)) {
          res = true;
          break;
        }
        if (item.type == "text" && (item.title == "" || item.content == "")) {
          res = true;
          break;
        }
      }
      return res;
    },
    updateForm(){
      this.emptyDescription = this.hasEmptyDescriptionEntry();
    },
    updateDescription(data) {
      let { ...tempData } = data;
      this.description[data.index] = tempData;
      this.updateForm();
    },
    deleteDescription(data) {
      this.description.splice(data.index, 1);
      const length = this.description.length;
      if (length) {
        this.updateForm();
      } else {
        this.snackbar("请添加至少一条竞赛详细信息", "error");
        this.emptyDescription = true;
      }
    },
    createBasicContestInfo() {
      this.sendingForm = true;
      console.log("dates", this.lastDate, this.allowDate, this.date);
      if (
        !this.$refs.contestForm.validate() ||
        this.date[5] === undefined ||
        this.maxGroupMember < this.minGroupMember
      ) {
        this.snackbar("请完整填写正确的信息", "error");
        this.sendingForm = false;
      } else {
        let uploadInfo = { ...this.contestInfo };
        let parsedDate = this.date.map((x) =>
          dateParser.dateStringToTimestamp(x)
        );
        console.log("parsed date", parsedDate);
        uploadInfo.description = "";
        uploadInfo.applyStartTime = parsedDate[0];
        uploadInfo.applyDeadline = parsedDate[1];
        uploadInfo.contestStartTime = parsedDate[2];
        uploadInfo.contestDeadline = parsedDate[3];
        uploadInfo.reviewStartTime = parsedDate[4];
        uploadInfo.reviewDeadline = parsedDate[5];
        uploadInfo.chargeType = this.contestCharge ? "charge" : "audit";
        requestPost(
          {
            url: "/contest/creation",
            data: uploadInfo,
          },
          this.getUserJwt()
        )
          .then((res) => {
            this.sendingForm = false;
            switch (res.data.error) {
              case undefined:
                console.log("created contest:", res.data);
                this.contestId = res.data.id;
                this.createStep = 2;
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
            this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
            this.sendingForm = false;
            console.log("error", err);
          });
      }
    },
    __uploadContestPictures(headerPicId, config, formData) {
      this.sendingForm = true;

      config.push({
        pictureId: headerPicId,
        type: "contestHead",
        contentId: this.contestId,
        fileKey: "file" + headerPicId,
      });

      formData["file" + headerPicId] = this.contestPicture;

      formData.config = config;

      console.log("what is sent?", formData, config);

      requestUploadPictures({
        data: formData,
      })
        .then((res) => {
          this.sendingForm = false;
          switch (res.data.error) {
            case undefined:
              console.log("modify ok", res.data);
              this.snackbar("您已成功创建竞赛！", "success");
              this.createStep = 3;
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
          this.snackbar(
            "您的竞赛已成功创建，但未能上传详情，请稍后在管理页面重试",
            "error"
          );
          this.sendingForm = false;
          console.log("error", err);
        });
    },
    __syncDescriptionToServer(picIDs) {
      this.sendingForm = true;
      console.log("before send a form, picid:", picIDs);
      let config = [];
      let formData = {};
      let parsed = [];
      let idIndex = 1;
      for (let i in this.description) {
        let item = this.description[i];
        if (item.type == "picture") {
          item.picId = picIDs[idIndex];
          config.push({
            pictureId: picIDs[idIndex],
            type: "contestBody",
            contentId: this.contestId,
            fileKey: "file" + picIDs[idIndex],
          });
          formData["file" + picIDs[idIndex]] = item.selectedPicture;
          idIndex++;
        }
        let { ...shrinked } = item;
        delete shrinked.selectedPicture;
        parsed.push(shrinked);
      }
      console.log("look at me", parsed, this.contestId, this.description);

      requestPost(
        {
          url: "/contest/modify",
          data: {
            contestId: this.contestId,
            modifyAttribute: ["description"],
            modifyValue: [JSON.stringify(parsed)],
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.sendingForm = false;
          console.log("after send a form, picid:", picIDs);
          switch (res.data.error) {
            case undefined:
              console.log("modify ok", res.data);
              this.snackbar("正在上传图片，请稍后", "info");
              this.__uploadContestPictures(picIDs[0], config, formData);
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
          this.snackbar(
            "您的竞赛已成功创建，但未能上传详情，请稍后在管理页面重试",
            "error"
          );
          this.sendingForm = false;
          console.log("error", err);
        });
    },
    submitContest() {
      this.sendingForm = true;
      if (!this.$refs.contestForm.validate()) {
        this.snackbar("请完整填写正确的信息", "error");
        this.sendingForm = false;
      } else {
        let picCount = 1;
        console.log("description", this.description);
        for (let des in this.description) {
          if (this.description[des].type == "picture") {
            picCount += 1;
          }
        }
        console.log("picCount", picCount);
        // TODO: FIXME: resume here.
        // 1. 预约新的图片位置
        requestPost(
          {
            url: "/handlepic/reserve",
            data: {
              count: picCount,
            },
          },
          this.getUserJwt()
        )
          .then((res) => {
            this.sendingForm = false;
            switch (res.data.error) {
              case undefined:
                console.log("reserved pics:", res.data);
                //TODO: FIXME:
                //resume here.
                //update description and upload pics.
                this.__syncDescriptionToServer(res.data.pictureId);
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
            this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
            this.sendingForm = false;
            console.log("error", err);
          });
      }
    },
  },
  data() {
    return {
      contestId: undefined,
      validContestInfo: false,
      contestCharge: false,
      contestInfo: {
        title: "",
        abstract: "",
        module: [],
        allowGroup: false,
        minGroupMember: 1,
        maxGroupMember: 1,
        chargeType: "audit",
        chargeFee: 1,
      },

      titleRules: [
        (v) => !!v || "请输入竞赛标题",
        (v) => (v && v.length <= 64) || "竞赛标题的长度不能超过64个字符",
      ],

      abstractRules: [
        (v) => !!v || "请输入竞赛简介",
        (v) => (v && v.length <= 1024) || "简介的长度不能超过1024个字符",
      ],

      minMemberRules: [
        (v) => !!v || "请输入团队人数下限",
        (v) => (v && /^[0-9]+$/.test(String(v))) || "团队人数下限应为正整数",
        (v) => (v && v > 0) || "团队人数下限应为正整数",
      ],

      maxMemberRules: [
        (v) => !!v || "请输入团队人数上限",
        (v) => (v && /^[0-9]+$/.test(String(v))) || "团队人数上限应为正整数",
        (v) =>
          (v && this.contestInfo.minGroupMember <= v) ||
          "团队人数上限应为正整数，且大于人数下限",
      ],

      moneyRules: [
        (v) => !!v || "请输入报名费",
        (v) => (v && /^[0-9]+$/.test(String(v))) || "报名费用应为正整数",
        (v) => (v && v > 0) || "报名费用应为正整数",
      ],

      dateRules: [(v) => !!v || "日期不能为空"],
      date: [],

      sendingForm: false,
      dateMenu: [],
      emptyDescription: true,
      description: [{ title: "", content: "" }],
      createStep: 1,
      
      contestPicture: [],
      pictureRules: [
        (value) => !!value || "您不能上传空文件",
        (value) => value.size < 5000000 || "您上传的图片大小最多为5MB.",
      ],

      moduleItems: ["数字", "计算机", "物理"],
      timeSelect: [
        { text: "报名开始时间" },
        { text: "报名结束时间" },
        { text: "竞赛开始时间" },
        { text: "竞赛结束时间" },
        { text: "评审开始时间" },
        { text: "评审结束时间" },
      ],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
