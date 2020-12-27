<template>
  <div id="AdminPage" style="display: flex">
    <aside>
      <v-card height="100%" min-height="1200" max-width="360" :dark="true" tile>
        <v-navigation-drawer permanent>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="title" style="text-align: center">
                平台管理页面
              </v-list-item-title>
              <v-list-item-subtitle style="text-align: center">
                Admin
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
    <div class="main" style="display: block; width: 100%; height: 100%">
      <div style="margin: 0; background: white; width: 100%; height: 80px">
        <v-breadcrumbs :items="paths" divider="-"></v-breadcrumbs>
      </div>
      <v-container v-if="page === 'userinfo'">
        <v-btn class="info ma-2" @click="getUserInfo"> 刷新 </v-btn>
        <v-expansion-panels>
          <admin-user-info-panel
            @showSnackbar="snackbar"
            v-for="info in userInfo"
            :key="info.userId"
            :info="info"
          />
        </v-expansion-panels>
      </v-container>

      <v-container v-if="page === 'contest'">
        <v-btn class="info ma-2" @click="getContestInfo"> 刷新 </v-btn>
        <v-expansion-panels>
          <contest-panel
            @showSnackbar="snackbar"
            v-for="info in contestInfo"
            :key="info.name"
            :info="info"
          ></contest-panel>
        </v-expansion-panels>

        <v-pagination
          v-model="pageNum"
          :length="totalPages"
          :total-visible="7"
          @change="getContestInfo"
        ></v-pagination>
      </v-container>

      <v-container v-if="page === 'sponsor'">
        <v-row>
          <v-dialog v-model="invitationDialog" persistent max-width="290">
            <template v-slot:activator="{ attrs }">
              <v-col>
                <v-text-field
                  label="输入欲邀请组织的机构名称"
                  outlined
                  type="string"
                  v-model="invitationTruename"
                >
                </v-text-field>
              </v-col>
              <v-btn
                class="mt-5"
                color="primary"
                dark
                v-bind="attrs"
                @click="getInvitationCode"
              >
                生成主办方邀请码
              </v-btn>
            </template>
            <v-card>
              <v-card-title class="headline">
                下面是可用的主办方邀请码
              </v-card-title>
              <v-card-text>
                {{ invitationCode }}
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="green darken-1"
                  text
                  @click="invitationDialog = false"
                >
                  完成
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-spacer></v-spacer>
        </v-row>
        <v-simple-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">邀请码编号</th>
                <th class="text-left">邀请码正文</th>
                <th class="text-left">主办方用户名</th>
                <th class="text-left">是否已经使用</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="info in sponsorInfo" :key="info.code">
                <td>{{ info.codeId }}</td>
                <td>{{ info.codeText }}</td>
                <td>{{ info.trueName }}</td>
                <td>{{ info.valid ? "尚未注册" : "已经注册" }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-container>
      <v-container
        v-if="page === 'user'"
        style="
          margin: 10px;
          background: white;
          width: auto;
          height: 85%;
          border-radius: 4px;
        "
      >
      </v-container>
    </div>
  </div>
</template>

<script>
// 管理员中心页面
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import { logState } from "@/mixins/logState.js";
import ContestPanel from "@/components/AdminComponents/AdminContestPanel.vue";
import AdminUserInfoPanel from "@/components/AdminComponents/AdminUserInfoPanel.vue";
export default {
  name: "AdminPage",
  mixins: [redirect, snackbar, filter, logState],
  inject: ["checkUserType"],
  components: {
    ContestPanel,
    AdminUserInfoPanel,
  },
  methods: {
    // 创建竞赛举办者的邀请码
    getInvitationCode() {
      this.invitationDialog = false;
      if (this.invitationTruename === "") {
        this.snackbar("请输入欲邀请的机构全称", "error");
        return;
      }
      this.invitationCode = "";
      requestPost(
        {
          url: "/code/generate",
          data: {
            trueName: String(this.invitationTruename),
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          if (res.data.error == undefined) {
            this.invitationCode = res.data.code;
            this.invitationDialog = true;
            this.getSponsorInfo();
          } else {
            this.snackbar("出错啦，错误原因：" + res.data.error, "error");
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
        });
    },
    // 获取待审核竞赛的详细信息
    getContestInfo() {
      const params = this.getContestFilter({ censorStatus: "Pending" });
      requestPost(
        {
          url: "/contest/retrieve",
          data: {
            params: params,
            pageNum: this.pageNum,
            pageSize: this.pageSize,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          if (res.data.error == undefined) {
            let count = res.data.count;
            this.totalPages = Math.max(
              1,
              Math.ceil(this.totalPages / this.pageSize)
            );
            this.pageNum = Math.min(this.totalPages, this.pageNum);
            this.contestInfo = res.data.data;
          } else {
            this.snackbar("出错啦，错误原因：" + res.data.error, "error");
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
        });
    },
    // 获取竞赛举办者的信息
    getSponsorInfo() {
      requestPost(
        {
          url: "/code/browse",
        },
        this.getUserJwt()
      )
        .then((res) => {
          if (res.data.error == undefined) {
            this.sponsorInfo = res.data.data;
          } else {
            this.snackbar("出错啦，错误原因：" + res.data.error, "error");
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
        });
    },
    // 获取需要人工验证身份的用户的信息
    getUserInfo() {
      requestPost(
        {
          url: "/qualification/fetch",
        },
        this.getUserJwt()
      )
        .then((res) => {
          if (res.data.error == undefined) {
            this.userInfo = res.data.data;
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
  created() {
    // 检查用户状态
    // 如果确实是管理员，则加载相关组件和信息
    this.checkUserType();
    this.getContestInfo();
    this.getSponsorInfo();
    this.getUserInfo();
  },
  data() {
    return {
      page: "contest",
      invitationDialog: false,
      invitationTruename: "",
      pageNum: 1,
      totalPages: 1,
      pageSize: 20,
      navigation: [
        { icon: "playlist_add_check", title: "竞赛创建审核", page: "contest" },
        { icon: "how_to_reg", title: "竞赛发布者管理", page: "sponsor" },
        { icon: "fact_check", title: "用户实名信息审核", page: "userinfo" },
      ],
      invitationCode: "",
      contestInfo: [],
      sponsorInfo: [],
      userInfo: [],
    };
  },
  computed: {
    paths() {
      return [
        {
          text: "平台管理",
          disabled: false,
        },
        {
          text: hashtable[this.page],
          disabled: false,
        },
      ];
    },
  },
  watch: {
    page: function (newVal, oldVal) {
      if (newVal == "contest") {
        this.getContestInfo();
      } else if (newVal == "sponsor") {
        this.getSponsorInfo();
      } else if (newVal == "userinfo") {
        this.getUserInfo();
      }
    },
  },
};
const hashtable = {
  contest: "竞赛创建审核",
  sponsor: "竞赛发布者管理",
  userinfo: "用户实名信息审核",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
