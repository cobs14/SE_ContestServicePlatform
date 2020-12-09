<template>
  <v-container tile id="ChatBox">
    <v-card class="overflow-y-auto" max-height="400" ref="chatArea">
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
              <!-- <v-chip
                v-if="!isMe(msg)"
                class="mb-1"
                color="warning darken-1"
                x-small
                text-color="white"
                >新消息</v-chip
              > -->

              {{ parseTimestamp(msg.sendTime) }}：
              <br />
              {{ msg.content }}</v-card-text
            >
          </v-card>
          <v-spacer v-if="!isMe(msg)"></v-spacer>
        </v-row>
      </v-container>
      <div id="chatBoxBottom"></div>
    </v-card>

    <v-card-actions>
      <v-text-field
        class="mt-3"
        v-model="newMsg"
        :disabled="sendingMsg"
        :loading="sendingMsg"
      ></v-text-field>
      <v-btn
        class="success darken-1 ml-3"
        fab
        small
        :disabled="sendingMsg"
        :loading="sendingMsg"
        @click="sendMsg"
      >
        <v-icon small> send </v-icon>
      </v-btn>
    </v-card-actions>
  </v-container>
</template>

<script>
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
    parseTimestamp(timestamp) {
      return dateParser.secondTimestampParser(timestamp);
    },
    isMe(msg) {
      return msg.sender != this.contactInfo.id;
    },
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
              // TODO: FIXME:
              // check if this is necessary
              // this.loadMsg();
              this.scrollToBottom();
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
    scrollToBottom() {
      document.getElementById("chatBoxBottom").scrollIntoView();
    },
    loadMsg() {
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
              this.msgList = [];
              this.$nextTick(() => {
                this.msgList = res.data.currentMessage;
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
    console.log("start chating!", this.contactInfo);
    // 每秒刷新一次
    this.loadMsg();
    this.timer = setInterval(() => {
      this.loadMsg();
    }, 5000);
  },
  mounted() {
    this.scrollToBottom();
  },
  destroyed() {
    clearInterval(this.timer);
  },
  data() {
    return {
      timer: undefined,
      msgList: [],
      sendingMsg: false,
      newMsg: "",
    };
  },
};
</script>