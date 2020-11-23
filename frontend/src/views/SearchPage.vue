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
        </v-tab-item>
      </v-tabs-items>
      <v-pagination
        v-model="page"
        :length="totalPages"
        @input="onChangePage"
      ></v-pagination>
      <v-skeleton-loader v-if="isLoading" type="list-item-avatar-three-line@3">
      </v-skeleton-loader>
      <v-tabs-items
        v-model="tab"
        v-if="!isLoading && options[tab].items.length > 0"
      >
        <v-tab-item v-for="option in options" :key="option.title">
          233
        </v-tab-item>
        <div v-if="options[0].items.length > 0">
          <v-tab-item v-for="item in options[0].items" :key="item.id">
            What loaded now is: {{ item.title }} <br />
          </v-tab-item>
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
import SearchContest from "@/components/SearchContest.vue";
export default {
  name: "SearchPage",
  mixins: [redirect, snackbar],
  watch: {},
  components: { SearchContest },
  methods: {
    refreshList(index, resetPage = false) {
      console.log(index, this.options[index].params);
      this.isLoading = true;
      if (resetPage) {
        this.oldPage = 1;
        this.page = 1;
      }
      requestPost({
        url: "/contest/retrieve",
        data: {
          params: this.options[index].params,
          pageNum: this.page,
          pageSize: this.pageSize,
        },
      })
        .then((res) => {
          //TODO: do send & refresh logic here
          //TODO: refresh & check pagination logic
          this.isLoading = false;
          console.log("ok", res, res.data);
          if (res.data.error == undefined) {
            let data = res.data.data;
            let count = res.data.count;
            this.totalPages = Math.max(
              1,
              Math.ceil(this.totalPages / this.pageSize)
            );
            this.page = Math.min(this.totalPages, this.page);
            this.options[index].items = data;
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
      console.log("tab", this.tab);
      this.refreshList(this.tab, true);
      //TODO: do tab logic here
    },
    onChangePage() {
      if (this.oldPage == this.page) {
        return;
      }
      console.log("page", this.page);
      this.oldPage = this.page;
      this.refreshList(this.tab);
      //TODO: do page logic here.
    },
  },
  created() {
    console.log(this.keyword);
    this.onChangeTab();
    this.$route.params.keyword;
  },
  data() {
    return {
      tab: 0,
      oldPage: 1,
      page: 1,
      totalPages: 1,
      pageSize: 20,
      isLoading: false,
      options: [
        { icon: "mdi-account", title: "竞赛", params: Object, items: [] },
        { icon: "mdi-account", title: "用户", params: Object, items: [] },
        { icon: "mdi-lock", title: "社区", params: Object, items: [] },
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
