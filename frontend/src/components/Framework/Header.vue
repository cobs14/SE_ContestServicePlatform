<template>
  <v-app-bar
    app
    dark
    src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg"
  >
    <v-container>
      <v-row class="align-center">
        <div @click.stop="redirect('/')" style="cursor: pointer">
          <v-col v-if="$vuetify.breakpoint.mdAndUp">
            <v-card-title>Contest+</v-card-title>
            <v-card-subtitle>竞赛新发现</v-card-subtitle>
          </v-col>
          <v-card-title v-if="!$vuetify.breakpoint.mdAndUp"
            >Contest+
          </v-card-title>
        </div>
        <v-spacer></v-spacer>
        <v-text-field
          v-if="$vuetify.breakpoint.smAndUp"
          class="mr-4"
          hide-details
          append-icon="mdi-magnify"
          single-line
          placeholder="输入名称、关键词以查找竞赛"
          v-model="contestFilter"
          @click:append="searchContests"
        ></v-text-field>
        <v-btn
          v-if="!$vuetify.breakpoint.smAndUp"
          class="mr-4"
          icon
          @click="searchContests"
          ><v-icon dark> mdi-magnify </v-icon></v-btn
        >

        <v-btn v-if="!isLoggedIn" class="info ml-2" @click="redirect('/login')"
          >登录</v-btn
        >
        <v-btn
          v-if="isLoggedIn"
          class="info ml-2"
          @click="
            userLogout();
            redirect('/login');
          "
          >注销</v-btn
        >

        <a :href="toCenter">
          <v-badge
            :value="hasNewMessage"
            bordered
            color="red"
            dot
            overlap
            class="mx-4"
          >
            <v-avatar v-if="isLoggedIn">
              <img
                v-show="avatarLoaded"
                :src="userAvatar"
                @load="avatarLoaded = true"
              />
              <img v-show="!avatarLoaded" :src="defaultHead" />
            </v-avatar>
          </v-badge>
        </a>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
// 网站上方的工具栏
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
import { requestPost } from "@/network/request.js";
export default {
  mixins: [redirect, logState, snackbar],
  name: "v-header",
  methods: {
    // 搜索竞赛：跳转到对应的搜索界面
    searchContests() {
      this.redirect("/search/" + encodeURIComponent(this.contestFilter));
    },
    // 获取1条未读信息以判断是否有未读信息
    // 并对应地显示小红点
    fetchMessage() {
      requestPost(
        {
          url: "/message/getmessage",
          data: {
            type: "Unread",
            currentContactId: -1,
            pageNum: 1,
            pageSize: 1,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          switch (res.data.error) {
            case undefined:
              this.hasNewMessage = res.data.contact.length != 0;
              break;
            case "login":
              this.clearLogInfo();
            default:
              clearInterval(this.checkMessageTimer);
              break;
          }
        })
        .catch((err) => {
          clearInterval(this.checkMessageTimer);
        });
    },
  },
  // 页面创建时则设定响应的消息获取定时器
  created() {
    if (!this.hasLogin()) return;
    this.checkMessageTimer = setInterval(() => {
      this.fetchMessage();
    }, 2500);
  },
  computed: {
    // 判断用户是否登录
    isLoggedIn() {
      return this.hasLogin();
    },
    // 根据用户身份决定点击头像后应该前往哪个页面
    toCenter() {
      if (this.userType === "admin") {
        return "/admin";
      } else if (this.userType === "sponsor") {
        return "/management";
      } else {
        return "/user/" + this.userId;
      }
    },
  },
  data() {
    return {
      checkMessageTimer: 0,
      hasNewMessage: false,
      avatarLoaded: false,
      defaultHead: require("../../../static/images/defaultHead.jpg"),
      contestFilter: "",
      userAvatar: this.getUserAvatar(),
      userId: this.getUserId(),
      userType: this.getUserType(),
    };
  },
};
</script>