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
      <div v-if="contestInfo.allowGroup">
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
      <div v-if="contestInfo.allowGroup || true" class="my-2">
        <v-form ref="form">
          <v-text-field
            v-model="params.groupName"
            label="团队名"
            color="blue-grey lighten-2"
            placeholder="在此输入您团队的名称"
            counter="64"
          />

          <v-autocomplete
            v-model="selectedUsers"
            :loading="loadingUsers"
            :search-input.sync="usernameToSearch"
            :items="matchedUsers"
            chips
            no-data-text="没有找到匹配的用户"
            color="blue-grey lighten-2"
            label="查找您的队友"
            item-text="username"
            item-value="id"
            multiple
          >
            <template v-slot:selection="data">
              <v-chip
                v-bind="data.attrs"
                :input-value="data.selected"
                close
                @click="data.select"
                @click:close="remove(data.item)"
              >
                <v-avatar left>
                  <v-img :src="data.item.avatar"></v-img>
                </v-avatar>
                {{ data.item.username }}
              </v-chip>
            </template>
            <template v-slot:item="data">
              <template v-if="typeof data.item !== 'object'">
                <v-list-item-content v-text="data.item"></v-list-item-content>
              </template>
              <template v-else>
                <v-list-item-avatar>
                  <img :src="data.item.avatar" />
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title
                    v-html="data.item.username"
                  ></v-list-item-title>
                  <v-list-item-subtitle
                    v-html="data.item.school + '，' + data.item.major"
                  ></v-list-item-subtitle>
                </v-list-item-content>
              </template>
            </template>
          </v-autocomplete>

          <v-textarea
            v-model="params.description"
            label="团队描述"
            color="blue-grey lighten-2"
            placeholder="输入描述可让竞赛举办者和其他人了解您的团队，并有助于通过验证"
            counter="128"
          />
        </v-form>
      </div>
    </v-card-text>
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
  watch: {
    usernameToSearch(newName) {
      this.fetchUsers(newName);
    },
  },
  methods: {
    removeSelectedUser(item) {
      const index = this.selectedUsers.indexOf(item.id);
      if (index >= 0) this.selectedUsers.splice(index, 1);
    },
    fetchUsers(username) {
      this.loadingUsers = true;
      let params = this.getUserFilter({
        username: username ? username : "",
        userType: "",
      });

      console.log("haha fetchUser is triggered!", params);

      requestPost(
        {
          url: "/user/retrieve",
          data: {
            params: params,
            pageNum: 1,
            pageSize: 5,
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
    downloadNoticeFile() {
      //TODO: FIXME: download files here
      this.isDownloading = true;
      console.log("we are gonna download,", this.notice);
      requestPost(
        {
          url: "/notice/download",
          data: {
            noticeId: this.notice.noticeId,
          },
          responseType: "blob",
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isDownloading = false;
          switch (res.data.error) {
            case undefined:
              //TODO: FIXME: we have done nothing here
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
          this.isDownloading = false;
        });
    },
  },
  data() {
    return {
      params: {
        contestId: 0,
        groupName: "",
        description: "",
        participantId: [],
      },
      selectedUserCount: 1,
      selectedUsers: [], //[int]
      matchedUsers: [], //[Object]
      usernameToSearch: "",
      loadingUsers: false,
    };
  },
  created() {
    // 防抖
    this.fetchUsers = lodash.debounce(this.fetchUsers, 300);
    this.params.contestId = this.contestInfo.id;
    //this.params.participantId.push(this.getUserId());
  },
  props: {
    contestInfo: Object,
  },
};
</script>

<style>
</style>