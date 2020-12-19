<template>
  <div class="err_page">
    <v-container>
      <v-main
        :class="[`text-h1`, `font-weight-medium`]"
        class="transition-swing text--grey"
        v-text="`404`"
      >
      </v-main>
      <div
        :class="[`text-h5`]"
        class="transition-swing"
        v-text="`We can't find the page you are looking for,`"
      ></div>
      <div
        :class="[`text-h6`]"
        class="transition-swing"
        v-text="`but we will take you home soon.`"
      ></div>
    </v-container>
  </div>
</template>

<script>
import { redirect } from "@/mixins/router.js";
export default {
  name: "ErrPage",
  mixins: [redirect],
  created() {
    setTimeout(() => {
      this.redirect("/");
    }, 5000);
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
