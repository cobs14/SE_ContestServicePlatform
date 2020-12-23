<template>
  <v-row justify="center" eager>
    <v-dialog v-model="dialog" scrollable max-width="300px" @click:outside="disable" eager>
      <v-card>
        <v-card-title>
            选择要提交的文件
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text style="height: 300px">
          <v-radio-group v-model="dialogm1" column>
            <v-radio label="文件1.txt" value="bahamas"></v-radio>
            <v-radio label="文件2.zip" value="bahrain"></v-radio>
            <v-radio label="代码1.c" value="bangladesh"></v-radio>
            <v-radio label="代码2.py" value="barbados"></v-radio>
          </v-radio-group>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="showRouter">
            提交
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
  name: 'submitFileDlg',
  data () {
    return {
      checkbox: true,
      dialogm1: 'bahamas'
    }
  },
  props: ['dialog'],
  methods: {
    disable: function () {
      this.$emit('disable')
    },
    showRouter: function () {
      this.$emit('routeTo', '/contest/finished')
    }
  }

}
</script>
