<template>
    <v-card
      class="mx-auto my-2"
      color="white"
      width="100%"
    >
      <v-card-title>
        <v-chip
        class="ma-2"
        label
      >
        #1
      </v-chip>
        第一届华大学编程竞赛
      </v-card-title>
      <v-card-subtitle>
        校赛
      </v-card-subtitle>
      <v-card-text
        class="pt-3"
        style="position: relative;"
      >
      程序员的第一个编程校赛
      </v-card-text>
      <v-card-actions>
        <!--v-btn
          color="deep-purple lighten-2"
          text
        >
        修改
        </v-btn-->
        <v-btn
          color="deep-purple lighten-2"
          href="/manage/contest/1"
          text

        >
        竞赛管理
        </v-btn>
      </v-card-actions>
    </v-card>
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
