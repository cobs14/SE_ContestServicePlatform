<template>
  <v-container id="ApplyManager">
    <v-card-title class="font-weight-black mb-3" style="font-size: 1.6em">
      管理 {{ contestInfo.title }} 的报名
    </v-card-title>
    <v-divider></v-divider>
    <v-tabs v-model="switchMode">
      <v-tab>报名成功</v-tab>
      <v-tab>待审核</v-tab>
      <v-tab-item>
        <apply-group 
          v-if="contestType === 'group'" 
          :registerList="registerList" 
          :showAction="false"
          @showSnackbar="snackbar"
          @sendApply="refreshList"
          >
        </apply-group>
        <apply-single 
          v-if="contestType === 'single'" 
          :registerList="registerList" 
          :showAction="false"
          @showSnackbar="snackbar"
          @sendApply="refreshList"
          >
        </apply-single>
      </v-tab-item>
      <v-tab-item>
        <apply-group 
          v-if="contestType === 'group'" 
          :registerList="registerList" 
          :showAction="true"
          @showSnackbar="snackbar"
          @sendApply="refreshList"
          >
        </apply-group>
        <apply-single 
          v-if="contestType === 'single'" 
          :registerList="registerList" 
          :showAction="true"
          @showSnackbar="snackbar"
          @sendApply="refreshList"
          >
        </apply-single>
      </v-tab-item>
    </v-tabs>  
  </v-container>
</template>

<script>
// 报名管理界面
// 供竞赛发布者使用
import merge from "webpack-merge";
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";
import ApplySingle from "@/components/ApplyManageComponents/ApplySingle.vue"
import ApplyGroup from "@/components/ApplyManageComponents/ApplyGroup.vue"
export default {
  components: { 
    ApplySingle,
    ApplyGroup
  },
  name: "ApplyManager",
  mixins: [redirect, snackbar, logState],
  computed:{
    manageMode(){
      return this.switchMode ? "仅查看待审核":"查看成功报名者"
    }
  },
  // 变更管理模式时重新加载列表
  watch:{
    switchMode: function(newVal, oldVal){
      this.refreshList();
    }
  },
  methods: {
    // 重新获取不同模式下报名成员的列表
    refreshList() {
      this.isLoading = true;
      requestPost(
        {
          url: "/contest/list",
          data: {
            contestId: this.contestInfo.id,
            status: this.switchMode ? 'Pending' : 'Accept',
            pageNum: 0,
            pageSize: 0
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isLoading = false;
          switch (res.data.error) {
            case undefined:
              this.contestType = res.data.type;
              this.registerList = res.data.list;
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
          this.softReload();
          this.isLoading = false;
        });
    },
  },
  props: {
    contestInfo: Object,
  },
  created() {
    // 加载时自动获取一次列表
    this.refreshList(); 
  },
  data() {
    return {
      registerList: [],
      switchMode: true,
      contestType: '', // either group or single
      isLoading: true,
    };
  },
};
</script>