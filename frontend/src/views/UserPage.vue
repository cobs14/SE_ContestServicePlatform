<template>
  <v-container id="UserPage">
    <div v-if="isLoading">
        <v-skeleton-loader type="image" class="my-5"></v-skeleton-loader>
        <v-skeleton-loader type="heading" class="my-2"></v-skeleton-loader>
        <v-skeleton-loader type="list-item-avatar-three-line@3">
        </v-skeleton-loader>
    </div>
    <div v-if="!isLoading">
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
          <div class="grey--text">就读院校：{{ userInfo.school || "暂无" }}</div>
          <div class="grey--text">就读专业：{{ userInfo.major || "暂无" }}</div>
          <div class="grey--text">电子邮箱：{{ userInfo.email || "暂无" }}</div>
          <div class="grey--text">
            个人简介：{{ userInfo.description || "暂无" }}
          </div>
        </v-card-text>
        <v-card-text v-if="userInfo.userType === 'sponsor'">
          <div class="grey--text">联系邮箱：{{ userInfo.email || "暂无" }}</div>
        </v-card-text>
      </v-col>
      <v-col cols="12" sm="8">
        <v-card-subtitle class="text-h6 mt-6">和 {{showName()}} 聊天</v-card-subtitle>
        <v-divider></v-divider>
        <!-- TODO: load after userInfo is fetched -->
        <chat-box :contactInfo="userInfo"></chat-box>
      </v-col>
    </v-row>
      </v-card>
    </div>
  </v-container>
</template>

<script>
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
import ChatBox from "@/components/MessageComponents/ChatBox.vue";
export default {
  name: "UserPage",
  mixins: [redirect, snackbar, logState],
  components: { ChatBox },
  methods: {
    pageNotFound() {
      this.softReload("/pagenotfound");
      this.snackbar("您查找的用户不存在", "error");
    },
    fetchUserInfo() {
      console.log('user id', this.userId);
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
            console.log("Get User Info: ");
            console.log(this.userInfo);
            this.isLoading = false;
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
    showName(){
      return this.userInfo.userType === 'sponsor' ? this.userInfo.trueName : this.userInfo.username ;
    }
  },
  created() {
    // TODO: skeleton loader
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
  },
  data() {
    return {
      userId: 0,
      userInfo: Object,
      isLoading: true,
      defaultHead: require("../../static/images/defaultHead.jpg")
    };
  },
  computed: {},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
