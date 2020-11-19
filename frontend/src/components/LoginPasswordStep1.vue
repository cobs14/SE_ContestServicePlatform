<template>
    <v-container>
    <v-row>
    <v-card flat style="width: 80%; margin: auto">
        <v-col>
        <v-text-field
        label="请输入绑定的电子邮箱地址"
        v-model="email"
        :error-messages="emailErrors"
        @input="$v.email.$touch()"
        @blur="$v.email.$touch()"
        ></v-text-field>
        </v-col>
        <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                class="info ma-2"
                @click="submit()"
                :loading="sendingForm"
                :disabled="sendingForm"
                >
                确认
                </v-btn>    
        </v-card-actions>
    </v-card>
    </v-row>
    </v-container>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { validationMixin } from "vuelidate";
import {
  required,
  email,
} from "vuelidate/lib/validators";
export default {
  name: "LoginPasswordStep1",
  mixins: [redirect, snackbar, validationMixin],
  data() {
    return {
      sendingForm: false,
      passstep: 1,
      email: ""
    };
  },
  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("输入的邮箱地址无效");
      !this.$v.email.required && errors.push("请输入邮箱地址");
      return errors;
    },
  },
  components: {},
  validations: {
    email: { required, email },
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        // this.$emit("update:email", "");
        this.snackbar("请完整填写正确的信息", "error");
        this.sendingForm = false;
      } else {
        // do your submit logic here
        this.sendingForm = true;
        // simulating sending forms
        setTimeout(() => {
          this.sendingForm = false;
          this.passstep = 2;
          this.$emit("update:passstep", this.passstep);
          this.$emit("update:email", this.email);
        }, 1000);
        
      }
    },
  },
};
</script>