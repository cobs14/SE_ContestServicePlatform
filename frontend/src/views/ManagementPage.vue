<template>
  <div id="ManagePage" style="display: flex">
    <aside>
      <v-card height="100%" min-height="1200" max-width="360" :dark="true" tile>
        <v-navigation-drawer permanent>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="title" style="text-align: center">
                竞赛管理页面
              </v-list-item-title>
              <v-list-item-subtitle style="text-align: center">
                Manage
              </v-list-item-subtitle>
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
      <v-container v-if="page === 'create'">
        <contest-create
          v-on:goto-list="page = 'list'"
          @showSnackbar="snackbar"
        ></contest-create>
      </v-container>
      <v-container v-if="page === 'list'">
        <contest-loader />
      </v-container>
      <v-container v-if="page === 'message'">
        <message-center @showSnackbar="snackbar" />
      </v-container>
    </div>
  </div>
</template>

<script>
import { snackbar } from "@/mixins/message.js";
import { redirect } from "@/mixins/router.js";
import ContestCreate from "@/components/ContestManager/ContestCreate.vue";
import MessageCenter from "@/components/NoticeComponent/MessageCenter.vue";
import ContestLoader from "@/components/ContestInfo/ContestLoader.vue";
export default {
  name: "ManagementPage",
  mixins: [snackbar, redirect],
  inject: ["checkUserType"],
  components: {
    ContestCreate,
    ContestLoader,
    MessageCenter,
  },
  created() {
    this.checkUserType();
  },
  methods: {},
  data() {
    return {
      page: "list",
      navigation: [
        { icon: "add", title: "创建竞赛", page: "create" },
        { icon: "list", title: "竞赛管理", page: "list" },
        { icon: "message", title: "通知中心", page: "message" },
      ],
    };
  },
  computed: {
    paths() {
      return [
        {
          text: "竞赛管理",
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
  create: "创建竞赛",
  list: "竞赛管理",
  message: "通知中心",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
