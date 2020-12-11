<template>
  <div id="SearchPage">
    <!-- <v-container>
      <v-btn class="mx-2" fab dark color="teal">
        <v-icon dark> mdi-format-list-bulleted-square </v-icon>
      </v-btn>
    </v-container> -->
    <v-container>
      <v-tabs v-model="tab" @change="onChangeTab">
        <v-tab v-for="option in options" :key="option.title">
          <v-icon left> {{ option.icon }} </v-icon>
          {{ option.title }}
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item v-for="option in options" :key="option.title" class="mb-3">
          <search-contest
            v-show="tab == 0"
            v-bind:contestParams.sync="options[0].params"
            @refreshList="refreshList"
            @showSnackbar="snackbar"
          >
          </search-contest>

          <search-user
            v-show="tab == 1"
            v-bind:userParams.sync="options[1].params"
            @refreshList="refreshList"
            @showSnackbar="snackbar"
          >
          </search-user>
        </v-tab-item>
      </v-tabs-items>
      <v-pagination
        v-model="page"
        :length="totalPages"
        @input="onChangePage"
      ></v-pagination>

      <user-info-bar
        @showSnackbar="snackbar"
        :info="{
          avatar: 'https://cdn.vuetifyjs.com/images/john.jpg',
          id: 1,
          username: 'Sponsor',
          school: '清华大学',
          major: '软件工程',
        }"
      >
      </user-info-bar>

      <user-info-bar
        @showSnackbar="snackbar"
        :info="{
          avatar: 'https://cdn.vuetifyjs.com/images/john.jpg',
          id: 2,
          username: 'User',
          school: '清华大学',
          major: '软件工程',
        }"
      >
      </user-info-bar>

      <v-skeleton-loader v-if="isLoading" type="list-item-avatar-three-line@3">
      </v-skeleton-loader>
      <v-tabs-items
        v-model="tab"
        v-if="!isLoading && options[tab].items.length > 0"
      >
        <div v-if="tab == 0 && options[0].items.length > 0">
          <contest-info-bar
            v-for="item in options[0].items"
            :info="item"
            :key="item.id"
            @showSnackbar="snackbar"
          />
        </div>

        <div v-if="tab == 1 && options[1].items.length > 0">
          <user-info-bar
            v-for="item in options[1].items"
            :info="item"
            :key="item.id"
            @showSnackbar="snackbar"
          />
        </div>
      </v-tabs-items>
      <v-card-title v-if="!isLoading && options[tab].items.length == 0">
        未能找到满足要求的信息
      </v-card-title>
      <v-pagination
        v-model="page"
        :length="totalPages"
        @input="onChangePage"
      ></v-pagination>
    </v-container>
  </div>
</template>

<script>
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import {logState} from "@/mixins/logState.js";
import SearchContest from "@/components/SearchContest.vue";
import ContestInfoBar from "@/components/ContestInfoBar.vue";
import SearchUser from "@/components/SearchUser.vue";
import UserInfoBar from "@/components/UserInfoBar.vue";
export default {
  name: "SearchPage",
  mixins: [redirect, snackbar, filter, logState],
  components: { SearchContest, ContestInfoBar, SearchUser, UserInfoBar },
  methods: {
    refreshList(index, resetPage = false) {
      //console.log('we gonna search...', index, this.options[index].params);

      this.isLoading = true;
      if (resetPage) {
        this.oldPage = 1;
        this.page = 1;
      }
      requestPost({
        url: this.options[index].url,
        data: {
          params: this.options[index].params,
          pageNum: this.page,
          pageSize: this.pageSize,
        },
      }, this.getUserJwt())
        .then((res) => {
          //TODO: do send & refresh logic here
          //TODO: refresh & check pagination logic
          this.isLoading = false;
          if (res.data.error == undefined) {
            let data = res.data.data;
            let count = res.data.count;
            this.totalPages = Math.max(
              1,
              Math.ceil(this.totalPages / this.pageSize)
            );
            this.page = Math.min(this.totalPages, this.page);
            this.options[index].items = data;
            //console.log(data, this.options[index]);
          } else {
            this.snackbar("出错啦，错误原因：" + res.data.error, "error");
            this.options[index].items = [];
            this.totalPages = 1;
            this.page = 1;
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          this.isLoading = false;
          console.log("error", err);
        });
    },
    onChangeTab() {
      //console.log("tab", this.tab);
      this.refreshList(this.tab, true);
    },
    onChangePage() {
      if (this.oldPage == this.page) {
        return;
      }
      //console.log("page", this.page);
      this.oldPage = this.page;
      this.refreshList(this.tab);
    },
  },
  created() {
    //console.log("keyword", this.keyword, this.$route.params.keyword);
    //TODO: add other params later
    this.options[0].params = this.getContestFilter();
    this.options[1].params = this.getUserFilter();
    if (this.keyword != undefined) {
      //TODO: FIXME:
      //if some of the characters can't be parsed properly
      //check here.
      this.keyword = decodeURIComponent(this.keyword);
      //console.log('decoded', this.keyword);
      this.options[0].params["text"].push(this.keyword);
    }
    //console.log("original params", this.options[0]);
    console.log('search params', this.options[0]);
    this.refreshList(this.tab, true);
  },
  data() {
    return {
      tab: 0,
      oldPage: 1,
      page: 1,
      totalPages: 1,
      pageSize: 20,
      isLoading: false,
      //TODO: change url when necessary
      options: [
        {
          icon: "mdi-account",
          title: "竞赛",
          url: "/contest/retrieve",
          params: Object,
          items: [],
        },
        {
          icon: "mdi-account",
          title: "用户",
          url: "/user/retrieve",
          params: Object,
          items: [],
        },
        {
          icon: "mdi-lock",
          title: "社区",
          url: "todohere",
          params: Object,
          items: [],
        },
      ],
      keyword: this.$route.params.keyword,
      email: "",
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
