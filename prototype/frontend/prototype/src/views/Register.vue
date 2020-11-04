<template>
  <div id="Register">
    <v-container>
      <v-row>
        <v-spacer> </v-spacer>
        <v-card style="width: 70%; margin-top: 5%; height: 700px">
          <v-card-title class="font-weight-black" style="font-size: 1.6em">
            注册新用户
          </v-card-title>
          <v-tabs v-model="tab">
            <v-tab v-for="item in items" :key="item.tab">
              {{ item.tab }}
            </v-tab>
          </v-tabs>
          <v-divider> </v-divider>
          <v-tabs-items v-model="tab">
            <v-tab-item v-for="item in items" :key="item.tab">
              <v-container>
                <v-navigation-drawer
                  absolute
                  permanent
                  right
                  style="width: 30%"
                >
                  <template v-slot:prepend>
                    <v-list-item two-line>
                      <v-list-item-avatar>
                        <img
                          src="https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=3096801686,872084145&fm=26&gp=0.jpg"
                        />
                      </v-list-item-avatar>

                      <v-list-item-content>
                        <v-list-item-subtitle
                          >以{{
                            item.content == 0 ? "学生" : "组织者"
                          }}身份加入我们</v-list-item-subtitle
                        >
                        <v-list-item-title>欢迎加入Contest+!</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </template>

                  <v-divider></v-divider>
                  <v-list-item-subtitle>
                    {{
                      item.content == 0
                        ? "学生具有很多优势，比如ABC"
                        : "组织者使用Contest+有123的好处。"
                    }}
                  </v-list-item-subtitle>
                </v-navigation-drawer>
                <v-card flat style="width: 70%">
                  <v-col>
                    <v-text-field label="用户名"></v-text-field>
                    <v-text-field label="密码"></v-text-field>
                    <v-text-field label="确认密码"></v-text-field>
                    <v-text-field label="手机号/邮箱"></v-text-field>
                    <v-text-field label="接收到的验证码"></v-text-field>
                    <v-text-field
                      v-if="item.content == 0"
                      label="学信网验证码"
                    ></v-text-field>
                    <v-spacer> </v-spacer>
                    <v-row>
                      <v-btn class="info"> 注册 </v-btn>
                      <v-spacer> </v-spacer>
                      <v-btn class="warning"> 获取验证码 </v-btn>
                    </v-row>
                  </v-col>
                </v-card>
              </v-container>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
        <v-spacer> </v-spacer>
      </v-row>
    </v-container>
  </div>
</template>

<script>
/* eslint-disable */
import infocard from "@/components/ManagePageCard.vue";
export default {
  name: "Register",
  components: {
    infocard,
  },
  data() {
    return {
      tab: null,
      items: [
        { tab: "我是学生", content: 0 },
        { tab: "我是发布者", content: 1 },
      ],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
