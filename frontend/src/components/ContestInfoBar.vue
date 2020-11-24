<template>
  <v-card tile id="ContestInfoBar" class="mx-auto my-3">
    <v-card-title>
      {{ info.title }}
    </v-card-title>
    <v-card-subtitle> {{getState}}，由&nbsp;{{ info.sponsor }}&nbsp;举办 </v-card-subtitle>
    <v-card-text>
      {{ info.abstract }}
    </v-card-text>
    <v-card-actions>
      <v-btn text class="blue--text" @click="redirect('/contest/' + info.id)"> 查看详情 </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
export default {
  name: "ContestInfoBar",
  mixins: [redirect, snackbar],
  computed:{
    getState(){
      return 'TODO: HERE->日期处理'
    }
  },
  methods: {
    submit() {},
  },
  props: {
    info: Object,
  },
  created() {
    console.log(this.info);
  },
  data() {
    return {};
  },
};
</script>