<template>
  <div id="HomePage">
    <v-hover v-slot="{ hover }">
      <v-carousel
        cycle
        height="400"
        hide-delimiter-background
        show-arrows-on-hover
      >
        <v-carousel-item v-for="(contest, i) in contestInfo" :key="i"
          :src="contest.imgUrl"
          @click="redirect('/contest/' + contest.id)"
        >
        <v-expand-transition>
          <div
            v-if="hover"
            class="d-flex transition-fast-in-fast-out v-card--reveal white--text blue lighten-2 text-h4"
            style="height: 60%;"
          >
            {{contest.title}}
          </div>
        </v-expand-transition>
        </v-carousel-item>
      </v-carousel>
    </v-hover>
    <!--v-carousel
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
    </v-carousel-->
    <v-container>
      <v-row>
      <v-chip class="ma-2 ml-4" color="indigo" label text-color="white">
        <v-icon class="material-icons mr-1">event</v-icon>
        热门赛事
      </v-chip>
      <v-spacer></v-spacer>
      <v-btn
        text
        class="ma-2 mr-4"
        color="primary"
        @click="redirect('/search')"
      >
        更多竞赛》
      </v-btn>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-col v-for="contest in contestInfo" :key="contest.id" cols="12" sm="3">
          <contest-card :contest="contest" hoverColor="indigo"></contest-card>
        </v-col>
      </v-row>  
    </v-container>
    <v-container
      v-for="item in moduleContest"
      :key="item.moduleName"
    >
    <v-row>
      <v-chip class="ma-2 ml-4" :color="item.color" label text-color="white">
        <v-icon class="material-icons mr-1">event</v-icon>
        {{item.moduleName}}赛事
      </v-chip>
      <v-spacer></v-spacer>
      <v-btn
        text
        class="ma-2 mr-4"
        color="primary"
        @click="redirect('/search/' + item.moduleName)"
      >
        更多{{item.moduleName}}竞赛》
      </v-btn>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-col v-for="contest in item.contest" :key="contest.id" cols="12" sm="3">
          <contest-card :contest="contest" :hoverColor="item.color"></contest-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import { logState } from "@/mixins/logState.js";
import { requestPost, requestUploadPictures } from "@/network/request.js";
import ContestCard from "@/components/ContestInfo/ContestCard.vue"
import NoticeViewer from "@/components/NoticeComponent/NoticeViewer.vue";
export default {
  name: "HomePage",
  mixins: [redirect, snackbar, filter, logState],
  watch: {
    $route(val) {
      this.selectPage(val.params.option);
    },
  },
  components: { NoticeViewer, ContestCard },
  methods: {
    selectPage(param) {
      this.page = !param || param == "" ? "signup" : param;
      if (!["signup", "emailcheck", "verification"].includes(this.page))
        this.redirect("/pagenotfound");
    },
    getContest(){
      const params = this.getContestFilter({censorStatus: 'Accept'});
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
            // console.log(this.contestInfo);
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
    },
    getModuleContest(){
      for(let i=0; i<5 ; ++i){
        const params = this.getContestFilter({censorStatus: 'Accept', module:[this.moduleContest[i].moduleName]});
        // console.log(params);
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
              this.moduleContest[i].contest = res.data.data;
              console.log(this.moduleContest[i].contest);
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
    }
  },
  created() {
    this.isLoading = true;
    this.selectPage(this.$route.params.option);
    this.getContest();
    this.getModuleContest();
    this.isLoading = false;
  },
  data() {
    return {
      page: "",
      email: "",
      isLoading: true,
      /*
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
      */

      // 头版赛事
      contestInfo: {},
      moduleContest:[
        { contest: {}, moduleName: '数学', color: 'indigo lighten-2' },
        { contest: {}, moduleName: '计算机', color: 'blue lighten-1'},
        { contest: {}, moduleName: '物理', color: 'light-blue lighten-2'},
        { contest: {}, moduleName: '文学', color: 'cyan lighten-2'},
        { contest: {}, moduleName: '艺术', color: 'teal lighten-1'},
      ],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.v-card--reveal {
  align-items: center;
  bottom: 0;
  justify-content: center;
  opacity: .85;
  position: absolute;
  width: 100%;
}
</style>
