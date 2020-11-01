<template>
  <v-hover v-slot="{ hover }">
    <v-card
      class="mx-auto"
      color="grey lighten-4"
      max-width="600"
    >
      <v-img
        :aspect-ratio="16/9"
        src="https://cdn.vuetifyjs.com/images/cards/kitchen.png"
      >
        <v-expand-transition>
          <div
            v-if="hover"
            class="d-flex transition-fast-in-fast-out orange darken-2 v-card--reveal white--text"
            style="height: 60%;"
          >
            由浙江省教育厅主办，旨在教大家如何做饭。
          </div>
        </v-expand-transition>
      </v-img>
      <v-card-text
        class="pt-6"
        style="position: relative;"
      >
        <v-btn
          absolute
          color="orange"
          class="white--text "
          fab
          large
          right
          top
        >
          <v-icon>arrow_forward</v-icon>
        </v-btn>
        <div class="font-weight-light grey--text title mb-2">
          正在报名：团队竞赛
        </div>
        <h3 class="display-1 font-weight-light orange--text mb-2">
          烹饪的艺术
        </h3>
        <div class="font-weight-light title mb-2">
          浙江省教育厅 <br>
          报名截止于2020年12月7日
        </div>
      </v-card-text>
    </v-card>
  </v-hover>
</template>

<script>
export default {
  name: 'infocard'
}

</script>

<style scoped>
.v-card--reveal {
  align-items: center;
  bottom: 0;
  justify-content: center;
  opacity: .85;
  position: absolute;
  width: 100%;
}
</style>
