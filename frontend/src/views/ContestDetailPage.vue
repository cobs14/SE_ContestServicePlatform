<template>
  <div id="contest_detail_page">
    <v-container>
      <div v-if="isLoading" id="skeleton_loaders">
        <v-skeleton-loader type="image" class="my-5"></v-skeleton-loader>
        <v-skeleton-loader type="heading" class="my-2"></v-skeleton-loader>
        <v-skeleton-loader type="list-item-avatar-three-line@3">
        </v-skeleton-loader>
      </div>
      <div v-if="!isLoading">
        <v-img
          v-show="img.show"
          :src="info.imgUrl"
          max-height="360px"
          @error="img.show = false"
          @click.stop="(img.showOverlay = true), (img.show = false)"
        >
        </v-img>
        <v-card-title
          :class="[`text-h3`, `font-weight-medium`]"
          class="transition-swing text--grey"
          v-text="info.title"
        >
        </v-card-title>

        <v-chip
          outlined
          class="mx-2"
          color="info"
          v-for="(mod, index) in info.module"
          :key="index"
        >
          {{ mod }}
        </v-chip>
        <v-btn small outlined class="ml-3" color="orange">
          {{ contestStatus[3] }}
        </v-btn>
        <v-divider class="my-3"></v-divider>
        <div v-if="!info.description.isEmpty">
          <v-row>
            <v-col cols="12" sm="9">
              <v-chip class="ma-2" color="blue" label text-color="white">
                <v-icon class="material-icons mr-1">description</v-icon>
                竞赛详情
              </v-chip>
              <div v-for="item in info.description" :key="item.index">
                <v-img
                  v-if="item.type == 'picture' && !isFetchingBodyPictures"
                  :src="item.imgUrl"
                />
                <div v-if="item.type == 'text'">
                  <v-card-title style="font-weight: 800">
                    {{ item.title }}
                  </v-card-title>
                  <v-card-text>
                    {{ item.content }}
                  </v-card-text>
                </div>
              </div>
            </v-col>
            <v-col cols="12" sm="3">
              <div id="contestDetailPageButton">
                <v-btn v-if="calculatedStatus == 'pending'" class="grey" block>
                  报名未开始
                </v-btn>

                <v-btn
                  v-if="calculatedStatus == 'unregistered'"
                  class="info my-2"
                  block
                  @click="showPanel"
                >
                  现在报名
                </v-btn>

                <v-btn
                  v-if="calculatedStatus == 'unverified'"
                  class="warning my-2"
                  block
                >
                  等待审核报名信息
                </v-btn>

                <v-btn
                  v-if="calculatedStatus == 'unstart'"
                  class="warning my-2"
                  block
                >
                  等待竞赛开始
                </v-btn>

                <v-btn
                  v-if="calculatedStatus == 'unsubmitted'"
                  class="info my-2"
                  block
                  @click="showPanel"
                >
                  提交作品
                </v-btn>

                <v-btn
                  v-if="calculatedStatus == 'submitted'"
                  class="success my-2"
                  block
                  @click="showPanel"
                >
                  管理提交的作品
                </v-btn>

                <v-btn
                  v-if="calculatedStatus == 'userNotSubmit'"
                  class="warning my-2"
                  block
                >
                  您未按时提交作品
                </v-btn>

                <v-btn
                  v-if="userStatus.verified && info.allowGroup"
                  class="info my-2"
                  @click="(showGroupPanel = true), showPanel()"
                  block
                >
                  查看团队信息
                </v-btn>

                <v-btn
                  v-if="calculatedStatus == 'unjudged'"
                  class="warning my-2"
                  block
                >
                  等待奖项审批
                </v-btn>

                <v-btn
                  v-if="calculatedStatus == 'judged'"
                  class="success my-2"
                  block
                >
                  查看我的奖项(页面没写完)
                </v-btn>
              </div>
              <v-card class="mt-2">
                <v-chip class="ma-2" color="warning" label text-color="white">
                  <v-icon class="material-icons mr-1">info</v-icon>
                  赛事信息
                </v-chip>
                <v-card-text>
                  <div>竞赛主办方</div>
                  <div>{{ info.sponsor }}</div>
                </v-card-text>
                <v-card-text>
                  <div>赛事简介</div>
                  <div>{{ info.abstract }}</div>
                </v-card-text>
                <v-chip class="ma-2" color="green" label text-color="white">
                  <v-icon class="material-icons mr-1">call</v-icon>
                  联系我们
                </v-chip>
                <v-card-text>
                  <div>联系信箱</div>
                  <div>{{ info.sponsorEmail }}</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </div>
        <v-divider></v-divider>
        <v-container>
          <v-chip class="ma-2" color="pink" label text-color="white">
            <v-icon class="material-icons mr-1">event</v-icon>
            竞赛公告
          </v-chip>
          <v-skeleton-loader
            v-if="isLoadingNotice"
            type="card-heading,list-item-three-line@3"
          />
          <div v-if="!isLoadingNotice">
            <v-expansion-panels
              accordion
              v-if="!isLoadingNotice && noticeList.length > 0"
            >
              <v-expansion-panel
                v-for="item in noticeList"
                :info="item"
                :key="item.noticeId"
              >
                <v-expansion-panel-header>{{
                  item.title
                }}</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-card flat>
                    <notice-viewer
                      class="py-2"
                      :notice="item"
                      @showSnackbar="snackbar"
                    ></notice-viewer>
                  </v-card>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
            <v-card-title v-if="!isLoadingNotice && noticeList.length == 0">
              目前没有可用的公告
            </v-card-title>
            <v-card-title v-if="invisibleNoticeCount > 0">
              该竞赛还有{{ invisibleNoticeCount }}条仅参赛者可见的公告
            </v-card-title>
          </div>
        </v-container>
      </div>

      <v-dialog v-model="panelVisible" persistent max-width="600px">
        <v-divider> </v-divider>
        <v-card>
          <contest-group-info
            v-if="showGroupPanel"
            @showSnackbar="snackbar"
            @close="showPanel(false)"
            :userGroup="userParticipationInfo.userGroup"
          />
          <div v-if="!showGroupPanel">
            <contest-register
              v-if="calculatedStatus == 'unregistered'"
              @showSnackbar="snackbar"
              @close="showPanel(false)"
              :contestInfo="info"
            />
            <contest-sumbit-works
              v-if="
                calculatedStatus == 'unsubmitted' ||
                calculatedStatus == 'submitted'
              "
              @showSnackbar="snackbar"
              @close="showPanel(false)"
              :userSubmission="userParticipationInfo.userSubmission"
              :contestId="info.id"
            />
          </div>
        </v-card>
      </v-dialog>
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
  name: "ContestDetailPage",
  inject: ["softReload"],
  mixins: [redirect, snackbar, filter, logState],
  components: {
    NoticeViewer,
    ContestRegister,
    ContestGroupInfo,
    ContestSumbitWorks,
  },
  created() {
    this.contestId = this.$route.params.contestId;
    if (!/^\d+$/.test(this.contestId)) {
      this.pageNotFound();
    }
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
  },
  data() {
    return {
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
          } else if (!this.userStatus.submitted) {
            this.calculatedStatus = "userNotSubmit";
          } else if (!this.info.judgeCompleted) {
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
