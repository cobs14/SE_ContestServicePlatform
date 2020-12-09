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
        <v-main
          :class="[`text-h3`, `font-weight-medium`]"
          class="transition-swing text--grey"
          v-text="info.title"
        >
        </v-main>
        <v-divider></v-divider>
        <v-chip
          v-for="(mod, index) in info.module" :key="index"
        >
          {{mod}}
        </v-chip>
        <v-container v-if="!info.description.isEmpty">
          <v-row>
            <v-col cols="12" sm="9">
              <div v-for="item in info.description" :key="item.index">
                <v-img
                  v-if="item.type == 'picture' && !isFetchingBodyPictures"
                  :src="item.imgUrl"
                />
                <div v-if="item.type == 'text'">
                  <v-card-title>
                    {{ item.title }}
                  </v-card-title>
                  <v-card-text>
                    {{ item.content }}
                  </v-card-text>
                </div>
              </div>
            </v-col>
            <v-col cols="12" sm="3">
              <v-btn class="info" :block="true"> 提交
              </v-btn>
              <v-card class="mt-2">
                <v-chip class="ma-2" color="green" label text-color="white">
                  <v-icon class="material-icons mr-1">call</v-icon>
                  联系我们
                </v-chip>
                <v-card-subtitle>
                  竞赛主办方：
                </v-card-subtitle>
                <v-card-text>
                  {{info.sponsor}}
                </v-card-text>
                <v-card-subtitle>
                  联系信箱
                </v-card-subtitle>
                <v-card-text>
                  {{info.sponsorEmail}}
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
        <v-divider></v-divider>
        <v-container>
          <v-chip class="ma-2" color="pink" label text-color="white">
            <v-icon class="material-icons mr-1">event</v-icon>
            热门公告
          </v-chip>
        </v-container>
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
export default {
  name: "ContestDetailPage",
  inject: ["softReload"],
  mixins: [redirect, snackbar, filter, logState],
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
          // TODO: parse module
          console.log("haha,", this.haha);
          this.fetchBodyPictures();
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
      contestId: 0,
      isLoading: true,
      isFetchingBodyPictures: true,
      info: Object,
      img: {
        show: true,
        showOverlay: false,
        overlayMaxWidth: 1200,
        overlayMaxHeight: 800,
        height: 1200,
      },
    };
  },
  methods: {
    pageNotFound() {
      this.softReload("/pagenotfound");
      this.snackbar("您查找的页面不存在", "error");
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
