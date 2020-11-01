<template>
  <div id="app">
    <v-app>
      <v-header> </v-header>
      <infocard> </infocard>
      <router-view />
      <v-footer> </v-footer>
    </v-app>
  </div>
</template>

<script>
/* eslint-disable */
import vHeader from "@/components/Header.vue";
export default {
  components: {
    vHeader,
  },
  name: "App",
};
</script>


