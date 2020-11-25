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
            v-bind:params.sync="options[0].params"
            @showSnackbar="snackbar"
          >
          </search-contest>
        </v-tab-item>
      </v-tabs-items>
      <v-pagination
        v-model="page"
        :length="8"
        @input="onChangePage"
      ></v-pagination>
      <v-tabs-items v-model="tab">
        <v-tab-item v-for="option in options" :key="option.title">
          233
        </v-tab-item>
      </v-tabs-items>
      <v-pagination
        v-model="page"
        :length="8"
        @input="onChangePage"
      ></v-pagination>
    </v-container>
  </div>
</template>

<script>
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import SearchContest from "@/components/SearchContest.vue";
export default {
  name: "SearchPage",
  mixins: [redirect, snackbar],
  watch: {},
  components: { SearchContest },
  methods: {
    onChangeTab() {
      console.log("tab", this.tab);
      this.page = 1;
      //TODO: do tab logic here
    },
    onChangePage() {
      if (this.oldPage == this.page) {
        return;
      }
      console.log("page", this.page);
      this.oldPage = this.page;
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
      pageSize: 20,
      options: [
        { icon: "mdi-account", title: "竞赛", params: Object },
        { icon: "mdi-account", title: "用户", params: Object },
        { icon: "mdi-lock", title: "社区", params: Object },
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
