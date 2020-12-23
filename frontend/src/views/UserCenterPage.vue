<template>
  <div id="UserCenterPage" style="display: flex">
    <aside>
      <v-card height="100%" min-height="1200" max-width="360" :dark="true" tile>
        <v-navigation-drawer permanent>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="title" style="text-align: center">
                用户中心
              </v-list-item-title>
              <v-list-item-subtitle style="text-align: center">
                User Center
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          <v-list dense nav>
            <v-list-item
              v-for="item in navigation"
              :key="item.title"
              :link="true"
              @click="page = item.page"
            >
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
      </v-card>
    </aside>
    <div class="main" style="display: block; width: 100%; height: 100%">
      <div style="margin: 0; background: white; width: 100%; height: 80px">
        <v-breadcrumbs :items="paths" divider="-"></v-breadcrumbs>
      </div>
      <div v-if="isLoading" style="margin: 0; background: white; width: 100%; height: 80px">
        <v-skeleton-loader type="image" class="my-5"></v-skeleton-loader>
        <v-skeleton-loader type="heading" class="my-2"></v-skeleton-loader>
        <v-skeleton-loader type="list-item-avatar-three-line@2">
        </v-skeleton-loader>
      </div>
      <div v-else>
        <v-container v-if="page === 'info'">
          <user-card :info="userInfo" @showSnackbar="snackbar"></user-card>
          <user-info-manager
            v-if="panels.infoPanel"
            :info="userInfo"
            @showSnackbar="snackbar"
          />
          <user-password-manager
            v-if="panels.passwordPanel"
            :info="userInfo"
            @showSnackbar="snackbar"
          />
          <v-card class="ma-2 pa-2" v-if="userInfo.userType !== 'guest'">
            <v-card-title>管理您的组队码</v-card-title>
            <v-card-subtitle>
              当您参加团队竞赛时，队长将通过您的组队码进行组队。<br />
              请妥善保管组队码，如果您怀疑组队码已泄露，可随时重新生成。组队码也将在组队成功后自动重新生成。
            </v-card-subtitle>
            <v-card-title v-if="!showGroupCode" style="font-weight: 800"
              >········
            </v-card-title>
            <v-card-title v-else style="font-weight: 800"
              >{{ userInfo.groupCode || "您还没有组队码" }}
            </v-card-title>
            <v-card-actions>
              <v-btn
                v-if="!showGroupCode"
                class="info"
                @click="showGroupCode = true"
                >查看组队码</v-btn
              >
              <v-btn v-else class="info" @click="showGroupCode = false"
                >隐藏组队码</v-btn
              >
              <v-spacer></v-spacer>
              <v-btn
                class="warning"
                @click="refreshGroupCode"
                :loading="isReloadingGroupCode"
                >刷新组队码</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-container>
        <v-container v-if="page === 'contest' && contestInfo.length !== 0">
          <contest-info-bar
              v-for="item in contestInfo"
              :info="item"
              :key="item.id"
              @showSnackbar="snackbar"
            />
        </v-container>
        <v-container v-if="page === 'contest' && contestInfo.length === 0">
          <div>暂时没有报名记录，快去报名竞赛吧！</div>
        </v-container>
        <v-container v-if="page === 'message'">
          <message-center @showSnackbar="snackbar" />
        </v-container>
      </div>
    </div>
  </div>
</template>

<script>
import { requestPost } from "@/network/request.js";
import { filter } from "@/mixins/filter.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
import UserCard from "@/components/UserInfo/UserCard.vue";
import UserInfoBar from "@/components/UserInfo/UserInfoBar.vue";
import UserPasswordManager from "@/components/UserInfoManager/UserPasswordManager.vue";
import UserInfoManager from "@/components/UserInfoManager/UserInfoManager.vue";
import MessageCenter from "../components/NoticeComponent/MessageCenter.vue";
import ContestInfoBar from "@/components/ContestInfo/ContestInfoBar.vue";
export default {
  name: "UserCenterPage",
  mixins: [redirect, snackbar, logState, filter],
  inject: ['checkUserType'],
  components: {
    UserCard,
    UserInfoBar,
    UserPasswordManager,
    UserInfoManager,
    MessageCenter,
    ContestInfoBar
  },
  methods: {
    showPanel(panelName, visibility) {
      this.panels[panelName] = visibility;
    },
    refreshGroupCode() {
      if (this.isReloadingGroupCode) return;
      this.isReloadingGroupCode = true;
      requestPost(
        {
          url: "/user/groupcode",
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isReloadingGroupCode = false;
          if (res.data.error == undefined) {
            this.snackbar("已经更新您的组队码", "success");
            this.userInfo.groupCode = res.data.newGroupCode;
            console.log("new code", res.data);
            this.showGroupCode = true;
          } else {
            this.snackbar("出错啦，错误原因：" + res.data.error, "error");
          }
        })
        .catch((err) => {
          this.isReloadingGroupCode = false;
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
        });
    },
    getUserInfo() {
      requestPost(
        {
          url: "/user",
        },
        this.getUserJwt()
      )
        .then((res) => {
          if (res.data.error == undefined) {
            this.userInfo = res.data;
            console.log("Get User Info: ");
            console.log(this.userInfo);
            this.isLoading = false;
            this.getUserContest();
          } else if(res.data.error === "login"){
            this.clearUserInfo();
          } else {
            this.snackbar("出错啦，错误原因：" + res.data.error, "error");
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
        });
    },
    getUserContest() {
      const filter = {censorStatus: 'Accept', participant: [this.userInfo.id]}
      const params = this.getContestFilter(filter);
        // console.log(params);
        requestPost({
          url: "/contest/retrieve",
          data: {
            params: params,
            pageNum: 1,
            pageSize: 0,
          },
        }, this.getUserJwt())
          .then((res) => {
            if (res.data.error == undefined) {
              this.contestInfo = res.data.data;
              console.log(this.contestInfo);
            } else if(res.data.error === 'login'){
              this.clearLogInfo();
            } else{
              this.snackbar("出错啦，错误原因：" + res.data.error, "error");
            }
          })
          .catch((err) => {
            this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
            console.log("error", err);
          })
    }
  },
  created() {
    this.checkUserType();
    this.getUserInfo();
  },
  data() {
    return {
      isLoading: true,

      // 面板控制相关
      panels: {
        passwordPanel: false,
        infoPanel: false,
      },
      // 组队码相关
      showGroupCode: false,
      isReloadingGroupCode: false,

      // 竞赛相关
      contestInfo: {},

      // 页面相关
      page: "info",
      tab: "",
      userInfo: {},
      navigation: [
        { icon: "playlist_add_check", title: "个人信息", page: "info" },
        { icon: "how_to_reg", title: "我的竞赛", page: "contest" },
        { icon: "speaker_notes", title: "消息中心", page: "message" },
      ],
    };
  },
  provide() {
    return {
      showPanel: this.showPanel,
    };
  },
  computed: {
    paths() {
      return [
        {
          text: "用户中心",
          disabled: false,
        },
        {
          text: hashtable[this.page],
          disabled: false,
        },
      ];
    },
  },
};
const hashtable = {
  info: "我的信息",
  contest: "我的竞赛",
  message: "消息中心",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
