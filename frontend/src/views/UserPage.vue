<template>
  <v-container id="UserPage">
    <div v-if="isLoading">
      <v-skeleton-loader type="image" class="my-5"></v-skeleton-loader>
      <v-skeleton-loader type="heading" class="my-2"></v-skeleton-loader>
      <v-skeleton-loader type="list-item-avatar-three-line@3">
      </v-skeleton-loader>
    </div>
    <div v-if="!isLoading">
      <v-alert
        v-if="userType == 'guest'"
        prominent
        type="warning"
        border="left"
      >
        <v-row align="center">
          <v-col class="grow">
            您需要先前往个人中心进行实名验证后才能使用私信功能
          </v-col>
          <v-col class="shrink">
            <v-btn @click="redirect('/user')" outlined>前往认证页面</v-btn>
          </v-col>
        </v-row>
      </v-alert>
      <v-card class="ma-2 pa-2">
        <v-row>
          <v-col cols="12" sm="4">
            <v-card
              elevation="0"
              max-width="220px"
              max-height="220px"
              class="pl-5 pt-5"
            >
              <v-img
                v-if="userInfo.avatar && userInfo.avatar != ''"
                :src="userInfo.avatar"
                @error="userInfo.avatar = undefined"
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
            </v-card>
            <v-card-title style="font-weight: 800" class="text-h5">
              {{ showName() }}
            </v-card-title>
            <v-card-text v-if="userInfo.userType !== 'sponsor'">
              <div class="grey--text">
                就读院校：{{ userInfo.school || "暂无" }}
              </div>
              <div class="grey--text">
                就读专业：{{ userInfo.major || "暂无" }}
              </div>
              <div class="grey--text">
                电子邮箱：{{ userInfo.email || "暂无" }}
              </div>
              <div class="grey--text">
                个人简介：{{ userInfo.description || "暂无" }}
              </div>
            </v-card-text>
            <v-card-text v-if="userInfo.userType === 'sponsor'">
              <div class="grey--text">
                联系邮箱：{{ userInfo.email || "暂无" }}
              </div>
            </v-card-text>
          </v-col>
          <v-col cols="12" sm="8">
            <v-card-subtitle class="text-h6 mt-6"
              >和 {{ showName() }} 聊天</v-card-subtitle
            >
            <v-divider></v-divider>
            <chat-box :contactInfo="userInfo"></chat-box>
          </v-col>
        </v-row>
      </v-card>
    </div>
  </v-container>
</template>

<script>
// 用户浏览其他用户时能看到的页面
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
import ChatBox from "@/components/MessageComponents/ChatBox.vue";
export default {
  name: "UserPage",
  mixins: [redirect, snackbar, logState],
  inject: ["checkUserType"],
  components: { ChatBox },
  methods: {
    pageNotFound() {
      this.softReload("/pagenotfound");
      this.snackbar("您查找的用户不存在", "error");
    },
    // 获取其它用户的信息
    fetchUserInfo() {
      requestPost(
        {
          url: "/user",
          data: {
            id: this.userId,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          if (res.data.error == undefined) {
            this.userInfo = res.data;
            this.isLoading = false;
          } else if (res.data.error === "login") {
            this.clearUserInfo();
          } else {
            this.snackbar("出错啦，错误原因：" + res.data.error, "error");
            this.redirect("/");
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
          this.redirect("/");
        });
    },
    // 姓名显示
    showName() {
      return this.userInfo.userType === "sponsor"
        ? this.userInfo.trueName
        : this.userInfo.username;
    },
  },
  created() {
    // 页面创建后自动加载目标用户的信息
    // 并且，如果目标用户为当前登录用户
    // 则自动跳转到用户中心
    this.isLoading = true;
    this.userId = this.$route.params.userId;
    if (!/^\d+$/.test(this.userId)) {
      this.pageNotFound();
    }
    if (this.userId == this.getUserId()) {
      this.redirect("/user");
    } else {
      this.fetchUserInfo();
    }
    this.userType = this.getUserType();
  },
  data() {
    return {
      userId: 0,
      userInfo: Object,
      userType: "",
      isLoading: true,
      defaultHead: require("../../static/images/defaultHead.jpg"),
    };
  },
  computed: {},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
