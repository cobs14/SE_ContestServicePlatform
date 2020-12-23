<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" scrollable max-width="300px" @click:outside="disable">
      <v-card>
        <v-card-title>
            获奖名单
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text style="height: 300px">
          <v-radio-group v-model="dialogm1" column>
            <v-radio label="第一名：Cobs" value="bahamas"></v-radio>
            <v-radio label="第二名：Cobs" value="bahrain"></v-radio>
            <v-radio label="第三名：Cobs" value="bangladesh"></v-radio>
            <v-radio label="第四名：Cobs" value="barbados"></v-radio>
          </v-radio-group>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="showRouter">
            查看我的获奖信息
          </v-btn>
          <v-btn color="grey darken-1" text @click="disable">
            取消
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  name: 'showAwardsDlg',
  data () {
    return {
      dialogm1: ''
    }
  },
  props: ['dialog'],
  methods: {
    disable: function () {
      this.$emit('disable')
    },
    showRouter: function () {
      this.$emit('routeTo', '/showAwards')
    }
  }

}
</script>
