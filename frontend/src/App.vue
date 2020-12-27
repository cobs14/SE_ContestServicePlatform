<template>
  <div id="app">
    <v-app>
      <v-header v-if="header.show" @showSnackbar="showSnackbar"> </v-header>
      <v-snackbar
        top
        v-model="snackbar.show"
        :timeout="3000"
        :color="snackbar.color"
      >
        {{ snackbar.message }}
        <template v-slot:action="{ attrs }">
          <v-btn dark text v-bind="attrs" @click="snackbar.show = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
      <v-main>
        <router-view v-if="body.show" @showSnackbar="showSnackbar" />
      </v-main>
      <v-footer padless>DO NOT REMOVE</v-footer>
      <v-footer padless fixed>
        <v-spacer />
        <v-btn
          @click="external('https://beian.miit.gov.cn/')"
          depressed
          class="disabled"
          >京ICP备2020045776号-1</v-btn
        >
        <v-spacer />
      </v-footer>
    </v-app>
  </div>
</template>

<script>
// 网站主框架
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import vHeader from "@/components/Framework/Header.vue";
export default {
  mixins: [redirect],
  components: {
    vHeader,
  },
  name: "App",
  data() {
    return {
      snackbar: { show: false, color: "success", message: "" },
      header: { show: true },
      body: { show: true },
    };
  },
  methods: {
    // 提供snackbar给全部子组件使用
    showSnackbar: function (arg) {
      this.snackbar.message = arg.message;
      this.snackbar.color = arg.color;
      this.snackbar.show = true;
    },
    // 提供仅刷新header的方法
    headerReload: function () {
      this.header.show = false;
      this.$nextTick(() => {
        this.header.show = true;
      });
    },
    // 提供仅刷新header和主页面的方法
    // （从而能够保留snackbar不被刷新）
    softReload: function (url = null) {
      this.headerReload();
      if (url != null) {
        this.redirect(url);
      } else {
        this.body.show = false;
        this.$nextTick(() => {
          this.body.show = true;
        });
      }
    },
    // 清除未登录用户的信息
    clearUserInfo() {
      if (this.$cookies.get("jwt")) {
        let keys = this.$cookies.keys();
        for (let key in keys) {
          this.$cookies.remove(keys[key]);
        }
      }
      this.softReload("/login");
      this.showSnackbar({
        message: "您的登录信息已过期，请重新登录",
        color: "warning",
      });
    },
    // 判断当前登录用户的类型
    checkUserType() {
      requestPost(
        {
          url: "/user",
        },
        this.$cookies.get("jwt")
      ).then((res) => {
        if (res.data.error == undefined) {
          switch (res.data.userType) {
            case "user":
              if (this.$route.path !== "/user") {
                this.redirect("user");
              }
              break;
            case "sponsor":
              if (!this.$route.path.startsWith("/management", 0)) {
                this.redirect("/management");
              }
              break;
            case "admin":
              if (this.$route.path !== "/admin") {
                this.redirect("/admin");
              }
              break;
          }
        } else if (res.data.error === "login") {
          this.clearUserInfo();
        }
      });
    },
  },
  provide() {
    return {
      softReload: this.softReload,
      snackbar: this.showSnackbar,
      headerReload: this.headerReload,
      checkUserType: this.checkUserType,
    };
  },
};
</script>
