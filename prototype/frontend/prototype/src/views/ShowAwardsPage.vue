<template>
  <div id="ShowAwardsPage">
    <v-container>
      <submitFileDlg
        :dialog="dlg.submitFile"
        v-on:disable="dlg.submitFile = false"
        v-on:routeTo="routeTo"
        eager
      >
      </submitFileDlg>
      <showAwardsDlg
        :dialog="dlg.awards"
        v-on:disable="dlg.awards = false"
        v-on:routeTo="routeTo"
        eager
      >
      </showAwardsDlg>
      <v-row>
        <v-col>
          <v-card-title class="font-weight-black mb-1" style="font-size: 2.2em">
            获奖信息查询
          </v-card-title>
          <v-card-subtitle
            class="font-weight-black grey--text text--darken-1"
            style="font-size: 1.4em"
          >
            全国大学生算法竞赛
          </v-card-subtitle>
        </v-col>
        <v-spacer> </v-spacer>
        <v-card elevation="0" text>
          <v-card-title class="grey--text text--darken-2 mt-2">
            比赛已结束
          </v-card-title>
        </v-card>
      </v-row>
      <v-img
        src="https://publicqn.saikr.com/2020/09/25/contest5f6dacbecf3c23.844776221601023249623.png?imageView2/2/w/1080"
      />
      <v-divider> </v-divider>
      <v-card elevation="0" text style="min-height: 1200px" class="mt-2">
        <v-card>
          <v-row class="ml-3">
            <v-card-subtitle
              class="font-weight-black grey--text text--darken-1 mt-2"
              style="font-size: 1.2em"
            >
              参赛者姓名
            </v-card-subtitle>
            <v-card-title
              class="font-weight-black"
              style="font-size: 1.5em"
            >
              张三
            </v-card-title>
            <v-spacer> </v-spacer>
          </v-row>

          <v-row class="ml-3">
            <v-card-subtitle
              class="font-weight-black grey--text text--darken-1 mt-2"
              style="font-size: 1.2em"
            >
              证书编号
            </v-card-subtitle>
            <v-card-title
              class="font-weight-black"
              style="font-size: 1.5em"
            >
              C12345678
            </v-card-title>
            <v-spacer> </v-spacer>
          </v-row>

          <v-row class="ml-3">
            <v-card-subtitle
              class="font-weight-black grey--text text--darken-1 mt-2"
              style="font-size: 1.2em"
            >
              竞赛名称
            </v-card-subtitle>
            <v-card-title
              class="font-weight-black"
              style="font-size: 1.5em"
            >
              全国大学生算法竞赛
            </v-card-title>
            <v-spacer> </v-spacer>
          </v-row>

          <v-row class="ml-3">
            <v-card-subtitle
              class="font-weight-black grey--text text--darken-1 mt-2"
              style="font-size: 1.2em"
            >
              所获奖项
            </v-card-subtitle>
            <v-card-title
              class="font-weight-black"
              style="font-size: 1.5em"
            >
              个人编程一等奖
            </v-card-title>
            <v-spacer> </v-spacer>
            <v-card-subtitle
              class="font-weight-black grey--text text--darken-1 mt-2"
              style="font-size: 1.2em"
            >
              获奖时间
            </v-card-subtitle>
            <v-card-title
              class="font-weight-black"
              style="font-size: 1.5em"
            >
              2020年11月6日
            </v-card-title>
            <v-spacer> </v-spacer>
          </v-row>

          <v-row class="ml-3">
            <v-card-subtitle
              class="font-weight-black grey--text text--darken-1 mt-2"
              style="font-size: 1.2em"
            >
              所在院校
            </v-card-subtitle>
            <v-card-title
              class="font-weight-black"
              style="font-size: 1.5em"
            >
              华清小学
            </v-card-title>
            <v-spacer> </v-spacer>
            <v-card-subtitle
              class="font-weight-black grey--text text--darken-1 mt-2"
              style="font-size: 1.2em"
            >
              就读专业
            </v-card-subtitle>
            <v-card-title
              class="font-weight-black"
              style="font-size: 1.5em"
            >
              硬件工程
            </v-card-title>
            <v-spacer> </v-spacer>
          </v-row>

          <v-row class="ml-3">
            <v-card-subtitle
              class="font-weight-black grey--text text--darken-1 mt-2"
              style="font-size: 1.2em"
            >
              身份证号
            </v-card-subtitle>
            <v-card-title
              class="font-weight-black"
              style="font-size: 1.5em"
            >
              1504****1234
            </v-card-title>
            <v-spacer> </v-spacer>
            <v-card-subtitle
              class="font-weight-black grey--text text--darken-1 mt-2"
              style="font-size: 1.2em"
            >
              在校身份验证
            </v-card-subtitle>
            <v-card-title
              class="font-weight-black"
              style="font-size: 1.5em"
            >
              已通过学信网验证
            </v-card-title>
            <v-spacer> </v-spacer>
          </v-row>
          <v-divider> </v-divider>

          <v-row class="ml-3">
            <v-card-subtitle
              class="font-weight-black grey--text text--darken-1 mt-2"
              style="font-size: 1.2em"
            >
              证书查询二维码
            </v-card-subtitle>
          </v-row>

          <v-row>
            <v-spacer> </v-spacer>
            <v-img
              max-height="200"
              max-width="200"
              src="https://www.saikr.com/qrc/img?size=10&text=https%3A%2F%2Fwww.saikr.com%2Fraces%2F39657"
            />
            <v-spacer> </v-spacer>
          </v-row>

          <v-divider> </v-divider>

          <v-row class="ml-3">
            <v-card-subtitle
              class="font-weight-black grey--text text--darken-1 mt-2"
              style="font-size: 1.2em"
            >
              获奖证书
            </v-card-subtitle>
          </v-row>
          <v-row>
            <v-spacer> </v-spacer>
            <v-img :src="imgUrl" max-height="600px" max-width="600px"/>
            <v-spacer> </v-spacer>
          </v-row>

          <v-row>
            <v-spacer> </v-spacer>
            <v-btn class="info ma-3" title x-large>
              导出电子版
            </v-btn>
            <v-spacer> </v-spacer>
          </v-row>
        </v-card>
      </v-card>
    </v-container>
  </div>
</template>

<script>
/* eslint-disable */
import infocard from "@/components/ManagePageCard.vue";
import submitFileDlg from "@/components/SubmitFileDlg.vue";
import showAwardsDlg from "@/components/ShowAwardsDlg.vue";
export default {
  name: "ShowAwards",
  components: {
    infocard,
    submitFileDlg,
    showAwardsDlg,
  },
  methods: {
    routeTo: function (dir) {
      this.$router.push("/");
      this.$nextTick(() => this.$router.push(dir));
    },
  },
  data() {
    return {
      imgUrl:require('../resources/certificate.png'),
      dlg: {
        submitFile: false,
        awards: false,
      },
      status: this.$route.params.status || "visitor",
      items: [
        { icon: "list", title: "竞赛级别", content: "国家赛" },
        { icon: "source", title: "报名要求", content: "在校本科生" },
        { icon: "attach_money", title: "报名费用", content: "50元" },
        {
          icon: "card_membership",
          title: "奖项设置",
          content:
            "根据得分排名，前三名为一等奖，前十名为二等奖，前五十名为三等奖",
        },
      ],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
