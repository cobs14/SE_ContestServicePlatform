<template>
  <v-hover v-slot="{ hover }">
    <v-card
      class="mx-auto"
      color="grey lighten-4"
      max-width="600"
      @click="redirect('/contest/' + contest.id)"
    >
    <!--TODO: FIX FETCH IMAGE-->
      <v-img
        :aspect-ratio="16/9"
        src="https://cdn.vuetifyjs.com/images/cards/kitchen.png"
      >
        <v-expand-transition>
          <div
            v-if="hover"
            class="d-flex transition-fast-in-fast-out blue darken-2 v-card--reveal white--text"
            style="height: 60%;"
          >
            {{contest.abstract}}
          </div>
        </v-expand-transition>
      </v-img>
      <v-card-title class="display-1 font-weight-light blue--text mb-2">
        {{contest.title}}
      </v-card-title>
      <v-card-text
        class="pt-6"
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
    contest: Object
  },
  methods: {
    
  },
  created(){
    console.log(this.contest);
  }
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