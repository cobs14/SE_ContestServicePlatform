<template>
  <v-container tile id="ChatBox">
    <v-skeleton-loader v-if="isLoading" type="list-item-avatar-three-line@3">
    </v-skeleton-loader>
    <v-card
      v-show="!isLoading"
      flat
      class="overflow-y-auto"
      max-height="400"
      ref="chatArea"
    >
      <v-container v-for="(msg, i) in msgList" :key="i" tile>
        <v-row>
          <v-spacer v-if="isMe(msg)"></v-spacer>
          <v-card
            :dark="isMe(msg)"
            :class="'mx-3 ' + (isMe(msg) ? 'success' : 'grey lighten-3')"
            min-width="30%"
            max-width="90%"
          >
            <v-card-text>
              {{ parseTimestamp(msg.sendTime, true) }}：
              <br />
              {{ msg.content }}</v-card-text
            >
          </v-card>
          <v-spacer v-if="!isMe(msg)"></v-spacer>
        </v-row>
      </v-container>
      <div id="chatBoxBottom"></div>
    </v-card>

    <v-card-actions v-if="contactInfo.id > 0">
      <v-text-field
        class="mt-3"
        v-model="newMsg"
        :placeholder="
          userType === 'guest'
            ? '请先前往个人中心页面进行实名验证后发送消息'
            : ''
        "
        :disabled="userType === 'guest' || sendingMsg"
        :loading="sendingMsg"
        @keyup.enter="sendMsg"
      ></v-text-field>
      <v-btn
        class="success darken-1 ml-3"
        fab
        small
        :disabled="userType === 'guest' || sendingMsg"
        :loading="sendingMsg"
        @click="sendMsg"
      >
        <v-icon small> send </v-icon>
      </v-btn>
    </v-card-actions>
  </v-container>
</template>

<script>
// 通用聊天框组件（也可以用于显示系统通知）
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { requestPost } from "@/network/request.js";
import { logState } from "@/mixins/logState.js";
import { snackbar } from "@/mixins/message.js";
import * as dateParser from "@/assets/datetime.js";
export default {
  name: "ChatBox",
  mixins: [redirect, snackbar, logState],
  methods: {
    // 时间戳的解析
    parseTimestamp(timestamp) {
      return dateParser.secondTimestampParser(timestamp);
    },
    // 判断发信人是否为用户本人
    isMe(msg) {
      return msg.sender != this.contactInfo.id;
    },
    // 发送消息时调用的方法
    sendMsg() {
      if (this.newMsg.trim() == "") {
        this.snackbar("您不能发送空消息", "warning");
        return;
      }
      this.sendingMsg = true;
      requestPost(
        {
          url: "/message/newmessage",
          data: {
            contactId: this.contactInfo.id,
            content: this.newMsg,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          this.sendingMsg = false;
          switch (res.data.error) {
            case undefined:
              this.loadMsg(true);
              this.newMsg = "";
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
          this.sendingMsg = false;
          this.snackbar("服务器开小差啦，请稍后再尝试加载", "error");
          console.log("error", err);
        });
    },
    // 当有新消息时，将页面定位到消息最下方
    scrollToBottom() {
      document.getElementById("chatBoxBottom").scrollIntoView(false);
    },
    // 加载消息
    loadMsg(directToBottom = false) {
      requestPost(
        {
          url: "/message/currentmessage",
          data: {
            currentContactId: this.contactInfo.id,
          },
        },
        this.getUserJwt()
      )
        .then((res) => {
          switch (res.data.error) {
            case undefined:
              this.isLoading = false;
              this.msgList = res.data.currentMessage;
              this.$nextTick(() => {
                if (directToBottom) {
                  this.scrollToBottom();
                }
              });
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
        });
    },
  },
  props: {
    contactInfo: Object,
  },

  created() {
    this.userType = this.getUserType();
    // 每2.5秒刷新一次
    this.isLoading = true;
    this.loadMsg(true);
    this.timer = setInterval(() => {
      this.loadMsg();
    }, 2500);
  },
  mounted() {
    this.scrollToBottom();
  },
  // 离开页面前销毁计时器
  destroyed() {
    clearInterval(this.timer);
  },
  data() {
    return {
      timer: undefined,
      msgList: [],
      sendingMsg: false,
      newMsg: "",
      isLoading: false,
      userType: "",
    };
  },
};
</script>