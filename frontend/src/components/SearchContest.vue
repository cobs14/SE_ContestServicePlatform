<template>
  <v-card tile id="SearchContest" class="mx-auto">
    <v-card-actions @click="expand = !expand">
      <v-btn color="blue lighten-2" text @click.stop="expand = true">
        按条件查找竞赛...
      </v-btn>
      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>{{ expand ? "mdi-chevron-up" : "mdi-chevron-down" }}</v-icon>
      </v-btn>
    </v-card-actions>

    <v-expand-transition>
      <div v-show="expand">
        <v-divider></v-divider>
        <v-form class="mx-3">
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field
                class="mr-4"
                prepend-inner-icon="mdi-magnify"
                single-line
                placeholder="输入竞赛名称(可选)"
                persistent-hint
                hint="按名称查找"
                v-model="contestTitle"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                class="mr-4"
                prepend-inner-icon="mdi-magnify"
                single-line
                placeholder="输入竞赛主办方(可选)"
                persistent-hint
                hint="按主办方查找"
                v-model="contestSponsor"
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6">
              <v-combobox
                v-model="selectedContestKeyword"
                :search-input.sync="keywordSearch"
                hide-selected
                prepend-inner-icon="mdi-magnify"
                hint="请输入关键词，最多5个"
                label="输入关键词（可选）"
                single-line
                multiple
                persistent-hint
                small-chips
              >
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>
                        按下 <kbd>enter</kbd> 以添加"<strong
                          >{{ keywordSearch }} </strong
                        >".
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </template>
              </v-combobox>
            </v-col>

            <v-col cols="12" sm="6">
              <v-combobox
                v-model="selectedContestLabel"
                :items="contestLabels"
                :search-input.sync="labelSearch"
                hide-selected
                prepend-inner-icon="mdi-magnify"
                hint="选择或输入竞赛类别，最多5个"
                label="请选择竞赛类别（可选）"
                single-line
                multiple
                persistent-hint
                small-chips
              >
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>
                        没有找到"<strong>{{ labelSearch }}</strong
                        >". 按下 <kbd>enter</kbd> 以添加该类别
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </template>
              </v-combobox>
            </v-col>

            <v-col cols="12" sm="5">
              <v-select
                v-model="selectedContestState"
                :items="contestStates"
                :menu-props="{ maxHeight: '400' }"
                single-line
                hint="竞赛进行的状态"
                persistent-hint
              ></v-select>
            </v-col>
            <v-col cols="12" sm="5">
              <v-select
                v-model="selectedContestGroup"
                :items="contestGroups"
                :menu-props="{ maxHeight: '400' }"
                single-line
                hint="是否允许组队"
                persistent-hint
              ></v-select>
            </v-col>
            <v-spacer></v-spacer>
            <v-col>
              <v-btn class="info darken-1" @click="submit"> 查找 </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
export default {
  name: "SearchContest",
  mixins: [redirect, snackbar, filter],
  computed: {},
  components: {},
  methods: {
    submit() {
      this.expand = false;
      
      this.params["text"] = [];

      this.contestSponsor != "" &&
        (this.params["sponsorId"] = this.contestSponsor);

      this.contestTitle != "" && this.params["text"].push(this.contestTitle);

      this.params["module"] = this.selectedContestLabel.concat();
      this.params["module"] = this.params["module"].map((x) => x.trim());

      this.params["text"].push(...this.selectedContestKeyword);
      this.params["text"] = this.params["text"].map((x) => x.trim());

      this.params["allowGroup"] =
        this.selectedContestGroup == "不限"
          ? "Any"
          : this.selectedContestGroup == "个人"
          ? "False"
          : "True";

      let stateParams = {
        apply: 0,
        contest: 0,
        review: 0,
      };

      this.selectedContestState == ["未开始"] && (stateParams.apply = 1);
      this.selectedContestState == ["报名中"] && (stateParams.apply = 2);
      this.selectedContestState == ["比赛中"] && (stateParams.contest = 2);
      this.selectedContestState == ["评奖中"] && (stateParams.review = 2);
      this.selectedContestState == ["已结束"] && (stateParams.review = 3);

      this.params["state"] = stateParams;

      this.params["detailed"] = false;
      //console.log("pre", stateParams, this.params);
      this.params = this.getContestFilter(this.params);
      console.log("after", this.params);
      this.$emit("update:contestParams", this.params);
      // 0 for 'contest' category
      // true for we need to reset pageNum to 1
      // (since we don't know the count of total pages for now)
      this.$emit("refreshList", 0, true);
    },
  },
  watch: {
    selectedContestLabel(val) {
      if (val.length > 5) {
        this.$nextTick(() => this.selectedContestLabel.pop());
      }
    },
    selectedContestKeyword(val) {
      if (val.length > 5) {
        this.$nextTick(() => this.selectedContestKeyword.pop());
      }
    },
  },
  data() {
    return {
      expand: false,
      params: {},

      contestSponsor: "",
      contestTitle: "",
      selectedContestLabel: [],
      selectedContestKeyword: [],

      selectedContestState: "不限",
      contestStates: ["不限", "未开始", "报名中", "比赛中", "评奖中", "已结束"],

      selectedContestGroup: "不限",
      contestGroups: ["不限", "个人", "团队"],
      contestLabels: ["程序设计", "大数据", "算法", "数学建模"],

      labelSearch: null,
      keywordSearch: null,
    };
  },
};
</script>