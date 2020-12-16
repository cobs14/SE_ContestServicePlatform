<template>
  <v-container id="ApplyManager">
    <v-card-title class="font-weight-black mb-3" style="font-size: 1.6em">
      管理 {{ contestInfo.title }} 的报名
    </v-card-title>
    <v-divider></v-divider>
    <apply-group 
      v-if="contestType === 'group'" 
      :registerList="registerList" 
      @showSnackbar="snackbar"
      @sendApply="refreshList"
      >
    </apply-group>
    <apply-single 
      v-if="contestType === 'single'" 
      :registerList="registerList" 
      @showSnackbar="snackbar"
      @sendApply="refreshList"
      >
    </apply-single>
  </v-container>
</template>

<script>
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
  methods: {
    refreshList() {
      this.isLoading = true;
      requestPost(
        {
          url: "/contest/list",
          data: {
            contestId: this.contestInfo.id,
            status: 'Pending',
            // FIXME: FIX PAGE
            pageNum: 0,
            pageSize: 0
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isLoading = false;
          console.log(res);
          switch (res.data.error) {
            case undefined:
              this.contestType = res.data.type;
              this.registerList = res.data.list;
              console.log("contest type: " + this.contestType);
              console.log("register list: " + this.registerList);
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
    this.refreshList(); 
  },
  data() {
    return {
      registerList: [],
      contestType: '', // either group or single
      isLoading: true,
    };
  },
};
</script>