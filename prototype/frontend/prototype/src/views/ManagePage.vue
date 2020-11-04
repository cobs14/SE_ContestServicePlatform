<template>
  <div id="ManagePage" style="display: flex">
      <aside>
        <v-card height="1200"
                width="280"
                :dark="true"
        >
          <v-navigation-drawer permanent width="100%">
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title class="title" style="text-align: center">
                  竞赛管理页面
                </v-list-item-title>
                <v-list-item-subtitle style="text-align: center">
                  Manage
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <v-list
              dense
              nav
            >
              <v-list-item
                v-for="item in items"
                :key="item.title"
                :link=true
                :href="item.href"
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
      <div class="main" style="display: block; width: 100%; height: 100%; background: #DDDDDD">
        <div style="margin: 0; background: white; width: 100%; height: 80px">
          <v-breadcrumbs :items="paths" divider="-"></v-breadcrumbs>
        </div>
        <v-container v-if="type === 'contest_list'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
          <v-tabs v-model="tab">
            <v-tab>进行中</v-tab>
            <v-tab>历史</v-tab>
          </v-tabs>
          <infocard></infocard>
        </v-container>
        <v-container v-if="type === 'resource'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
          <v-tabs>
            <v-tab>课程</v-tab>
            <v-tab>图书</v-tab>
            <v-tab>题库</v-tab>
          </v-tabs>
          <infocard></infocard>
          <infocard></infocard>
        </v-container>
        <v-container v-if="type === 'finance'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
          <v-card
            class="mx-auto text-center"
            color="purple lighten-2"
            dark
            max-width="900"
          >
            <v-card-text>
              <v-sheet color="rgba(0, 0, 0, .12)">
                <v-sparkline
                  :value="value"
                  color="rgba(255, 255, 255, .7)"
                  height="100"
                  padding="24"
                  stroke-linecap="round"
                  smooth
                >
                  <template v-slot:label="item">
                    ${{ item.value }}
                  </template>
                </v-sparkline>
              </v-sheet>
            </v-card-text>
        
            <v-card-text>
              <div class="display-1 font-weight-thin">
                Sales Last 24h
              </div>
            </v-card-text>
        
            <v-divider></v-divider>
        
            <v-card-actions class="justify-center">
              <v-btn
                block
                text
              >
                Go to Report
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-container>
        <v-container v-if="type === 'certificate'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
        
        <v-data-table
        :headers="templateHeaders"
        :items="templateData"
        item-key="name"
        class="elevation-1"
      >
      <!--:search="search"
        <:custom-filter="filterOnlyCapsText"-->
        <template v-slot:top>
          <v-row align="center">
            <v-col
              class="d-flex"
              cols="12"
              sm="6"
            >
              <v-select
              :items="years"
              v-model="year"
              label="竞赛年份"
              class="mx-auto px-12"
              ></v-select>
            </v-col>
      
            <v-col
              class="d-flex"
              cols="12"
              sm="6"
            >
            <v-text-field
                v-model="search"
                label="Search"
                class="mx-4"
              ></v-text-field>
            </v-col>
          </v-row>  
        </template>
        <template v-slot:item.op="{ item }">
            <v-btn>设置模板</v-btn>
            <v-btn>下载证书</v-btn>

        </template>
      </v-data-table>
        </v-container>
      </div>
      
  </div>
</template>

<script>
import infocard from "@/components/ManagePageCard.vue";
export default {
  name: 'ManagePage',
  components:{
    infocard
  },
  data () {
    return {
      type: this.$route.params.type || 'contest_list',
      tab: '',
      year: 0,
      items: [
        { icon: 'list', title: '竞赛列表', href: '/manage/contest_list' },
        { icon: 'source', title: '资源管理', href: '/manage/resource' },
        { icon: 'attach_money', title: '财务管理', href: '/manage/finance' },
        { icon: 'card_membership', title: '证书管理', href: '/manage/certificate' },
      ],
      paths:[
        { text: '竞赛管理', disabled: false},
        { text: '竞赛列表', disabled: true}
      ],
      value:[
        678,123,345,789,890,456,234,567
      ],
      years:[
        2016,2017,2018,2019,2020,2021,2022
      ],
      templateData:[
        {
          id: 1,
          year: 2021,
          name: '第一届华大学编程竞赛',
          status: '未设置',
          result: '未提交审核',
        }
        
      ]
    }
  },
  computed:{
    templateHeaders(){
      return [
        {
          text: '序号',
          value: 'id'
        },
        {
          text: '年份',
          value: 'year'
        },
        {
          text: '竞赛名称',
          value: 'name'
        },
        {
          text: '状态',
          value: 'status'
        },
        {
          text: '审核结果',
          value: 'result'
        },
        {
          text: '操作',
          value: 'op'
        }  
      ]
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
