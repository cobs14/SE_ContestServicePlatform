<template>
  <div id="AdminPage" style="display: flex">
    <aside>
    <v-card height="100%"
            min-height="1200"
            max-width="360"
            :dark="true"
    >
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
    <div class="main" style="display: block; width: 100%; height: 100%; background: #DDDDDD">
    <div style="margin: 0; background: white; width: 100%; height: 80px">
      <v-breadcrumbs :items="paths" divider="-"></v-breadcrumbs>
    </div>
    <v-container v-if="page === 'contest'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
      <v-expansion-panels>
       <v-expansion-panel>
        <v-expansion-panel-header>
          <v-row no-gutters>
            <v-col cols="4">
              TODO:竞赛名称
            </v-col>
            <v-col
              cols="8"
              class="text--secondary"
            >
            <span>
              TODO:竞赛主办方
            </span>
            </v-col>
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-row no-gutters>
            <v-col cols="8">
              <v-form>
                <v-select
                  v-model="contestModules"
                  chips
                  label="竞赛模块"
                  multiple
                  outlined
                >
                </v-select>
                <v-textarea 
                  label="竞赛简介"
                  outlined
                  v-model="contestAbstract"
                ></v-textarea>
              </v-form>
            </v-col>  
            <v-col cols="3">
              <v-text-field 
                label="填写审核意见"
                outlined
                :counter="64"
              >
              </v-text-field>
            </v-col>
          </v-row>
  
          <v-card-actions>
            <v-btn
              class="info"
              @click="redirect('/contest/1')"
            >
              TODO: 导向特定contest
              <br/>
              查看预览
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              class="error"
            >
              拒绝
            </v-btn>
            <v-btn
              class="success"
            >
              审核通过
            </v-btn>
          </v-card-actions>
        </v-expansion-panel-content>
      </v-expansion-panel>
      </v-expansion-panels>
    
    
    
    </v-container>
    <v-container v-if="page === 'sponsor'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
        <v-tabs v-model="tab">
        <v-tab>进行中</v-tab>
        <v-tab>历史</v-tab>
        </v-tabs>
    </v-container>
    <v-container v-if="page === 'user'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
    </v-container>
    </div>
  </div>
</template>

<script>
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
export default {
  name: 'ManagementPage',
  mixins: [redirect, snackbar],
  components:{
  },
  methods:{

  },
  data () {
    return {
      page: 'contest',
      tab: '',
      navigation: [
        { icon: 'playlist_add_check', title: '竞赛创建审核', page: 'contest'},
        { icon: 'how_to_reg', title: '举办者身份申请', page: 'sponsor' },
        { icon: 'portrait', title: '用户人工验证', page: 'user' },
      ],
    }
  },
  computed:{
    paths() {
      return [
        {
          text: '平台管理',
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
  "contest": "竞赛创建审核",
  "sponsor": "举办者身份申请",
  "user": "用户人工验证",
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
