<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <v-row no-gutters>
        <v-col cols="4">
          {{ info.title }}
        </v-col>
        <v-col cols="8" class="text--secondary">
          <span>
            {{ info.sponsor }}
          </span>
        </v-col>
      </v-row>
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-row no-gutters>
        <v-col cols="8">
          <v-container>
            竞赛简介：
            <br />
            {{ info.abstract }}
          </v-container>
        </v-col>
        <v-col cols="4">
          <v-text-field
            label="填写审核意见"
            v-model="message"
            outlined
            :counter="64"
          >
          </v-text-field>
        </v-col>
      </v-row>

      <v-card-actions>
        <v-btn class="info" @click="redirect('/contest/' + info.id)">
          查看预览
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn class="error" @click="rejectApplication"> 拒绝 </v-btn>
        <v-btn class="success" @click="approveApplication"> 审核通过 </v-btn>
      </v-card-actions>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
// 管理员审核竞赛的页面
import { requestPost } from "@/network/request.js";
import { snackbar } from "@/mixins/message.js";
import { redirect } from "@/mixins/router.js";
import { logState } from "@/mixins/logState.js";
export default {
  name: "AdminContestPanel",
  mixins: [snackbar, redirect, logState],
  components: {},
  methods: {
    // 拒绝竞赛审批
    rejectApplication() {
      this.sendCensor(0);
    },

    // 通过竞赛审批
    approveApplication() {
      this.sendCensor(1);
    },

    // 发送请求
    sendCensor(status) {
      requestPost(
        {
          url: "/contest/status",
          data: {
            id: this.info.id,
            message: this.message,
            status: status,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          if (res.data.error == undefined) {
            const msg =
              "成功" +
              (status ? "通过 " : "拒绝 ") +
              this.info.title +
              " 的竞赛创建申请";
            this.snackbar(msg, "success");
            setTimeout(() => {
              this.redirect("/admin");
            }, 1000);
          } else {
            this.snackbar("出错啦，错误原因：" + res.data.error, "error");
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
        });
    },
  },
  props: {
    info: Object,
  },
  data() {
    return {
      message: "",
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
