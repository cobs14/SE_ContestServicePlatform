<template>
  <v-card>
    <v-card-title>
      报名管理
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-btn class="info ma-2">
      一键通过
    </v-btn>
    <v-data-table
      :headers="headers"
      :items="registerList"
      :search="search"
    ></v-data-table>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";

export default {
  components: {},
  name: "RegisterManagerSingle",
  mixins: [redirect, snackbar, logState],
  methods: {},
  props: {
    registerList: Array,
  },
  created() {
    console.log(this.registerList);
  },
  data() {
    return {
      isLoading: true,
      search: '',
      headers: [
        { text: '用户名', value: 'username'},
        { text: '真实姓名', value: 'trueName'},
        { text: '学校', value: 'school'},
        { text: '专业', value: 'major' },
        { text: '',  value: 'actions'}
      ]
    };
  },
};
</script>