<template>
  <div id="ContestCreate">
    <v-container>
      <v-stepper alt-labels :value="createStep">
        <v-stepper-header>
          <v-stepper-step 
            step="1"
          >
            竞赛基本信息
          </v-stepper-step>
          <v-stepper-step 
            step="2"
          >
            竞赛详细信息
          </v-stepper-step>
          <v-stepper-step 
            step="3"
          >
            竞赛创建成功
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
                            :close-on-content-click="false"
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
                                v-model= date[index]
                                :disabled="lastDate[index] === undefined"
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
                              :max="allowDate[index]"
                              @input="dateMenu[index] = false"
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
                        <v-btn class="info ma-1" 
                        @click="gotoContestDescription"
                        :loading="sendingForm"
                        :disabled="sendingForm"
                        > 下一步 </v-btn>
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
            <description-card
              v-for="(info, index) in description" :key="index"
              :index="index"
              @showSnackbar="snackbar"
              v-on:content-change="updateDescription"
              v-on:delete-description="deleteDescription"
              :descriptionTitle="info.title"
              :descriptionContent="info.content"
            >
            </description-card>
          <v-row>
            <v-spacer></v-spacer>
            <v-btn class="info ma-2" @click="gotoContestMain">上一页</v-btn>
            <v-btn class="secondary ma-2" @click="description.push({title: '', content: ''}); emptyDescription = true">增加详情</v-btn>
            <v-btn class="success ma-2" 
            @click="submitContest"
            :loading="sendingForm"
            :disabled="emptyDescription || sendingForm"
            >提交创建申请</v-btn>
            <v-spacer></v-spacer>
          </v-row>
          </v-stepper-content>
          <v-stepper-content
            :step = "3"
          >
           <v-card flat style="width: 80%; margin: auto">
            <v-card-title class="font-weight-black" style="font-size: 1.6em">
               创建申请已经送出
            </v-card-title>
            <v-divider> </v-divider>
            <v-card-subtitle class="font-weight-medium" style="font-size: 1.1em">
              您的竞赛创建申请已经送出，请静待管理员的审核。
              <br/>

            </v-card-subtitle>
            <v-card-actions>
              <v-spacer></v-spacer>
              <!--v-btn class="secondary ma-2">创建其他竞赛</v-btn-->
              <v-btn class="success ma-2" @click="$emit('goto-list')">前往竞赛列表</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
        </v-card>
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
  minValue
} from "vuelidate/lib/validators";
import DescriptionCard from "@/components/ContestDescriptionCard.vue"
export default {
  name: 'ContestCreate',
  mixins: [redirect, snackbar, validationMixin],
  components:{
    DescriptionCard
  },
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
      minValue: minValue(1)
    },
    maxGroupMember:{
      required,
      minValue: minValue(1)
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
      !this.$v.minGroupMember.minValue && errors.push("队伍人数最少1人");
      return errors;
    },
    maxGroupMemberErrors() {
      const errors = [];
       if (!this.$v.maxGroupMember.$dirty) return errors;
      !this.$v.maxGroupMember.required && errors.push("请输入队伍最高人数限制");
      !this.$v.maxGroupMember.minValue && errors.push("队伍人数最少1人");
      (this.maxGroupMember < this.minGroupMember) && errors.push("最高人数不可少于最低人数");
      return errors;
    },
    lastDate() {
      const date = [];
      date.push("0");
      for(let i = 0; i < 5; ++i){
        date.push(this.date[i]);
      }
      return date;
    },
    allowDate() {
      const date = [];
      for(let i = 1; i < 6; ++i){
        date.push(this.date[i]);
      }
      return date;
    }
  },
  methods: {
    updateDescription(data) {
      this.description[data.index] = {title: data.title, content: data.content};
      if(data.title === '' || data.content === '') this.emptyDescription = true;
      else{
        this.emptyDescription = false;
      }
    },
    deleteDescription(data) {
      this.description.splice(data.index, 1);
      const length = this.description.length;
      if(length){
        this.emptyDescription = false;
        for(let i = 0; i < length; ++i){
          if(data.title === '' || data.content === '') {
            this.emptyDescription = true;
            break;
          }
        }
      }
      else{
        this.snackbar("请添加至少一条竞赛详细信息", "error");
        this.emptyDescription = true;
      }     
    },
    gotoContestDescription(){
      this.$v.$touch();
      if (this.$v.$invalid || this.date[5] === undefined || this.maxGroupMember < this.minGroupMember) {
        this.snackbar("请完整填写正确的信息", "error");
        this.sendingForm = false;
      } else {
        // do your submit logic here
        this.sendingForm = true;
        // simulating sending forms
        setTimeout(() => {
          this.sendingForm = false;
          this.createStep = 2;
        }, 1000);
        
      }
    },
    gotoContestMain(){
      this.createStep = 1;
      console.log(this.createStep)
    },
    submitContest() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.snackbar("请完整填写正确的信息", "error");
        this.sendingForm = false;
      } else {
        // do your submit logic here
        this.sendingForm = true;
        // simulating sending forms
        setTimeout(() => {
          this.sendingForm = false;
          this.createStep = 3;
        }, 1000);
        
      }
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
      description: [{title: '', content: ''}],
      emptyDescription: true,
      sendingForm: false,
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
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
