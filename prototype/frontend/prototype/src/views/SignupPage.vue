<template>
  <div id="Signup">
    <v-container>
      <v-row>
        <v-spacer> </v-spacer>
        <v-card style="width: 70%; margin-top: 5%; min-height: 700px">
          <v-card-title class="font-weight-black" style="font-size: 1.6em">
            第一步：填写报名信息
          </v-card-title>
          <v-card-subtitle class="font-weight-black">
            正在报名：全国大学生算法竞赛
          </v-card-subtitle>
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
                          >由浙江省教育厅发布</v-list-item-subtitle
                        >
                        <v-list-item-title>报名须知</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </template>

                  <v-divider></v-divider>
                  <v-list-item-subtitle>
                    {{
                      item.content == 0
                        ? "严禁作弊。单人报名采用独立赛制"
                        : "严禁作弊，团队中不超过4个成员。"
                    }}
                  </v-list-item-subtitle>
                </v-navigation-drawer>
                <v-card flat style="width: 70%">
                  <v-col>
                    <v-text-field
                      label="赛区"
                      placeholder="华清小学"
                    ></v-text-field>
                    <v-text-field
                      label="编程语言"
                      placeholder="C--"
                    ></v-text-field>
                    <v-text-field
                      label="报名费"
                      placeholder="免费"
                      readonly
                    ></v-text-field>
                    <v-text-field
                      label="在校身份验证"
                      placeholder="已通过验证：在校本科生"
                      readonly
                    ></v-text-field>
                    <v-text-field
                      v-if="item.content == 1"
                      label="团队名称"
                    ></v-text-field>
                    <v-text-field
                      v-if="item.content == 1"
                      label="队友1用户名"
                    ></v-text-field>
                    <v-text-field
                      v-if="item.content == 1"
                      label="队友2用户名(可选)"
                    ></v-text-field>
                    <v-text-field
                      v-if="item.content == 1"
                      label="队友3用户名(可选)"
                    ></v-text-field>
                    <v-text-field
                      v-if="item.content == 1"
                      label="指导教师(可选)"
                    ></v-text-field>
                    <v-spacer> </v-spacer>
                    <v-btn class="info" @click="routeTo('/contest/signup')"> 报名 </v-btn>
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
  name: "Signup",
  components: {
    infocard,
  },
  methods:{
    routeTo: function (dir) {
      this.$router.push("/");
      this.$nextTick(() => this.$router.push(dir));
    },
  },
  data() {
    return {
      tab: null,
      items: [
        { tab: "单人报名", content: 0 },
        { tab: "团队报名", content: 1 },
      ],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
