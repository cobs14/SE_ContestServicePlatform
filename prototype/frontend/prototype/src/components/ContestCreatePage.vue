<template>
  <div id="Register">
    <v-container>
      <v-row>
        <v-spacer> </v-spacer>
          <v-divider> </v-divider>
          <v-container>
            <v-card flat style="width: 100%">
              <v-col>
                <v-text-field label="竞赛名称" required></v-text-field>
                <v-textarea label="竞赛简介"></v-textarea>
                <v-row>
                  <v-col>
                    <v-select
                      :items="teamSelect"
                      :rules="[v => !!v || 'Item is required']"
                      label="参赛方式"
                      required
                    ></v-select>
                  </v-col>
                  <v-col>
                    <v-select
                      :items="typeSelect"
                      :rules="[v => !!v || 'Item is required']"
                      label="竞赛方式"
                      required
                    ></v-select>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col
                    v-for="(select, index) in timeSelect" :key="index"
                    cols="12"
                    sm="6"
                    md="6"
                  >
                    <v-menu
                      ref="menu"
                      v-model="menu[index]"
                      :close-on-content-click="true"
                      :return-value.sync="date"
                      transition="scale-transition"
                      offset-y
                      min-width="290px"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          v-model = date[index]
                          :label= select.text
                          prepend-icon="event"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                        ></v-text-field>
                      </template>
                      <v-date-picker
                        v-model = date[index]
                        no-title
                        scrollable
                      >
                        <v-spacer></v-spacer>
                      </v-date-picker>
                    </v-menu>
                  </v-col>
                </v-row>
                <v-row>
                  <v-spacer></v-spacer>
                  <v-btn class="info ma-1"> 确认 </v-btn>
                  <v-btn class="warning ma-1"> 重置 </v-btn>
                </v-row>
              </v-col>
            </v-card>
          </v-container>
        <v-spacer> </v-spacer>
      </v-row>
    </v-container>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: 'ContestCreate',
  data() {
    return {
      date: [],
      menu: [],
      // dateModel: [],
      teamSelect:[
        '个人赛', '团体赛'
      ],
      typeSelect:[
        '线上竞赛', '线下竞赛'
      ],
      timeSelect:[
        {
          text: '开始报名时间'
        },
        {
          text: '开始提交时间'
        },
        {
          text: '竞赛截止时间'
        },
        {
          text: '成绩发布时间'
        }
      ]
    };
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
