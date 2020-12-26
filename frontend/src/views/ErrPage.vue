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
// 错误页面
import { redirect } from "@/mixins/router.js";
export default {
  name: "ErrPage",
  mixins: [redirect],
  data() {
    return {
      timer: 0,
    };
  },
  created() {
    if (this.timer) clearTimeout(this.timer);
    this.timer = setTimeout(() => {
      this.redirect("/");
    }, 5000);
  },
  beforeDestroy() {
    if (this.timer) clearTimeout(this.timer);
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
