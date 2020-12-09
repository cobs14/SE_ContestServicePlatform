<template>
  <div id="ContestManagePage" style="display: flex">
    <aside>
      <v-card height="100%" min-height="1200" max-width="360" dark tile>
        <v-navigation-drawer permanent>
          <v-list-item>
            <v-list-item-content>
              <v-btn @click="redirect('/management')">返回上一级</v-btn>
              <v-list-item-title class="title my-2" style="text-align: center">
                {{ contestInfo.title }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          <v-list dense nav>
            <v-list-item
              v-for="item in navigation"
              :key="item.title"
              :link="true"
              @click="page = item.page"
            >
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
      </v-card>
    </aside>
    <div class="main" style="display: block; width: 100%">
      <div>
        <v-breadcrumbs :items="paths" divider="-"></v-breadcrumbs>
      </div>
      <v-container v-if="page === 'notice' && !isLoading">
        <notice-manager :contestInfo="contestInfo" @showSnackbar="snackbar"/>
      </v-container>
    </div>
  </div>
</template>

<script>
import { snackbar } from "@/mixins/message.js";
import { redirect } from "@/mixins/router.js";
import { requestPost } from "@/network/request.js";
import { filter } from "@/mixins/filter.js";
import { logState } from "@/mixins/logState.js";
import SponsorContestLoader from "@/components/SponsorContestLoader.vue";
import NoticeManager from "@/components/ContestManager/NoticeManager.vue";
export default {
  name: "ContestManagePage",
  mixins: [snackbar, redirect, logState, filter],
  components: {
    SponsorContestLoader,
    NoticeManager,
  },
  methods: {
    pageNotFound() {
      this.softReload("/pagenotfound");
      this.snackbar("您查找的页面不存在或没有足够的权限查看它", "error");
    },
  },
  data() {
    return {
      page: "notice",
      navigation: [{ icon: "list", title: "公告管理", page: "notice" }],
      isLoading: true,
      contestInfo: Object,
    };
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
        this.isLoading = false;
        if (res.data.error == "login") {
          this.clearLogInfo();
        } else if (res.data.data.length > 0) {
          this.contestInfo = res.data.data[0];
        } else {
          this.pageNotFound();
        }
      })
      .catch((err) => {
        this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
        console.log("error", err);
        this.softReload("/management");
        this.isLoading = false;
      });
  },
  computed: {
    paths() {
      return [
        {
          text: "竞赛管理",
          disabled: false,
        },
        {
          text: this.contestInfo.title,
          disabled: false,
        },
        {
          text: hashtable[this.page],
          disabled: false,
        },
      ];
    },
  },
};
const hashtable = {
  notice: "公告管理",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
