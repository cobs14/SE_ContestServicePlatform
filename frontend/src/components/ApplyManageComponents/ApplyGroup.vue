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
    <v-btn class="info ml-2" @click="approveApplyMul">
      一键通过
    </v-btn>
    <v-btn class="error ml-2" @click="rejectApplyMul">
      一键拒绝
    </v-btn>
    <v-data-table
      v-model="selected"
      :headers="headers"
      :items="registerList"
      :search="search"
      item-key="groupId"
      show-expand
      show-select
    >
      <template v-slot:item.actions="{ item }">
        <v-icon
          small
          class="mr-2"
          @click="approveApply(item.groupId)"
        >
          mdi-check
        </v-icon>
        <v-icon
          small
          @click="rejectApply(item.groupId)"
        >
          mdi-delete
        </v-icon>
      </template>
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length" class="pa-2">
        <v-data-table
          :headers="memberHeaders"
          :items="item.member"
          item-key="userId"
          hide-default-footer
        >
        </v-data-table>
        </td>
      </template>
      <template v-slot:no-data>
        <v-container>
          暂无报名等待审核
        </v-container>
      </template>
    </v-data-table>
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
  name: "ApplyGroup",
  mixins: [redirect, snackbar, logState],
  inject:['softReload'],
  methods: {
    approveApplyMul(){
      const id_list = [];
      for(var groupInfo of this.selected){
        id_list.push(groupInfo.groupId);
      }
      this.sendApplyStatus(id_list, 1);
    },
    rejectApplyMul(){
      const id_list = [];
      for(var groupInfo of this.selected){
        id_list.push(groupInfo.groupId);
      }
      this.sendApplyStatus(id_list, 0);
    },
    approveApply(id){
      this.sendApplyStatus([id], 1);
    },
    rejectApply(id){
      this.sendApplyStatus([id], 0);
    },
    sendApplyStatus(id, status){
      requestPost(
        {
          url: "/contest/applystatus",
          data: {
            contestId: this.contestId,
            id: id,
            status: status
          },
        },
        this.getUserJwt()
      )
      .then((res) => {
        switch (res.data.error) {
          case undefined:
            this.snackbar("审核成功", "success");
            this.$emit("sendApply");
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
        this.softReload("/management" + this.contestId);
      });
    }
  },
  props: {
    registerList: Array,
  },
  created() {
    console.log(this.registerList);
    this.contestId = this.$route.params.contestId,
    console.log("contest id: " + this.contestId);
  },
  data() {
    return {
      contestId: this.$route.params.contestId,
      search: '',
      selected: [],
      headers: [
        { text: '报名编号', value: 'groupId'},
        { text: '队伍名称', value: 'groupName'},
        { text: '队伍描述', value: 'description'},
        { text: '队伍人数', value: 'memberCount'},
        { text: '', value: 'actions'},
        { text: '', value: 'data-table-expand'}
      ],
      memberHeaders:[
        { text: '用户名', value: 'username'},
        { text: '真实姓名', value: 'trueName'},
        { text: '学校', value: 'school'},
        { text: '专业', value: 'major' },
      ]
    };
  },
};
</script>