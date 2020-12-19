<template>
  <v-card tile id="SearchUser" class="mx-auto">
    <v-card-actions @click="expand = !expand">
      <v-btn color="green darken-1" text @click.stop="expand = true">
        按条件查找用户...
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
                placeholder="输入要查找的用户名(可选)"
                persistent-hint
                hint="按用户名查找"
                v-model="params.username"
                @change="update"
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field
                class="mr-4"
                prepend-inner-icon="mdi-magnify"
                single-line
                placeholder="输入要查找的院校(可选)"
                persistent-hint
                hint="按院校查找"
                v-model="params.school"
                @change="update"
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field
                class="mr-4"
                prepend-inner-icon="mdi-magnify"
                single-line
                placeholder="输入要查找的专业(可选)"
                persistent-hint
                hint="按专业查找"
                v-model="params.major"
                @change="update"
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field
                class="mr-4"
                prepend-inner-icon="mdi-magnify"
                single-line
                placeholder="输入要查找的学生号(可选)"
                persistent-hint
                hint="按学生号查找"
                v-model="params.studentNumber"
                @change="update"
              ></v-text-field>
            </v-col>

            <v-spacer></v-spacer>
            <v-col>
              <v-spacer></v-spacer>
              <v-btn class="success darken-1" @click="submit"> 查找 </v-btn>
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
import { logState } from "@/mixins/logState.js";
import { snackbar } from "@/mixins/message.js";
import { filter } from "@/mixins/filter.js";
export default {
  name: "SearchUser",
  mixins: [redirect, snackbar, filter, logState],
  computed: {},
  components: {},
  methods: {
    update() {
      this.params = this.getUserFilter(this.params);
      console.log("after, user search", this.params);
      this.$emit("update:userParams", this.params);
      // 1 for 'user' category
      // true for we need to reset pageNum to 1
      // (since we don't know the count of total pages for now)
      this.$emit("refreshList", 1, true);
    },
    submit() {
      this.expand = false;
      this.update();
    },
  },
  data() {
    return {
      expand: false,
      params: Object,
    };
  },
};
</script>