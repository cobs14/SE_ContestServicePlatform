// 组件：消息提示
// snackbar将在页面的上方显示出多种不同的提示信息
// 如操作成功、失败、警示或者一般的提示信息
// 使用该组件将使其它函数能够快速发送提示信息，无需重复实现功能
export const snackbar = {
  methods: {
    snackbar: function (message, color = null) {
      let msg = (message instanceof Object ? message : {
        message: message,
        color: color == null ? 'info' : color
      })
      this.$emit('showSnackbar', msg)
    },
  }
}