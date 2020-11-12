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
import { redirect } from "@/mixins/router.js";
import vHeader from "@/components/Header.vue";
export default {
  mixins: [redirect],
  components: {
    vHeader,
  },
  name: "App",
};
</script>
