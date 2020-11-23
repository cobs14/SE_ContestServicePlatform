<template>
  <v-card tile id="ContestInfoBar" class="mx-auto my-3">
    <v-card-title>
      {{ info.title }}
    </v-card-title>
    <v-card-text>
        {{info.abstract}}
    </v-card-text>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
export default {
  name: "ContestInfoBar",
  mixins: [redirect, snackbar],
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