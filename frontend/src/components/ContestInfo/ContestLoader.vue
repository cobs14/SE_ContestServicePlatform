<template>
  <v-card id="ContestLoader" flat>
    <v-tabs v-model="tab" @change="onChangeTab">
      <v-tab>全部</v-tab>
      <v-tab>报名中</v-tab>
      <v-tab>竞赛中</v-tab>
      <v-tab>评审中</v-tab>
      <v-tab>待审核</v-tab>
      <v-tab>审核未通过</v-tab>
    </v-tabs>

    <v-pagination
      v-model="page"
      :length="totalPages"
      @input="onChangePage"
    ></v-pagination>

    <v-skeleton-loader v-if="isLoading" type="list-item-avatar-three-line@3">
    </v-skeleton-loader>
    <v-tabs-items v-model="tab" v-if="!isLoading && contestList.length > 0">
      <div v-if="contestList.length > 0">
        <v-card
          class="ma-3"
          v-for="item in contestList"
          :info="item"
          :key="item.id"
          @showSnackbar="snackbar"
        >
          <v-card-title>
            {{ item.title }}
          </v-card-title>
          <v-card-text>
            {{ item.abstract }}
          </v-card-text>
          <v-card-actions>
            <v-btn
              text
              class="blue--text"
              @click="external('/contest/' + item.id)"
            >
              竞赛详情
            </v-btn>
            <v-btn
              :disabled="item.censorStatus !== 'accept'"
              text
              class="blue--text"
              @click="redirect('/management/' + item.id)"
            >
              {{ buttonText(item) }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </v-tabs-items>
    <v-card-title v-if="!isLoading && contestList.length == 0">
      未能找到满足要求的信息
    </v-card-title>
    <v-pagination
      v-model="page"
      :length="totalPages"
      @input="onChangePage"
    ></v-pagination>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "ContestLoader",
  mixins: [redirect, snackbar, filter, logState],
  methods: {
    refreshList(index, resetPage = false) {
      this.isLoading = true;
      if (resetPage) {
        this.oldPage = 1;
        this.page = 1;
      }
      this.params = {};
      this.params.sponsorId = this.getUserId();
      if (this.tab) {
        this.params.state = {
          apply: this.tab === 1 ? 2 : 0,
          contest: this.tab === 2 ? 2 : 0,
          review: this.tab === 3 ? 2 : 0,
        };
        this.params.censorStatus = this.tab === 4 ? 'Pending' : 'Accept';
        this.params.censorStatus = this.tab === 5 ? 'Reject' : this.params.censorStatus;
      }

      this.params = this.getContestFilter(this.params);
      console.log("sponsor params", this.params);
      requestPost(
        {
          url: "/contest/retrieve",
          data: {
            params: this.params,
            pageNum: this.page,
            pageSize: this.pageSize,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isLoading = false;
          if (res.data.error == undefined) {
            let data = res.data.data;
            let count = res.data.count;
            this.totalPages = Math.max(
              1,
              Math.ceil(this.totalPages / this.pageSize)
            );
            this.page = Math.min(this.totalPages, this.page);
            this.contestList = data;
            console.log("received data", this.contestList);
          } else {
            this.snackbar("出错啦，错误原因：" + res.data.error, "error");
            this.contestList = [];
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
      this.refreshList(this.tab, true);
    },
    onChangePage() {
      if (this.oldPage == this.page) {
        return;
      }
      this.oldPage = this.page;
      this.refreshList(this.tab);
    },
    buttonText(item){
      if(item.censorStatus === 'accept'){
        return '管理竞赛';
      }else if(item.censorStatus === 'pending'){
        return '等待审核';
      }else{
        return '审核未通过，请修改后再提出申请'
      }
    }
  },
  props: {
    info: Object,
  },
  created() {
    this.refreshList(this.tab, true);
  },
  data() {
    return {
      tab: 0,
      oldPage: 1,
      page: 1,
      totalPages: 1,
      pageSize: 20,
      params: Object,
      isLoading: false,
      contestList: [],
    };
  },
};
</script>