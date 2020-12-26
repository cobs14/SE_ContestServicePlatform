<template>
  <div id="CertificatePage">
    <v-container>
      <div v-if="isLoading" id="skeleton_loaders">
        <v-skeleton-loader type="image" class="my-5"></v-skeleton-loader>
        <v-skeleton-loader type="heading" class="my-2"></v-skeleton-loader>
        <v-skeleton-loader type="list-item-avatar-three-line@3">
        </v-skeleton-loader>
      </div>
      <div v-else>
        <v-alert
          v-if="!isValidVerifyCode"
          prominent
          type="warning"
          border="left"
        >
          <v-row align="center">
            <v-col class="grow"> 这似乎不是有效的获奖证书链接 </v-col>
            <v-col class="shrink">
              <v-btn @click="redirect('/')" outlined>回到首页</v-btn>
            </v-col>
          </v-row>
        </v-alert>
        <div v-else>
          <v-card-title :class="[`text-h4`, `font-weight-medium`]"
            >竞赛获奖信息在线验证</v-card-title
          >

          <v-alert text color="info">
            <h3 class="headline">赛事信息</h3>

            <v-divider class="my-4 info" style="opacity: 0.22"></v-divider>
            <v-row align="center" no-gutters>
              <v-col class="grow">
                赛事名称：{{ data.contestInfo.contestName }}<br />
                主办单位：{{ data.sponsorInfo.trueName }}<br />
                赛事类别：{{
                  data.contestInfo.allowGroup ? "团体赛" : "个人赛"
                }}
              </v-col>
              <v-spacer></v-spacer>
              <v-col class="shrink">
                <v-btn
                  color="info"
                  outlined
                  @click="external('/contest/' + data.contestInfo.contestId)"
                >
                  前往竞赛页面
                </v-btn>
              </v-col>
            </v-row>
          </v-alert>

          <v-alert text color="info">
            <h3 class="headline">奖项信息</h3>
            <v-divider class="my-4 info" style="opacity: 0.22"></v-divider>
            <v-row align="center" no-gutters>
              <v-col class="grow">
                颁奖日期：{{ data.contestInfo.issueDate }}<br />
                所获奖项：{{ data.contestInfo.award }}
              </v-col>
            </v-row>
          </v-alert>

          <v-alert
            text
            color="info"
            v-for="(userInfo, i) in data.participantInfo.participants"
            :key="i"
          >
            <h3 class="headline">获奖者信息</h3>
            <v-divider class="my-4 info" style="opacity: 0.22"></v-divider>
            <v-row align="center" no-gutters>
              <v-col class="grow">
                用户名：{{ userInfo.username }}
                {{ userInfo.documentId != "" ? "（学信网验证用户）" : "" }}
                <br />
                真实姓名：{{ userInfo.trueName }} <br />
                证件号码：{{ userInfo.documentId }}<br />
                就读院校：{{ userInfo.school }} <br />
                就读专业：{{ userInfo.major }}
              </v-col>
              <v-spacer></v-spacer>
              <v-col class="shrink">
                <v-btn
                  color="info"
                  outlined
                  @click="external('/user/' + userInfo.id)"
                >
                  前往他的主页
                </v-btn>
              </v-col>
            </v-row>
          </v-alert>
        </div>
      </div>
    </v-container>
  </div>
</template>

<script>
// 获奖证书在线查询页面
import { requestPost } from "@/network/request.js";
import { logState } from "@/mixins/logState.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import * as dateParser from "@/assets/datetime.js";
export default {
  name: "CertificatePage",
  inject: ["softReload"],
  mixins: [redirect, snackbar, filter, logState],
  created() {
    // 解析URL中的参数，发送请求来判断是否为有效的证书
    this.verifyCode = this.$route.params.verifyCode;
    if (!this.verifyCode) {
      this.pageNotFound();
    }
    requestPost({
      url: "/certification/verify",
      data: {
        verifyCode: this.verifyCode,
      },
    })
      .then((res) => {
        // 如果有效，则显示对应的验证结果
        this.isLoading = false;
        this.isValidVerifyCode = res.data.error == undefined;
        if (this.isValidVerifyCode) {
          this.data = res.data;
        }
      })
      .catch((err) => {
        this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
        console.log("error", err);
        this.isLoading = false;
      });
  },
  data() {
    return {
      isLoading: true,
      verifyCode: "",
      isValidVerifyCode: false,
      data: {
        contestInfo: Object,
        sponsorInfo: Object,
        participantInfo: Object,
      },
    };
  },
  methods: {
    pageNotFound() {
      this.softReload("/pagenotfound");
      this.snackbar("您查找的页面不存在", "error");
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
