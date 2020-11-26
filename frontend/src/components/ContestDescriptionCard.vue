<template>
<v-card class="ma-2 pa-2">
  <v-container>
    <v-text-field 
      label="详情标题"
      outlined
      v-model="descriptionTitle"
      :counter="64"
      :error-messages="descriptionTitleErrors"
      @input="$v.descriptionTitle.$touch()"
      @blur="$v.descriptionTitle.$touch()"
    >
    </v-text-field>
    <v-textarea 
      label="详情内容"
      outlined
      v-model="descriptionContent"
      :counter="2048"
      :error-messages="descriptionContentErrors"
      @input="$v.descriptionContent.$touch()"
      @blur="$v.descriptionContent.$touch()"
    ></v-textarea>
    <v-row>
      <v-spacer></v-spacer>
      <v-btn class="error ma-2" @click="deleteDescription()">删除</v-btn>
    </v-row>
  </v-container>
</v-card>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { validationMixin } from "vuelidate";
import {
  required,
  maxLength
} from "vuelidate/lib/validators";
export default {
  name: 'DescriptionCard',
  validations:{
    descriptionTitle: {
      required,
      maxLength: maxLength(64)
    },
    descriptionContent:{
      required,
      maxLength: maxLength(2048)
    },
  },
  computed: {
    descriptionTitleErrors() {
      const errors = [];
      if (!this.$v.descriptionTitle.$dirty) return errors;
      !this.$v.descriptionTitle.required && errors.push("请输入详情标题");
      !this.$v.descriptionTitle.maxLength && errors.push("竞赛名称至多64个字符");
      return errors;
    },
    descriptionContentErrors() {
      const errors = [];
      if (!this.$v.descriptionContent.$dirty) return errors;
      !this.$v.descriptionContent.required && errors.push("请输入详情内容");
      !this.$v.descriptionContent.maxLength && errors.push("竞赛简介至多2048个字符");
      return errors;
    },
  },
  watch:{
    descriptionTitle: function(newVal, oldVal){
      this.$emit("content-change", { index:this.index, title:this.descriptionTitle, content:this.descriptionContent})
    },
    descriptionContent: function(newVal, oldVal){
      this.$emit("content-change", { index:this.index, title:this.descriptionTitle, content:this.descriptionContent})
    }
  },
  methods:{
    deleteDescription() {
      this.$emit("delete-description", {index: this.index});
    }
  },
  props:{
    index: Number
  },
  data() {
    return {
      descriptionTitle: "",
      descriptionContent: ""
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
