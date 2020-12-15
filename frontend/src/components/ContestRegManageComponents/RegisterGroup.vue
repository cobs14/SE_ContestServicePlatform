<template>
  <v-card>
    <v-card-title>
      报名管理
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-btn class="info ma-2">
      一键通过
    </v-btn>
    <!--FIXME: -->
    <!--v-data-table
      :headers="headers"
      :items="registerList"
      :search="search"
    >
      <template v-slot:item.actions="{ item }">
        <v-icon
          small
          class="mr-2"
        >
          mdi-pencil
        </v-icon>
        <v-icon
          small
        >
          mdi-delete
        </v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn
          color="primary"
          @click="initialize"
        >
          Reset
        </v-btn>
      </template>
    </v-data-table-->

    <v-data-table
      :headers="headers"
      :items="registerList"
      :search="search"
    ></v-data-table>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { requestPost } from "@/network/request.js";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { logState } from "@/mixins/logState.js";

export default {
  components: {},
  name: "RegisterManagerGroup",
  mixins: [redirect, snackbar, logState],
  methods: {},
  props: {
    // FIXME:
    // registerList: Array,
  },
  created() {
    console.log(this.registerList);
  },
  data() {
    return {
      isLoading: true,
      search: '',
      // FIXME: set for test now, need to be replaced later
      registerList: [
        {
          id: 1,
          groupName: "feifei",
          memberCount: 2
        }
      ],
      headers: [
        { text: '报名编号', value: 'id'},
        { text: '队伍名称', value: 'groupName'},
        { text: '队伍人数', value: 'memberCount'},
        { text: '', value: 'actions' }
      ]
    };
  },
};
</script>