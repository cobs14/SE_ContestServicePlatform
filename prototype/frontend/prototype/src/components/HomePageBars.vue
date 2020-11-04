<template>
  <v-card class="mx-auto" color="blue darken-2" dark >
    <v-card-title>
      <span class="title font-weight-light">课程讨论区</span>
    </v-card-title>

    <v-card-text class="headline font-weight-bold">
      "有无同学知道高数课程配套讲义的快递什么时候送到？我都等一个星期了。"
    </v-card-text>

    <v-card-actions>
      <v-list-item class="grow">
        <v-list-item-avatar color="grey darken-3">
          <v-img
            class="elevation-6"
            alt=""
            src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
          ></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>Evan You 于 2分钟前</v-list-item-title>
        </v-list-item-content>

        <v-row align="center" justify="end">
          <v-icon class="mr-1 material-icons"> favorite </v-icon>
          <span class="subheading mr-2">256</span>
          <span class="mr-1">·</span>
          <v-icon class="mr-1 material-icons"> share-variant </v-icon>
          <span class="subheading">45</span>
        </v-row>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script>
/* eslint-disable */
export default {
  name: "infobar",
  data: () => ({
    //
  }),
};
</script>
