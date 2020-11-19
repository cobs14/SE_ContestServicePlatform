<template>
    <v-card>
    <v-container>
    <v-row>
        <v-card flat style="width: 80%; margin: auto">
        <v-col>
        <v-text-field
        label="用户名"
        v-model="username"
        readonly
        ></v-text-field>
        <v-text-field
        type="password"
        label="密码"
        v-model="password"
        :counter="20"
        :error-messages="passwordErrors"
        @input="$v.password.$touch()"
        @blur="$v.password.$touch()"
        ></v-text-field>
        <v-text-field
        type="password"
        label="再次输入密码"
        v-model="confirmPassword"
        :counter="20"
        :error-messages="confirmErrors"
        @input="$v.confirmPassword.$touch()"
        @blur="$v.confirmPassword.$touch()"
        ></v-text-field>
        </v-col>
        <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
        class="info ma-2"
        @click="resetPassword()"
        :loading="sendingForm"
        :disabled="sendingForm"
        >
        确认修改
        </v-btn>    
        </v-card-actions>
        </v-card>
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
  minLength,
  maxLength,
  sameAs
} from "vuelidate/lib/validators";
export default {
  name: "LoginPasswordStep3",
  mixins: [redirect, snackbar, validationMixin],
  data() {
    return {
      sendingForm: false,
      username: "test change",
      password: "",
      confirmPassword: ""
    };
  },
  computed: {
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !(this.$v.password.minLength && this.$v.password.maxLength) &&
        errors.push("密码长度应该介于6~20个字符");
      !this.$v.password.required && errors.push("请输入密码");
      return errors;
    },
    confirmErrors() {
      const errors = [];
      if (!this.$v.confirmPassword.$dirty) return errors;
      !this.$v.confirmPassword.required && errors.push("请再次输入密码以确认");
      !this.$v.confirmPassword.sameAsPassword &&
        errors.push("两次输入的密码不一致");
      return errors;
    },
  },
  components: {},
  validations: {
    password: {
      required,
      minLength: minLength(6),
      maxLength: maxLength(20),
    },
    confirmPassword: {
      required,
      sameAsPassword: sameAs("password"),
    },
  },
  methods: {
    resetPassword(){
      this.$v.$touch();
      if (this.$v.$invalid) {
        // this.$emit("update:email", "");
        // this.snackbar("请完整填写正确的信息", "error");
        this.sendingForm = false;
      } else {
        // do your submit logic here
        this.sendingForm = true;
        
        // simulating sending forms
        setTimeout(() => {
          this.sendingForm = false;
          // this.$emit("update:email", this.email);
          // this.$router.replace({ path: "/register/emailcheck" });
        }, 1000);
      }
    }
  },
};
</script>