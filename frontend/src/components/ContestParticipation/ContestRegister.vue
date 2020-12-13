<template>
  <div id="ContestRegister">
    <v-card-title style="font-weight: 800">确认报名信息 </v-card-title>

    <v-card-text>
      <div>竞赛基本信息</div>
      <div class="grey--text">竞赛名称：{{ contestInfo.title }}</div>
      <div class="grey--text">
        竞赛类别：{{ contestInfo.allowGroup ? "团队赛" : "个人赛" }}
      </div>
      <div class="grey--text">
        竞赛主办方：{{
          contestInfo.sponsorTrueName
            ? contestInfo.sponsorTrueName
            : contestInfo.sponsor
        }}
      </div>
      <div class="grey--text" v-if="contestInfo.allowGroup">
        团队人数限制：
        {{
          contestInfo.minGroupMember +
          (contestInfo.minGroupMember == contestInfo.maxGroupMember
            ? ""
            : " ~ " + contestInfo.maxGroupMember)
        }}人
      </div>
    </v-card-text>

    <v-card-text>
      <div>用户报名信息</div>
      <div class="grey--text">您的用户名：{{ this.getUsername() }}</div>
      <div v-if="contestInfo.allowGroup" class="my-2">
        <v-form ref="form">
          <v-text-field
            v-model="params.groupName"
            label="团队名"
            color="blue-grey lighten-2"
            placeholder="在此输入您团队的名称"
            :rules="groupNameRules"
            counter="64"
          />

          <v-textarea
            v-model="params.description"
            label="团队描述"
            :rules="descriptionRules"
            color="blue-grey lighten-2"
            placeholder="输入描述可让竞赛举办者和其他人了解您的团队，并有助于通过验证"
            counter="128"
          />

          <v-autocomplete
            v-model="selectedUsers"
            :loading="loadingUsers"
            :search-input.sync="usernameToSearch"
            :items="matchedUsers"
            :rules="participantIdRules"
            cache-items
            chips
            no-data-text="没有找到匹配的用户"
            color="blue-grey lighten-2"
            label="查找您的队友"
            placeholder="输入队友的用户名以查找他们"
            item-text="username"
            return-object
            multiple
            :counter="maxCnt"
          >
            <template v-slot:selection="data">
              <v-chip
                v-bind="data.attrs"
                :input-value="data.selected"
                close
                @click="data.select"
                @click:close="removeSelectedUser(data.item)"
              >
                <v-avatar left v-show="data.item.avatar">
                  <img :src="data.item.avatar" />
                </v-avatar>
                <v-avatar
                  left
                  v-show="!data.item.avatar"
                  color="green darken-3"
                >
                  <span class="white--text">{{
                    data.item.username.substr(0, 2)
                  }}</span>
                </v-avatar>
                {{ data.item.username }}
              </v-chip>
            </template>
            <template v-slot:item="data">
              <template v-if="typeof data.item !== 'object'">
                <v-list-item-content v-text="data.item"></v-list-item-content>
              </template>
              <template v-else>
                <v-list-item-avatar v-show="data.item.avatar">
                  <img :src="data.item.avatar" />
                </v-list-item-avatar>
                <v-list-item-avatar
                  v-show="!data.item.avatar"
                  color="green darken-3"
                >
                  <span class="white--text headline">{{
                    data.item.username.substr(0, 2)
                  }}</span>
                </v-list-item-avatar>
                <v-list-item-content class="ml-2">
                  <v-list-item-title
                    v-html="data.item.username"
                  ></v-list-item-title>
                  <v-list-item-subtitle
                    v-html="
                      (data.item.school ? data.item.schoo : '未知学校') +
                      '，' +
                      (data.item.major ? data.item.major : '未知专业')
                    "
                  ></v-list-item-subtitle>
                </v-list-item-content>
              </template>
            </template>
          </v-autocomplete>

          <v-text-field
            v-for="(user, i) in selectedUsers"
            :key="i"
            :label="'输入 ' + user.username + ' 的组队码'"
            v-model="user.groupCode"
            :rules="groupCodeRules"
          />
        </v-form>
      </div>
    </v-card-text>
    <v-card-actions>
      <v-btn depressed class="info" :loading="isSubmitting" @click="submit"
        >报名</v-btn
      >
      <v-spacer />
      <v-btn depressed :disabled="isSubmitting" @click="closePage"
        >关闭此页面</v-btn
      >
    </v-card-actions>
  </div>
</template>

<script>
import lodash from "lodash";
import { requestPost, downloadFile } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "ContestRegister",
  mixins: [redirect, snackbar, filter, logState],
  inject: ["softReload"],
  watch: {
    usernameToSearch(newName) {
      console.log("current options:", this.selectedUsers);
      this.fetchUsers(newName);
    },
  },
  methods: {
    showLog() {
      console.log("clicked, selected users are:", this.selectedUsers);
    },
    closePage() {
      this.$emit("close");
    },
    removeSelectedUser(item) {
      const index = this.selectedUsers.indexOf(item);
      if (index >= 0) this.selectedUsers.splice(index, 1);
    },
    fetchUsers(username) {
      this.loadingUsers = true;
      let params = this.getUserFilter({
        username: username ? username : "",
        // FIXME: TODO: REMOVE THIS LATER
        // userType: "",
      });

      console.log("haha fetchUser is triggered!", params);

      requestPost(
        {
          url: "/user/retrieve",
          data: {
            params: params,
            pageNum: 1,
            pageSize: 6,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.loadingUsers = false;
          switch (res.data.error) {
            case undefined:
              this.matchedUsers = res.data.data;
              console.log("what we fetch is ", this.matchedUsers);
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
          console.log("error", err);
          this.softReload();
          this.loadingUsers = false;
        });
    },
    submit() {
      if (this.isSubmitting) return;
      if (!this.contestInfo.allowGroup || this.$refs.form.validate()) {
        this.isSubmitting = true;
        if (this.contestInfo.allowGroup) {
          this.params.participantId = this.selectedUsers.map((v) => v.id);
          this.params.participantCode = this.selectedUsers.map(
            (v) => v.groupCode
          );
        }
        console.log("params gonna sent:", this.params);
        requestPost(
          {
            url: "/contest/apply",
            data: this.contestInfo.allowGroup
              ? this.params
              : { contestId: this.params.contestId },
          },
          this.getUserJwt()
        )
          .then((res) => {
            this.isSubmitting = false;
            switch (res.data.error) {
              case undefined:
                if (res.data.message == "ok") {
                  this.snackbar("报名申请已提交，请等待审核", "success");
                  this.softReload();
                } else {
                  this.snackbar("您输入的组队码有误，请重试", "error");
                }
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
            console.log("error", err);
            this.softReload();
            this.isSubmitting = false;
          });
      } else {
        this.snackbar("您的报名信息填写有误，请检查", "warning");
      }
    },
  },
  data() {
    return {
      isSubmitting: false,
      params: {
        contestId: 0,
        groupName: "",
        description: "",
        participantId: [],
      },
      minCnt: 0,
      maxCnt: 1,
      currentUserId: 0,
      selectedUsers: [], //[int]
      matchedUsers: [], //[Object]
      usernameToSearch: "",
      loadingUsers: false,
      groupNameRules: [
        (v) => !!v || "团队名不能为空",
        (v) => !v || v.length <= 64 || "团队名不能超过64个字符",
      ],
      descriptionRules: [
        (v) => !!v || "团队描述不能为空",
        (v) => !v || v.length <= 128 || "团队描述不能超过128个字符",
      ],
      participantIdRules: [
        (v) =>
          (this.minCnt <= v.length && v.length <= this.maxCnt) ||
          "您的团队人数不符合要求",
        (v) => !v.includes(this.currentUserId) || "您不能将自己选为队友",
      ],
      groupCodeRules: [
        (v) => !!v || "组队码不能为空",
        (v) => !v || v.length <= 64 || "组队码不能超过64个字符",
      ],
    };
  },
  created() {
    // 防抖
    this.fetchUsers = lodash.debounce(this.fetchUsers, 300);
    this.params.contestId = this.contestInfo.id;
    this.maxCnt = this.contestInfo.maxGroupMember
      ? this.contestInfo.maxGroupMember - 1
      : 1; //FIXME: -3 is for debug, normally 1
    this.minCnt = this.contestInfo.minGroupMember
      ? this.contestInfo.minGroupMember - 1
      : 0;
    this.currentUserId = this.getUserId();
    //this.params.participantId.push(this.getUserId());
    console.log("numbers ", this.minCnt, this.maxCnt, this.contestInfo);
  },
  props: {
    contestInfo: Object,
  },
};
</script>

<style>
</style>