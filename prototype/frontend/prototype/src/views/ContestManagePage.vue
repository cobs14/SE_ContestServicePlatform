<template>
  <div id="ContestManagePage" style="display: flex">
      <aside>
        <v-card height="1200"
                max-width="300"
                :dark="true"
        >
          <v-navigation-drawer permanent width="100%">
            <v-list-item>
              <v-list-item-content>
                <v-btn href="/manage/contest_list" class="ma-1"> 
                  返回
                </v-btn>
                <v-list-item-title class="title" style="text-align: center">
                  第一届华大学编程竞赛
                </v-list-item-title>
                <v-list-item-subtitle style="text-align: center">
                  校赛
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
        <v-container v-if="type === 'setting'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
          <contestedit></contestedit>
        </v-container>
        <v-container v-if="type === 'register'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
          <v-data-table
            :headers="regHeaders"
            :items="templateData"
            item-key="name"
            class="elevation-1"
          >
          </v-data-table>
        </v-container>
        <v-container v-if="type === 'news'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
          
        </v-container>
        <v-container v-if="type === 'score'" style="margin: 10px; background: white; width: auto; height: 85%; border-radius: 4px">
          <v-data-table
            :headers="scoreHeaders"
            :items="templateData"
            item-key="name"
            class="elevation-1"
          >
          </v-data-table>
        </v-container>
      </div>
      
  </div>
</template>

<script>
/* eslint-disable */
import contestedit from "@/components/ContestCreatePage.vue";
export default {
  name: 'ContestManagePage',
  components:{
    contestedit
  },
  data () {
    return {
      type: this.$route.params.type || 'setting',
      tab: '',
      year: 0,
      select: '',
      items: [
        { icon: 'settings', title: '竞赛设置', href: '/manage/contest/1/setting' },
        { icon: 'people', title: '报名管理', href: '/manage/contest/1/register' },
        { icon: 'speaker_notes', title: '动态发布', href: '/manage/contest/1/news'},
        { icon: 'grading', title: '评分与奖项', href: '/manage/contest/1/score' },
      ],
      paths:[
        { text: '竞赛管理', disabled: false},
        { text: '竞赛列表', disabled: true}
      ]
    }
  },
  computed:{
      regHeaders(){
        return[
          {
            text: '序号',
            value: 'id'
          },
          {
            text: '参赛名称',
            value: 'name'
          },
          {
            text: '团队状态',
            value: 'status'
          },
          {
            text: '操作',
            value: 'op'
          }
        ]
      },
      scoreHeaders(){
        return[
          {
            text: '序号',
            value: 'id'
          },
          {
            text: '参赛名称',
            value: 'name'
          },
          {
            text: '提交作品',
            value: 'work'
          },
          {
            text: '最终评分',
            value: 'score'
          },
          {
            text: '奖项',
            value: 'mark'
          }
        ]
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
