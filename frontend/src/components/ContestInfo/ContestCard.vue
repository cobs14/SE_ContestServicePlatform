<template>
  <v-hover v-slot="{ hover }">
    <v-card
      class="mx-auto"
      color="grey lighten-4"
      max-width="600"
      @click="redirect('/contest/' + contest.id)"
    >
      <v-img
        :aspect-ratio="16/9"
        :src="contest.imgUrl"
      >
        <v-expand-transition>
          <div
            v-if="hover"
            :class="hoverColorStr"
            style="height: 60%;"
          >
            {{sliceAbstract(contest.abstract)}}
          </div>
        </v-expand-transition>
      </v-img>
      <v-card-title class="font-weight-light blue--text mb-2">
        {{contest.title}}
      </v-card-title>
      <v-card-text
        style="position: relative;"
      >
      主办方：{{contest.sponsorTrueName ? contest.sponsorTrueName : contest.sponsor}}
      </v-card-text>
    </v-card>
  </v-hover>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
export default {
  name: 'infocard',
  mixins: [redirect],
  props:{
    contest: Object,
    hoverColor: String
  },
  methods: {
    sliceAbstract(str){
      return str.length > 30 ? str.slice(0,30) + '...' : str;
    }
  },
  data(){
    return{
      hoverColorStr: "d-flex transition-fast-in-fast-out v-card--reveal white--text " + this.hoverColor
    }
  },
}
</script>

<style scoped>
.v-card--reveal {
  align-items: center;
  bottom: 0;
  justify-content: center;
  opacity: .85;
  position: absolute;
  width: 100%;
}
</style>