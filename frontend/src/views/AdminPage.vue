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
       <v-expansion-panel
        v-for="info in contestInfo"
        :key="info.name"
       >
        <v-expansion-panel-header>
          <v-row no-gutters>
            <v-col cols="4">
              TODO:{{info.name}}
            </v-col>
            <v-col
              cols="8"
              class="text--secondary"
            >
            <span>
              TODO:{{info.sponsor}}
            </span>
            </v-col>
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-row no-gutters>
            <v-col cols="8">
              <v-container>
                竞赛简介：
                <br/>
                {{info.abstract}}
              </v-container>
            </v-col>  
            <v-col cols="4">
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
    <v-row>
      <v-dialog
        v-model="invitationDialog"
        persistent
        max-width="290"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-col>
            <v-text-field 
              label="邀请码数"
              outlined
              type="number"
              v-model="invitationNumber"
            >
            </v-text-field>
          </v-col>
          <v-btn
            class="mt-5"
            color="primary"
            dark
            v-bind="attrs"
            v-on="on"
          >
            生成主办方邀请码
          </v-btn>
        </template>
        <v-card>
          <v-card-title class="headline">
            下面是可用的主办方邀请码
          </v-card-title>
          <v-card-text> 
            <v-container
              v-for="code in invitationCodes"
              :key="code"
            >
              {{code}}
              <br/>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="green darken-1"
              text
              @click="invitationDialog = false"
            >
              完成
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-spacer></v-spacer>
    </v-row>
    <v-simple-table>
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">
              邀请码
            </th>
            <th class="text-left">
              主办方用户名
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="info in sponsorInfo"
            :key="info.code"
          >
            <td>{{ info.code }}</td>
            <td>{{ info.sponsor }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
    <v-pagination
        v-model="pageNum"
        :length="15"
        :total-visible="7"
      ></v-pagination>
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
    getInvitationCode(){
      // TODO: call get invitation code
      this.invitationCodes = [
        "19883", "21231", "24562", "89546", "20145"
      ]
    }
  },
  data () {
    return {
      page: 'contest',
      tab: '',
      invitationDialog: false,
      invitationNumber: 1,
      invitationCodes: ["19883", "21231", "24562", "89546", "20145"],
      pageNum: 1, 
      navigation: [
        { icon: 'playlist_add_check', title: '竞赛创建审核', page: 'contest'},
        { icon: 'how_to_reg', title: '竞赛发布者管理', page: 'sponsor' },
        { icon: 'portrait', title: '用户人工验证', page: 'user' },
      ],
      // TODO: change info
      contestInfo:[
        {
        name: '竞赛名称文本',
        sponsor: '竞赛主办方',
        abstract: '竞赛简介内容文本竞赛简介内容文本竞赛简介内容文本竞赛简介内容文本竞赛简介内容文本竞赛简介内容文本竞赛简介内容文本竞赛简介内容文本竞赛简介内容文本竞赛简介内容文本'
        },
      ],
      // TODO: change sponsor info
      sponsorInfo:[
        {
          code: 123123,
          sponsor: "主办方"
        }
      ]
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
  "sponsor": "竞赛发布者管理",
  "user": "用户人工验证",
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
