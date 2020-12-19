<template>
  <div id="CertificatePage">
    <v-container>
      <div v-if="false && isLoading" id="skeleton_loaders">
        <v-skeleton-loader type="image" class="my-5"></v-skeleton-loader>
        <v-skeleton-loader type="heading" class="my-2"></v-skeleton-loader>
        <v-skeleton-loader type="list-item-avatar-three-line@3">
        </v-skeleton-loader>
      </div>
      <div v-if="true || !isLoading">
        <v-alert
          prominent
          type="warning"
          border="left"
        >
          <v-row align="center">
            <v-col class="grow">
              欢迎查看您的证书：{{verifyCode}}
            </v-col>
            <v-col class="shrink">
              <v-btn @click="redirect('/user')" outlined>前往认证页面</v-btn>
            </v-col>
          </v-row>
        </v-alert>
      </div>
    </v-container>
  </div>
</template>

<script>
import { requestPost } from "@/network/request.js";
import { logState } from "@/mixins/logState.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import * as dateParser from "@/assets/datetime.js";
import NoticeViewer from "@/components/NoticeComponent/NoticeViewer.vue";
import ContestRegister from "@/components/ContestParticipation/ContestRegister.vue";
import ContestGroupInfo from "@/components/ContestParticipation/ContestGroupInfo.vue";
import ContestSumbitWorks from "../components/ContestParticipation/ContestSumbitWorks.vue";
export default {
  name: "CertificatePage",
  inject: ["softReload"],
  mixins: [redirect, snackbar, filter, logState],
  components: {
    NoticeViewer,
    ContestRegister,
    ContestGroupInfo,
    ContestSumbitWorks,
  },
  created() {
    this.verifyCode = this.$route.params.verifyCode;
    if (false) {
      if (!/^\d+$/.test(this.contestId)) {
        this.pageNotFound();
      }
      this.userType = this.getUserType();
      requestPost(
        {
          url: "/contest/retrieve",
          data: {
            params: this.getContestFilter({
              id: Number(this.contestId),
              detailed: true,
            }),
            pageNum: 0,
            pageSize: 0,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          console.log("no!!!", res);
          this.isLoading = false;
          if (res.data.data.length > 0) {
            this.info = res.data.data[0];
            try {
              this.info["description"] = JSON.parse(this.info["description"]);
            } catch (error) {
              console.log("json parse error", error);
              this.info["description"] = {
                isEmpty: true,
              };
            }
            try {
              this.info["module"] = JSON.parse(this.info["module"]);
            } catch (error) {
              console.log("module json parse error", error);
              this.info["module"] = [];
            }

            console.log("haha,", this.info);
            this.contestStatus = dateParser.getStateDescription(
              this.info["state"]
            );
            this.fetchUserStatus();
            this.fetchBodyPictures();
            this.fetchNotice();
            switch (this.info.censorStatus) {
              case "pending":
                this.contestStatus[3] = "竞赛待审核";
                break;
              case "reject":
                this.contestStatus[3] = "审核未通过";
                break;
            }
            console.log(this.info);
          } else {
            this.pageNotFound();
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
          this.softReload("/search");
          this.isLoading = false;
        });
    }
  },
  data() {
    return {
      verifyCode: "",
      userType: "",
      panelVisible: false,
      showGroupPanel: false,
      contestId: 0,
      isLoading: true,
      isLoadingNotice: true,
      isFetchingBodyPictures: true,
      info: Object,
      img: {
        show: true,
        showOverlay: false,
        overlayMaxWidth: 1200,
        overlayMaxHeight: 800,
        height: 1200,
      },
      noticeList: [],
      invisibleNoticeCount: 0,
      userStatus: Object,
      userParticipationInfo: Object,
      contestStatus: [],
      calculatedStatus: "notUser",
    };
  },
  methods: {
    pageNotFound() {
      this.softReload("/pagenotfound");
      this.snackbar("您查找的页面不存在", "error");
    },

    showPanel(openPanel = true) {
      this.panelVisible = openPanel;
      this.showGroupPanel &= openPanel;
    },

    calculateUserStatus() {
      // 有 限 状 态 自 动 机
      // 咋 回 事 儿 啊   啥 玩 意 儿 啊    啥 情 况 啊
      // TODO: 这几句吐槽应该删掉
      console.log("calculated status", this.contestStatus);
      if (this.calculatedStatus == "notUser") {
        return;
      }
      switch (this.contestStatus[0]) {
        case "apply":
          if (this.contestStatus[1] == 1) {
            this.calculatedStatus = "pending";
          } else {
            if (!this.userStatus.registered) {
              this.calculatedStatus = "unregistered";
            } else if (!this.userStatus.verified) {
              this.calculatedStatus = "unverified";
            } else {
              this.calculatedStatus = "unstart";
            }
          }
          break;
        case "contest":
          //TODO: FIXME: RESUMEhere
          if (!this.userStatus.registered) {
            this.calculatedStatus = "userNotParticipate";
          } else if (!this.userStatus.verified) {
            this.calculatedStatus = "unverified";
          } else {
            if (this.contestStatus[1] == 1) {
              this.calculatedStatus = "unstart";
            } else {
              if (!this.userStatus.submitted) {
                this.calculatedStatus = "unsubmitted";
              } else {
                this.calculatedStatus = "submitted";
              }
            }
          }
          break;
        case "review":
          if (!this.userStatus.registered) {
            this.calculatedStatus = "userNotParticipate";
          } else if (!this.userStatus.verified) {
            this.calculatedStatus = "unverified";
          }
          //  else if (!this.userStatus.submitted) {
          //   this.calculatedStatus = "userNotSubmit";
          // }
          else if (!this.info.judgeCompleted) {
            this.calculatedStatus = "unjudged";
          } else {
            this.calculatedStatus = "judged";
          }
          break;
        default:
          this.calculatedStatus = "notValid";
      }
    },

    fetchUserStatus() {
      requestPost(
        {
          url: "/user/checkrelation",
          data: {
            contestId: this.contestId,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          console.log("userStatus", res.data);
          switch (res.data.error) {
            case undefined:
              if (res.data.isUser) {
                this.userStatus = res.data.userStatus;
                this.userParticipationInfo = res.data;
                this.calculatedStatus = "";
                this.calculateUserStatus();
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
          this.snackbar("服务器开小差啦，暂时无法获取您的状态", "error");
          console.log("error", err);
        });
    },

    fetchNotice() {
      this.isLoadingNotice = true;
      console.log("notice params", this.contestInfo, this.contestId);
      requestPost(
        {
          url: "/notice/browse",
          data: {
            contestId: this.contestId,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isLoadingNotice = false;
          switch (res.data.error) {
            case undefined:
              this.noticeList = res.data.data;
              this.invisibleNoticeCount = Math.max(
                res.data.count - res.data.data.length,
                0
              );
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
          this.snackbar("服务器开小差啦，加载公告失败", "error");
          console.log("error", err);
          this.isLoadingNotice = false;
        });
    },

    fetchBodyPictures() {
      let pictureId = [];
      for (let i in this.info.description) {
        let item = this.info.description[i];
        if (item.type == "picture") {
          pictureId.push(item.picId);
        }
      }
      console.log("the ids", pictureId);
      requestPost(
        {
          url: "/handlepic/view",
          data: {
            pictureId: pictureId,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          switch (res.data.error) {
            case undefined:
              let counter = 0;
              for (let i in this.info.description) {
                let item = this.info.description[i];
                if (item.type == "picture") {
                  item.imgUrl = res.data.imageUrl[counter];
                  counter++;
                }
              }
              console.log("what we fetch?", res.data, this.info.description);
              // TODO: 这一行不要提前
              this.isFetchingBodyPictures = false;
              break;
            default:
              this.isFetchingBodyPictures = false;
              this.snackbar(
                "哎呀，出错了，错误原因：" + res.data.error,
                "error"
              );
          }
        })
        .catch((err) => {
          this.snackbar("哎呀，加载图片出错了，请稍后重试", "error");
          this.isFetchingBodyPictures = false;
          console.log("error", err);
        });
    },
    // onScroll(e) {
    //   console.log("haha", this.img.height);
    //   this.img.height = Math.max(0, 400 - e.target.scrollTop);
    // },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
