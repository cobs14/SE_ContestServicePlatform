<template>
  <div id="UserCenterPage" style="display: flex">
    <aside>
    <v-card height="100%"
            min-height="1200"
            max-width="360"
            :dark="true"
            tile
    >
      <v-navigation-drawer permanent>
      <v-list-item>
          <v-list-item-content>
          <v-list-item-title class="title" style="text-align: center">
              用户界面
          </v-list-item-title>
          <v-list-item-subtitle style="text-align: center">
              User
          </v-list-item-subtitle>
          </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list
          dense
          nav
      >
          <v-list-item
          v-for="item in navigation"
          :key="item.title"
          :link=true
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
    <div class="main" style="display: block; width: 100%; height: 100%;">
    <div style="margin: 0; background: white; width: 100%; height: 80px">
      <v-breadcrumbs :items="paths" divider="-"></v-breadcrumbs>
    </div>
    <v-container v-if="page === 'info'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
      <user-card
        :info="userInfo"
        @showSnackbar="snackbar"
      ></user-card>
    </v-container>
    <v-container v-if="page === 'contest'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
    </v-container>
    <v-container v-if="page === 'user'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
      <v-row>
        <v-col>
          <user-info-bar
            :info="userInfo"
          ></user-info-bar>
        </v-col>
        <v-col>
          <user-info-bar
            :info="userInfo"
          ></user-info-bar>
        </v-col>
      </v-row>
    </v-container>
    <v-container v-if="page === 'sponsor'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
    </v-container>
    </div>
  </div>
</template>

<script>
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js"
import UserCard from "@/components/UserCard.vue"
import UserInfoBar from "@/components/UserInfoBar.vue"
export default {
  name: 'UserCenterPage',
  mixins: [redirect, snackbar, logState],
  components:{
    UserCard,
    UserInfoBar
  },
  methods:{
    getUserInfo(){
      requestPost({
        url: "/user",
      },
      this.getUserJwt())
        .then((res) => {
          if (res.data.error == undefined) {
            this.userInfo = res.data;
            console.log("Get User Info: ");
            console.log(this.userInfo);          
          } else {
            this.snackbar("出错啦，错误原因：" + res.data.error, "error");
          }
        })
        .catch((err) => {
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
        });
    }
  },
  created(){
    this.getUserInfo();
  },
  data () {
    return {
      page: 'info',
      tab: '',
      userInfo: {},
      navigation: [
        { icon: 'playlist_add_check', title: '我的信息', page: 'info'},
        { icon: 'how_to_reg', title: '我的竞赛', page: 'contest' },
        { icon: 'portrait', title: '我的联系人', page: 'user' },
        // { icon: 'portrait', title: '关注的主办方', page: 'sponsor'}
      ],
    }
  },
  computed:{
    paths() {
      return [
        {
          text: '用户中心',
          disabled: false
        },
        {
          text: hashtable[this.page],
          disabled: false
        }
      ]
    }
  }
}
const hashtable = {
  "info": "我的信息",
  "contest": "我的竞赛",
  "user": "我的联系人",
  // "sponsor": "关注的主办方",
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
