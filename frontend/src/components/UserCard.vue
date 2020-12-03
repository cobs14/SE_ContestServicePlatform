<template>
<v-card class="ma-2 pa-2">
  <v-avatar>
        <img
          src="https://cdn.vuetifyjs.com/images/john.jpg"
          alt="John"
        >
  </v-avatar>
  <v-card-title>
    陆景和
  </v-card-title>
  <v-card-subtitle>
    清华大学软件学院大三
  </v-card-subtitle>
</v-card>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
export default {
  name: 'UserCard',
  computed: {
  
  },
  watch:{

  },
  methods:{
    
  },
  props:{

  },
  data() {
    return {
      
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
