<template>
  <div id="homepage">
    <v-carousel
      cycle
      height="400"
      hide-delimiter-background
      show-arrows-on-hover
    >
      <v-carousel-item v-for="(slide, i) in slides" :key="i">
        <v-sheet :color="colors[i]" height="100%">
          <v-row class="fill-height" align="center" justify="center">
            <div class="display-3">{{ slide }}</div>
          </v-row>
        </v-sheet>
      </v-carousel-item>
    </v-carousel>
    <v-spacer> </v-spacer>
    <v-container>
      <v-chip class="ma-2" color="pink" label text-color="white">
        <v-icon class="material-icons mr-1">event</v-icon>
        热门赛事
      </v-chip>
      <v-row>
        <v-col v-for="n in 4" :key="n" cols="12" sm="4">
          <infocard> </infocard>
        </v-col>
      </v-row>
    </v-container>

    <v-container>
      <v-chip class="ma-2" color="orange" label text-color="white">
        <v-icon class="material-icons mr-1">menu_book</v-icon>
        精选课程
      </v-chip>
      <v-row>
        <v-col v-for="n in 3" :key="n" cols="12" sm="4">
          <infocard> </infocard>
        </v-col>
      </v-row>
    </v-container>

    <v-container>
      <v-chip class="ma-2" color="blue" label text-color="white">
        <v-icon class="material-icons mr-1">notes</v-icon>
        社区讨论
      </v-chip>
      <v-row>
        <v-col v-for="n in 2" :key="n" cols="12" sm="12">
          <infobar> </infobar>
        </v-col>
      </v-row>
    </v-container>

    <v-container>
      <v-chip class="ma-2" color="green" label text-color="white">
        <v-icon class="material-icons mr-1">call</v-icon>
        联系我们
      </v-chip>
      <v-row>
        <v-col v-for="n in 3" :key="n" cols="12" sm="4">
          <contactus> </contactus>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
/* eslint-disable */
import infocard from "@/components/HomePageCards.vue";
import infobar from "@/components/HomePageBars.vue";
import contactus from "@/components/HomePageContactUs.vue";
export default {
  name: "HomePage",
  components: {
    infocard,
    infobar,
    contactus
  },
  methods:{
    routeTo: function (dir) {
      this.$router.push("/");
      this.$nextTick(() => this.$router.push(dir));
    },
  },
  data() {
    return {
      colors: [
        "indigo",
        "warning",
        "pink darken-2",
        "red lighten-1",
        "deep-purple accent-4",
      ],
      slides: [
        "清华大学第一届编程大赛(假装有图)",
        "我们的赞助商：Contest+",
        "Google Coding Jam",
        "4th slide",
        "5th slide",
      ],
    };
  },
};
</script>