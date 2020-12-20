<template>
  <v-card tile id="ContestInfoBar" class="mx-auto my-3">
    <v-card-title>
      {{ info.title }}
      <v-chip class="mx-5" small :color="stateColor" label outlined>{{
        contestState[2]
      }}</v-chip>
    </v-card-title>
    <v-card-subtitle>
      由&nbsp;{{ info.sponsorTrueName? info.sponsorTrueName:info.sponsor }}&nbsp;举办，{{ contestState[3] }}
    </v-card-subtitle>
    <v-card-text>
      {{ info.abstract }}
    </v-card-text>
    <v-card-actions>
      <v-btn text class="blue--text" @click="redirect('/contest/' + info.id)">
        查看详情
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import * as dateParser from "@/assets/datetime.js";
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
    this.contestState = dateParser.getStateDescription(this.info.state);
    if (this.contestState[4] < 1) {
      this.stateColor = "grey";
    } else if (this.contestState[4] < 2) {
      this.stateColor = "info";
    } else if (this.contestState[4] < 4) {
      this.stateColor = "success";
    } else {
      this.stateColor = "orange";
    }
    switch (this.info.censorStatus) {
      case "pending":
        this.contestState[2] = "竞赛待审核";
        this.stateColor = "grey";
        break;
      case "reject":
        this.contestState[2] = "审核未通过";
        this.stateColor = "red";
        break;
    }
  },
  data() {
    return {
      contestState: Object,
      stateColor: "grey",
    };
  },
};
</script>