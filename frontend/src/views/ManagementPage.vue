<template>
  <div id="ManagePage" style="display: flex">
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
      <!--
        <v-breadcrumbs :items="paths" divider="-"></v-breadcrumbs>
        -->
    </div>
    <v-container v-if="page === 'create'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
      <contest-create
      v-on:goto-list="page = 'list'"
      @showSnackbar="snackbar"
      ></contest-create>
      
    </v-container>
    <v-container v-if="page === 'list'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
        <v-tabs v-model="tab">
        <v-tab>进行中</v-tab>
        <v-tab>历史</v-tab>
        </v-tabs>
    </v-container>
    <v-container v-if="page === 'resource'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
    </v-container>
    <v-container v-if="page === 'finance'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
      
    </v-container>
    <v-container v-if="page === 'certificate'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
    </v-container>
    </div>
  </div>
</template>

<script>
import { snackbar } from "@/mixins/message.js";
import ContestCreate from "@/components/ContestCreate.vue"
// import DescriptionCard from "@/components/ContestDescriptionCard.vue"
export default {
  name: 'ManagementPage',
  mixins: [snackbar],
  components:{
    ContestCreate,
    // DescriptionCard
  },
  methods:{

  },
  data () {
    return {
      page: 'list',
      tab: '',
      navigation: [
        { icon: 'add', title: '创建竞赛', page: 'create'},
        { icon: 'list', title: '竞赛管理', page: 'list' },
        { icon: 'source', title: '资源管理', page: 'resource' },
        { icon: 'attach_money', title: '财务管理', page: 'finance' },
        { icon: 'card_membership', title: '证书管理', page: 'certificate' },
      ],
    }
  },
  computed:{
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
