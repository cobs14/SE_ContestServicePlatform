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
        >
          mdi-pencil
        </v-icon>
        <v-icon
          small
        >
          mdi-delete
        </v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn
          color="primary"
          @click="initialize"
        >
          Reset
        </v-btn>
      </template>
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          More info about {{ item.groupId }}
        </td>
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
      for(var userinfo of this.selected){
        id_list.push(userinfo.userId);
      }
      this.sendApplyStatus(id_list, 1);
    },
    rejectApplyMul(){
      const id_list = [];
      for(var userinfo of this.selected){
        id_list.push(userinfo.userId);
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
    // FIXME:
    registerList: Array,
  },
  created() {
    console.log(this.registerList);
  },
  data() {
    return {
      isLoading: true,
      search: '',
      selected: [],
      headers: [
        { text: '报名编号', value: 'groupId'},
        { text: '队伍名称', value: 'groupName'},
        { text: '队伍描述', value: 'description'},
        { text: '队伍人数', value: 'memberCount'},
        { text: '', value: 'data-table-expand'}
        // { text: '', value: 'actions'},
        
      ]
    };
  },
};
</script>