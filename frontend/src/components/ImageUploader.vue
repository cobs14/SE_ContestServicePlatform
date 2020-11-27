<template>
  <div>
    <v-form id="pictureForm">
      <v-file-input
        v-model="selectedPicture"
        :rules="pictureRules"
        required
        show-size
        accept="image/*"
        placeholder="点击此处选择要上传的图片"
        label="竞赛背景图"
        prepend-icon="mdi-camera"
      >
      </v-file-input>
    </v-form>
    <v-img :src="imgUrl"> </v-img>
  </div>
</template>

<script>
export default {
  data: () => ({
    pictureRules: [
      (img) => !!img || "您不能上传空文件",
      (img) => img.size < 5000000 || "您上传的图片大小最多为5MB.",
    ],
    selectedPicture: "",
    imgUrl: "",
  }),
};
</script>

<style scoped>
</style>