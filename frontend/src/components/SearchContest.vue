<template>
  <v-card tile id="SearchContest" class="mx-auto">
    <v-card-actions @click="expand = !expand">
      <v-btn color="orange lighten-2" text @click.stop="expand = true">
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
              <v-btn class="info darken-1" @click="submit">
                查找
              </v-btn>
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
export default {
  name: "SearchContest",
  mixins: [redirect, snackbar],
  computed: {},
  components: {},
  methods: {
    submit() {
      //Step 1. Parse all the things into packet.
      
      this.$emit("update:params", this.params);
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
      params: Object,
      selectedContestState: "不限",
      contestStates: ["不限", "未开始", "报名中", "比赛中", "评奖中", "已结束"],
      contestTitle: "",
      contestSponsor:"",
      selectedContestGroup: "不限",
      contestGroups: ["不限", "个人", "团队"],
      contestLabels: ["程序设计", "大数据", "算法", "数学建模"],
      selectedContestLabel: [],
      selectedContestKeyword: [],
      labelSearch: null,
      keywordSearch: null,
    };
  },
};
</script>