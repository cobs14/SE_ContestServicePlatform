<template>
  <div id="HomePage">
    <v-carousel
      cycle
      height="400"
      hide-delimiter-background
      show-arrows-on-hover
    >
      <v-carousel-item v-for="(slide, i) in slides" :key="i">
        <v-sheet :color="colors[i]" height="100%">
          <v-row class="fill-height" align="center" justify="center">
            <div class="display-3">{{ slide }}</div>
          </v-row>
        </v-sheet>
      </v-carousel-item>
    </v-carousel>
    <v-container>
      <v-chip class="ma-2" color="indigo" label text-color="white">
        <v-icon class="material-icons mr-1">event</v-icon>
        头版赛事
      </v-chip>
      <!--TODO: Add 4 contest card -->
      <!--v-row>
        <v-col v-for="n in 4" :key="n" cols="12" sm="3">
          <contest-card></contest-card>
        </v-col>
      </v-row-->
     
      <v-divider></v-divider>
      <v-chip class="ma-2" color="pink" label text-color="white">
        <v-icon class="material-icons mr-1">event</v-icon>
        最新公告
      </v-chip>
      <!--v-skeleton-loader
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
          </div-->
    </v-container>
    <!-- FIXME: this should be removed later -->
    <!--div>
      <v-btn @click="uploadPicture" class="warning ma-5">Send Picture</v-btn>
      <v-form ref="pictureForm">
        <v-file-input
          v-model="selectedPicture"
          :rules="pictureRules"
          required
          show-size
          accept="image/*"
          placeholder="点击此处选择要上传的图片"
          label="竞赛背景图"
          prepend-icon="mdi-camera"
        >
        </v-file-input>
      </v-form>
      <v-img :src="imgUrl"> </v-img>
    </div-->

    <v-container> </v-container>
  </div>
</template>

<script>
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import { logState } from "@/mixins/logState.js";
import { requestPost, requestUploadPictures } from "@/network/request.js";
import ContestCard from "@/components/ContestCard.vue"
import NoticeViewer from "@/components/NoticeComponent/NoticeViewer.vue";
export default {
  name: "HomePage",
  mixins: [redirect, snackbar, filter, logState],
  watch: {
    $route(val) {
      this.selectPage(val.params.option);
    },
    selectedPicture(val) {
      if (val == undefined) {
        this.selectedPicture = [];
      }
    },
  },
  components: { NoticeViewer, ContestCard },
  methods: {
    selectPage(param) {
      this.page = !param || param == "" ? "signup" : param;
      if (!["signup", "emailcheck", "verification"].includes(this.page))
        this.redirect("/pagenotfound");
    },
    __fetchImgUrl(imgId) {
      requestPost({
        url: "/handlepic/view",
        data: {
          pictureId: [imgId],
        },
      })
        .then((res) => {
          switch (res.data.error) {
          case undefined:
            console.log("url is, ", res.data, res.data.imageUrl);
            this.imgUrl = res.data.imageUrl[0];
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
        });
    },
    __sendPicture(imgId) {
      console.log("file is ", this.selectedPicture, ", id is", imgId);
      requestUploadPictures(
        {
          data: {
            config: [
              {
                pictureId: imgId,
                type: "contestHead",
                //TODO: FIXME: this is hard-coded now
                contentId: 233,
                fileKey: "img",
              },
            ],
            img: this.selectedPicture,
          },
        },
        this.$cookies.get("jwt")
      )
        .then((res) => {
          this.sendingPictures = false;
          console.log("send pic res:", res.data);
          if (res.data.error == undefined) {
            this.snackbar("上传图片成功，现在开始从服务器加载图片", "success");
            this.__fetchImgUrl(imgId);
          } else {
            this.snackbar(
              "上传图片时出错，错误原因：" + res.data.error,
              "error"
            );
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          this.sendingPictures = false;
          console.log("error", err);
        });
    },
    uploadPicture() {
      // if (this.$refs.pictureForm.validate()) {
      if (true) {
        this.sendingPictures = true;
        requestPost(
          {
            url: "/handlepic/reserve",
            data: {
              //TODO: set the number of identifiers here
              count: 1,
            },
          },
          this.$cookies.get("jwt")
        )
          .then((res) => {
            console.log(res.data);
            if (res.data.error == undefined) {
              console.log("ids:", res.data);
              this.__sendPicture(res.data.pictureId[0]);
            } else {
              this.sendingPictures = false;
              this.snackbar("糟糕，您的登录信息有误，请重新登录", "error");
              //TODO: logout & redirect here.
            }
          })
          .catch((err) => {
            console.log("error", err);
            this.snackbar("服务器开小差啦，请稍后再试", "error");
          });
      } else {
        this.snackbar("您选择的文件不符合要求", "error");
      }
    },
    getContest(){
      const params = this.getContestFilter({});
      console.log(params);
      requestPost({
        url: "/contest/retrieve",
        data: {
          params: params,
          pageNum: 1,
          pageSize: 4,
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
        });
    }
  },
  created() {
    this.selectPage(this.$route.params.option);
    this.getContest();
  },
  data() {
    return {
      page: "",
      email: "",
      colors: [
        "indigo",
        "warning",
        "pink darken-2",
        "red lighten-1",
        "deep-purple accent-4",
      ],
      slides: [
        "清华大学第一届编程大赛(假装有图)",
        "我们的赞助商：Contest+",
        "Google Coding Jam",
        "4th slide",
        "5th slide",
      ],

      //TODO: FIXME:
      //this should be removed later
      pictureRules: [
        (value) => !!value || "您不能上传空文件",
        (value) => value.size < 5000000 || "您上传的图片大小最多为5MB.",
      ],
      selectedPicture: [],
      imgUrl: "",
      sendingPictures: false,

      // 头版赛事
      contestInfo: {}
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
