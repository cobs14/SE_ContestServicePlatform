<template>
  <div id="HomePage">
    <div v-if="isLoading" >
      <v-skeleton-loader type="carousel" class="my-0" height="400"></v-skeleton-loader>
    </div>
    <v-carousel
      v-if="!isLoading"
      cycle
      height="400"
      hide-delimiter-background
      show-arrows-on-hover
    >
      <v-carousel-item v-for="(contest, i) in contestInfo[0].contest" :key="i"
        :src="contest.imgUrl"
        @click="redirect('/contest/' + contest.id)"
      >
        <div
          class="d-flex v-card--reveal white--text grey text-h4"
          style="height: 30%;"
        >
          {{contest.title}}
        </div>
      </v-carousel-item>
    </v-carousel>
    <v-container
      v-for="item in contestInfo"
      :key="item.moduleName"
    >
    <v-row>
      <v-chip class="ma-2 ml-4" :color="item.color" label text-color="white">
        <v-icon class="material-icons mr-1">event</v-icon>
        {{item.moduleName === '' ? '热门' : item.moduleName}}赛事
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
      <v-row v-if="isLoading">
        <v-col v-for="index of 4" :key="index" cols="12" sm="3">
          <v-skeleton-loader
            class="mx-auto"
            max-width="300"
            type="card"
          ></v-skeleton-loader>
        </v-col>
      </v-row>
      <v-row v-if="!isLoading">
        <v-col v-for="contest in item.contest" :key="contest.id" cols="12" sm="3">
          <contest-card :contest="contest" :hoverColor="item.color"></contest-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
// 主页：竞赛轮播图和推荐卡片
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
    // 按照不同的规则获取竞赛并显示
    getContest(){
      for(let i=0; i<6 ; ++i){
        var filter = {censorStatus: 'Accept', module: []};
        if(this.contestInfo[i].moduleName !== ''){
          filter.module = [this.contestInfo[i].moduleName];
        }
        const params = this.getContestFilter(filter);
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
              this.contestInfo[i].contest = res.data.data;
              if(i === 5){
                this.isLoading = false;
              }
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
  },
  created() {
    // 页面创建后自动开始加载推荐竞赛
    this.isLoading = true;
    this.getContest();
  },
  data() {
    return {
      page: "",
      email: "",
      isLoading: true,

      contestInfo:[
        { contest: {}, moduleName: '', color: 'indigo'},
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
