<template>
  <div id="ContestCreate">
    <v-container>
      <v-stepper alt-labels :value="createStep">
        <v-stepper-header>
          <v-stepper-step 
            editable
            step="1"
          >
            竞赛基本信息
          </v-stepper-step>
          <v-stepper-step 
            editable
            step="2"
          >
            竞赛详细信息
          </v-stepper-step>
        </v-stepper-header>
        <v-divider></v-divider>
        <v-stepper-items>
          <v-stepper-content
            :step = "1"   
            >
            <v-row>
              <v-spacer> </v-spacer>
                <v-divider> </v-divider>
                <v-container>
                  <v-card flat style="width: 100%">
                    <v-col>
                      <v-text-field 
                        label="竞赛名称"
                        outlined
                        v-model="contestName"
                        :error-messages="contestNameErrors"
                        :counter="64"
                        @input="$v.contestName.$touch()"
                        @blur="$v.contestName.$touch()"
                      >
                      </v-text-field>
                      <v-select
                        v-model="contestModules"
                        :items="moduleItems"
                        chips
                        label="竞赛模块"
                        multiple
                        outlined
                      >
                      </v-select>
                      <v-textarea 
                        label="竞赛简介"
                        outlined
                        v-model="contestAbstract"
                        :error-messages="contestAbstractErrors"
                        :counter="256"
                        @input="$v.contestAbstract.$touch()"
                        @blur="$v.contestAbstract.$touch()"
                      ></v-textarea>
                      <v-row>
                        <v-col>
                        <v-radio-group v-model="allowGroup" row>
                          <v-radio
                            label="个人赛"
                            :value="false"
                          ></v-radio>
                          <v-radio
                            label="团体赛"
                            :value="true"
                          ></v-radio>
                        </v-radio-group>
                        </v-col>
                        <v-col>
                          <v-text-field 
                            label="队伍人数下限"
                            outlined
                            :disabled="!allowGroup"
                            type="number"
                            v-model="minGroupMember"
                            :error-messages="minGroupMemberErrors"
                            @input="$v.minGroupMember.$touch(); $v.maxGroupMember.$touch()"
                            @blur="$v.minGroupMember.$touch(); $v.maxGroupMember.$touch()"
                          >
                          </v-text-field>
                        </v-col>
                        <span class="text">_</span>
                        <v-col>
                          <v-text-field 
                            label="队伍人数上限"
                            outlined
                            :disabled="!allowGroup"
                            type="number"
                            v-model="maxGroupMember"
                            :error-messages="maxGroupMemberErrors"
                            @input="$v.maxGroupMember.$touch()"
                            @blur="$v.maxGroupMember.$touch()"
                          >
                          </v-text-field>
                        </v-col>
                      </v-row>
                      <v-timeline
                        dense
                      >
                        <v-timeline-item
                          v-for="(select, index) in timeSelect" :key="index"
                        >
                          <v-menu
                            ref="menu"
                            v-model="dateMenu[index]"
                            :close-on-content-click="true"
                            
                            :return-value.sync="date"
                            transition="scale-transition"
                            offset-y
                            min-width="290px"
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <!--
                              <v-checkbox
                                v-if="index == 2"
                                label="开始比赛后仍允许报名"
                              >
                              </v-checkbox>
                              -->
                              <v-text-field
                                v-model = date[index]
                                :label= select.text
                                prepend-icon="event"
                                readonly
                                v-bind="attrs"
                                v-on="on"
                              ></v-text-field>
                              
                            </template>
                            
                            <v-date-picker
                              v-model = date[index]
                              :min="lastDate[index]"
                              no-title
                              scrollable
                            >
                              <v-spacer></v-spacer>
                            </v-date-picker>
                          </v-menu>
                          
                        </v-timeline-item>
                      </v-timeline>
                      <v-row>
                        <v-spacer></v-spacer>
                        <v-btn class="info ma-1" @click="createStep = 2"> 下一步 </v-btn>
                        <v-btn class="warning ma-1"> 重置 </v-btn>
                      </v-row>
                    </v-col>
                  </v-card>
                </v-container>
              <v-spacer> </v-spacer>
            </v-row>
          </v-stepper-content>
          <v-stepper-content
            :step = "2"
          >
          </v-stepper-content>
        </v-stepper-items>
        </v-stepper>
    </v-container>
  </div>
</template>

<script>
import merge from "webpack-merge";
import { redirect } from "@/mixins/router.js";
import { snackbar } from "@/mixins/message.js";
import { validationMixin } from "vuelidate";
import {
  required,
  maxLength,
  email,
  sameAs,
  minLength,
} from "vuelidate/lib/validators";
export default {
  name: 'ContestCreate',
  validations:{
    contestName: {
      required,
      maxLength: maxLength(64)
    },
    contestAbstract:{
      required,
      maxLength: maxLength(256)
    },
    minGroupMember:{
      required,
    },
    maxGroupMember:{
      required,
    }
  },
  computed: {
    contestNameErrors() {
      const errors = [];
      if (!this.$v.contestName.$dirty) return errors;
      !this.$v.contestName.required && errors.push("请输入竞赛名称");
      !this.$v.contestName.maxLength && errors.push("竞赛名称至多64个字符");
      return errors;
    },
    contestAbstractErrors() {
      const errors = [];
      if (!this.$v.contestAbstract.$dirty) return errors;
      !this.$v.contestAbstract.required && errors.push("请输入竞赛简介");
      !this.$v.contestAbstract.maxLength && errors.push("竞赛简介至多64个字符");
      return errors;
    },
    minGroupMemberErrors() {
      const errors = [];
      if (!this.$v.minGroupMember.$dirty) return errors;
      !this.$v.minGroupMember.required && errors.push("请输入队伍最低人数限制");
      return errors;
    },
    maxGroupMemberErrors() {
      const errors = [];
       if (!this.$v.maxGroupMember.$dirty) return errors;
      !this.$v.maxGroupMember.required && errors.push("请输入队伍最高人数限制");
      (this.maxGroupMember < this.minGroupMember) && errors.push("最高人数不可少于最低人数");
      return errors;
    },
    lastDate() {
      const date = [];
      date.push('0');
      for(let i = 0; i < 5; ++i){
        date.push(this.date[i]);
      }
      console.log(date);
      return date;
    }
  },
  data() {
    return {
      contestName: "",
      contestAbstract: "",
      contestModules: [],
      createStep: 1,
      allowGroup: false,
      minGroupMember: 1,
      maxGroupMember: 1,
      date: [],
      dateMenu: [],
      moduleItems: ['数字', '计算机', '物理'],
      timeSelect:[
        { text: '报名开始时间' },
        { text: '报名结束时间' },
        { text: '竞赛开始时间' },
        { text: '竞赛结束时间' },
        { text: '评审开始时间' },
        { text: '评审结束时间' }
      ]
    };
  },
  methods: {
    next() {
      console.log(this.allowGroup);
    },
    allowedDate(index){

    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
