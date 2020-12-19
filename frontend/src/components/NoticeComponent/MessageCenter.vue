<template>
  <v-card id="MessageCenter">
    <v-skeleton-loader v-if="isLoading" type="list-item-avatar-three-line@3">
    </v-skeleton-loader>
    <v-toolbar v-show="!isLoading" flat color="primary" dark>
      <v-toolbar-title>通知中心</v-toolbar-title>
    </v-toolbar>
    <div v-show="!isLoading">
      <div v-if="contactList.length > 0">
        <v-tabs v-model="tab" show-arrows @change="setCurrentContact">
          <v-tab v-for="(contact, i) in contactList" :key="i">
            <v-badge
              :value="contact.newMessage"
              bordered
              color="red"
              dot
              overlap
              class="mx-4"
            >
              <v-avatar size="22">
                <img
                  v-if="contact.avatar && contact.avatar != ''"
                  :src="contact.avatar"
                  @error="contact.avatar = ''"
                />
                <img v-else :src="defaultHead" />
              </v-avatar>
            </v-badge>
            {{ contact.username }}
          </v-tab>
        </v-tabs>
        <chat-box v-if="!tabChanged" :contactInfo="contactList[tab]" />
      </div>
      <v-card-title v-else>您还没有任何通知</v-card-title>
    </div>
  </v-card>
</template>

<script>
import { requestPost, downloadFile } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
import { logState } from "@/mixins/logState.js";
import ChatBox from "@/components/MessageComponents/ChatBox.vue";
export default {
  name: "MessageCenter",
  mixins: [redirect, snackbar, filter, logState],
  components: {
    ChatBox,
  },
  methods: {
    setCurrentContact(newTab) {
      console.log("new tab", newTab);
      this.contactList[newTab].newMessage = 0;
      this.tabChanged = true;
      this.$nextTick(() => {
        this.tabChanged = false;
      });
    },
    fetchMessage() {
      this.isFetching = true;
      console.log("we are gonna download,", this.notice);
      requestPost(
        {
          url: "/message/getmessage",
          data: {
            type: "Any",
            currentContactId: -1,
            pageNum: 1,
            pageSize: 100,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.isFetching = false;
          switch (res.data.error) {
            case undefined:
              this.contactList = res.data.contact;
              this.isLoading = false;
              break;
            case "login":
              this.clearLogInfo();
              break;
            default:
              this.isLoading = false;
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
          this.isFetching = false;
        });
    },
  },
  data() {
    return {
      tab: 0,
      tabChanged: false,
      contactList: [],
      isLoading: true,
      defaultHead: require("../../../static/images/defaultHead.jpg"),
    };
  },
  created() {
    this.fetchMessage();
  },
  props: {},
};
</script>

<style>
</style>