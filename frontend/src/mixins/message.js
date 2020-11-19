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