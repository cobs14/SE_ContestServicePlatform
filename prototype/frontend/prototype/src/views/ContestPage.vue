<template>
  <div id="ContestPage">
    <v-container>
      <v-img
        src="https://publicqn.saikr.com/2020/09/25/contest5f6dacbecf3c23.844776221601023249623.png?imageView2/2/w/1080"
      />
      <v-row>
        <v-card-title class="font-weight-black" style="font-size: 2.2em">
          全国大学生算法竞赛
        </v-card-title>
        <v-spacer> </v-spacer>
        <v-card elevation="0" text>
          <v-card-title class="grey--text text--darken-2">
            正在报名
          </v-card-title>
          <v-card-subtitle> 还有9天截止 </v-card-subtitle>
        </v-card>
        <v-btn class="success ma-3" title x-large> 现在报名 </v-btn>
      </v-row>
      <v-divider> </v-divider>
      <v-card elevation="0" text style="min-height: 1200px">
        <v-navigation-drawer absolute permanent right style="width:22%">
          <template v-slot:prepend>
            <v-list-item two-line>
              <v-list-item-avatar>
                <img
                  src="https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=3096801686,872084145&fm=26&gp=0.jpg"
                />
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-subtitle>赛事发布方</v-list-item-subtitle>
                <v-list-item-title>浙江省教育厅</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>

          <v-divider></v-divider>

          <v-list dense>
            <v-list-item v-for="item in items" :key="item.title">
              <v-container elevation="0" text>
                <v-row>
                  <v-list-item-icon>
                    <v-icon>{{ item.icon }}</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                  </v-list-item-content>
                </v-row>
                <v-card-subtitle>{{ item.content }}</v-card-subtitle>
                <v-divider> </v-divider>
              </v-container>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>

        <v-card style="width: 78%">
          <v-card-title class="font-weight-black headline">
            大赛介绍
          </v-card-title>
          <v-card-text>
            CCF大数据与计算智能大赛（以下简称CCF
            BDCI）由中国计算机学会2013年创办。大赛是大数据与人工智能领域的算法、应用、系统、创业大型挑战赛事。大赛面向重点行业和应用领域征集需求，以前沿技术与行业应用问题为导向，以促进行业发展及产业升级为目标，以众智、众包的方式，汇聚海内外产学研用多方智慧，为社会发现和培养了大量高质量数据人才。
            大赛迄今已成功举办七届，参赛规模、影响力逐年增强，累计吸引到了全球1500余所高校、1800家企事业单位及80余所科研机构的9万余人参与。其中，仅2019年第七届大赛，吸引全球25个国家的28269人组成25045支队伍参赛，这些参赛队伍来自谷歌、腾讯等1282家企业、麻省理工、清华大学等1215所高校，提交作品8万余件。大赛已经成为中国大数据与人工智能领域最具影响力的活动之一，是大数据综合赛事第一品牌。
            2020年，第八届CCF
            BDCI大赛进一步扩大参与规模及影响力，关注技术发展与人才培养，助力推动我国大数据技术及产业生态发展。
          </v-card-text>
          <v-card-title class="font-weight-black headline">
            赛程赛制
          </v-card-title>
          <v-card-text>
            大赛赛程10个月，分为公益专题赛、竞技赛、训练赛三个系列，竞技赛采用初赛、决赛“二级赛制”，具体赛程如下：
            2020/02-2020/06 “科技战疫”专题赛举办 2020/09/29 赛题发布，开放报名
            2020/10/13 启动仪式，开放数据下载及作品评测 2020/10/13-2020/12/06
            举办线上初赛，参赛者提交基础作品（部分赛题在此环节含复赛）
            2020/12/07-2020/12/18 作品提交截止，决赛入围资格审核 2020/12/下旬
            大赛决赛，答辩评审及颁奖典礼 备注：赛程时间根据实际情况调整。
          </v-card-text>
          <v-card-title class="font-weight-black headline">
            赛题方向
          </v-card-title>
          <v-card-text>
            本次大赛分为大数据算法赛道、自主平台赛道、先进系统赛道、创新创业赛道、训练赛道共“五大赛道”，通过此系列联赛，助力国家发展战略，通过多种形式的赛道，进行线上赛宣传、参赛，考察参赛者的算法能力、应用创新能力、基础系统优化以及实践应用能力，发掘优秀团队，通过线下赛评审、嘉奖，推动作品应用落地。
            大数据算法赛道 ：通过算法模型，就某场景或行为的特定指标进行优化。
            自主平台赛道：通过使用国产AI开源框架，进行相应算法赛题的研究。
            先进系统赛道：通过解决方案，提升对指定数据或环境的系统优化能力。
            创新创业赛道
            ：提交围绕大数据、人工智能、相关技术及其在制造、健康、交通、零售、家居、教育、金融等行业场景的创新项目。
            训练赛道：根据公开数据集，出具自然语言处理、图像识别、分类预测等不同方向的低难度赛题，辅助参赛者学习。
          </v-card-text>
          <v-card-title class="font-weight-black headline">
            大赛奖励
          </v-card-title>
          <v-card-text>
            参赛选手奖项
            单赛题奖：单赛题将评选出一二三等共五支团队，各获奖团队队员均可获得奖金、证书、面试绿色通道等奖励。
            CCF综合奖：CCF综合奖将评选出综合特等奖一名、最佳单项奖三名，参赛团队队员均可获得奖金、证书及相关荣誉。
            参赛特别奖：在线上赛过程中将根据参赛团队每周排名、开源算法及人气获得周冠军奖、开源挑战奖及人气奖等特别奖项。
            评审专家奖项
            优秀指导老师：CCF综合奖获奖团队指导教师均可获得优秀指导老师奖，并在决赛颁奖典礼颁发奖杯。
            CCF评审专家证书：参与CCF BDCI评审的专家学者均可获得CCF评审专家奖杯。
            突出贡献奖：参与CCF
            BDCI题目出具、走进高校的专家学者均可获得CCF突出贡献奖奖杯。
            合作伙伴奖项
            优秀案例：部分出题企业所出具的优质赛题可获得由CCF颁发的优秀案例奖杯。
            优秀合作伙伴：部分出题企业将获得由CCF颁发的优秀合作伙伴奖杯。
          </v-card-text>
          <v-card-title class="font-weight-black headline">
            联系方式
          </v-card-title>
          <v-card-text> 可以扫描下方二维码加群联系： </v-card-text>
          <v-row>
            <v-spacer> </v-spacer>
            <v-img
              max-height="250"
              max-width="250"
              src="https://www.saikr.com/qrc/img?size=10&text=https%3A%2F%2Fwww.saikr.com%2Fraces%2F39657"
            />
            <v-spacer> </v-spacer>
          </v-row>
          <v-row>
            <v-spacer> </v-spacer>
            <v-btn class="success ma-3" title x-large> 现在报名 </v-btn>
            <v-spacer> </v-spacer>
          </v-row>
        </v-card>
      </v-card>
    </v-container>
  </div>
</template>

<script>
/* eslint-disable */
import infocard from "@/components/ManagePageCard.vue";
export default {
  name: "ContestPage",
  components: {
    infocard,
  },
  data() {
    return {
      type: this.$route.params.type || "contest_list",
      items: [
        { icon: "list", title: "竞赛级别", content: "国家赛" },
        { icon: "source", title: "报名要求", content: "在校本科生" },
        { icon: "attach_money", title: "报名费用", content: "50元" },
        {
          icon: "card_membership",
          title: "奖项设置",
          content:
            "根据得分排名，前三名为一等奖，前十名为二等奖，前五十名为三等奖",
        },
      ],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
