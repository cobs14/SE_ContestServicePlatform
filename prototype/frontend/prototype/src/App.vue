<template>
  <div id="app">
    <v-app>
      <v-header> </v-header>
      <v-main>
        <router-view />
      </v-main>
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


