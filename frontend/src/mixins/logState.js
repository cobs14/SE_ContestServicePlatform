export const logState = {
    inject: ['softReload'],
    data() {
        return {
            loggingIn: false,
        }
    },
    methods: {
        userLogout: function () {
            let keys = this.$cookies.keys();
            console.log(keys);
            for (let key in keys) {
                console.log('what', key);
                this.$cookies.remove(keys[key]);
            }
            this.softReload();
            this.snackbar("您已成功退出登录", "success");
        },
        clearLogInfo: function () {
            //Used when server noticed that our loginfo is not valid
            let keys = this.$cookies.keys()
            for (let key in keys) {
                this.$cookies.remove(key);
            }
            this.softReload('/login');
            this.snackbar("您的登录信息已过期，请重新登录", "warning");
        },
        hasLogin: function () {
            return this.$cookies.isKey('jwt');
        },
        // getUserInfo: function () {

        // },
        getUserJwt: function () {
            return this.$cookies.get('jwt');
        },
        //TODO: 还需要写加密相关的代码
    }
}