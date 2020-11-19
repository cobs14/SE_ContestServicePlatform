<template>
  <v-card tile id="SearchContest" class="mx-auto">
    <v-card-actions>
      <v-btn color="orange lighten-2" text @click="expand = true">
        按条件查找竞赛...
      </v-btn>
      <v-spacer></v-spacer>

      <v-btn icon @click="expand = !expand">
        <v-icon>{{ expand ? "mdi-chevron-up" : "mdi-chevron-down" }}</v-icon>
      </v-btn>
    </v-card-actions>

    <v-expand-transition>
      <div v-show="expand">
        <v-divider></v-divider>
        <v-form class="mx-3">
          <v-row>
            <v-col cols="12" sm="4">
              <v-select
                v-model="selectedContestState"
                :items="contestStates"
                :menu-props="{ maxHeight: '400' }"
                chips
                single-line
                hint="竞赛进行的状态"
                persistent-hint
              ></v-select>
            </v-col>
            <v-col cols="12" sm="4">
              <v-select
                v-model="selectedContestState"
                :items="contestStates"
                :menu-props="{ maxHeight: '400' }"
                chips
                single-line
                hint="竞赛进行的状态"
                persistent-hint
              ></v-select>
            </v-col>
          </v-row>
        </v-form>

        <v-card-text>
          I'm a thing. But, like most politicians, he promised more than he
          could deliver. You won't have time for sleeping, soldier, not with all
          the bed making you'll be doing. Then we'll go with that data file!
          Hey, you add a one and two zeros to that or we walk! You're going to
          do his laundry? I've got to find a way to escape.
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
export default {
  name: "SearchContest",
  mixins: [redirect, snackbar],
  computed: {},
  components: {},
  methods: {
    submit() {
      this.$emit("update:params", this.params);
    },
  },
  data() {
    return {
      expand: false,
      params: Object,

      selectedContestState: "不限",
      contestStates: ["不限", "未开始", "报名中", "比赛中", "评奖中", "已结束"],
    };
  },
};
</script>