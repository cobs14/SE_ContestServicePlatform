<template>
  <div id="app">
    <v-app>
      <v-header> </v-header>
      <v-snackbar
        top
        v-model="snackbar.show"
        :timeout="3000"
        :color="snackbar.color"
      >
        {{ snackbar.message }}
        <template v-slot:action="{ attrs }">
          <v-btn dark text v-bind="attrs" @click="snackbar.show = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
      <v-main>
        <router-view @showSnackbar="showSnackbar" />
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
  data() {
    return {
      snackbar: { show: false, color: "success", message: "" },
    };
  },
  methods: {
    showSnackbar: function (arg) {
      //console.log(arg.message, arg.color);
      this.snackbar.message = arg.message;
      this.snackbar.color = arg.color;
      this.snackbar.show = true;
    },
  },
};
</script>
