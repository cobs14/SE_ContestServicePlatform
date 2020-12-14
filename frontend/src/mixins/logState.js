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
            for (let key in keys) {
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
        getUserId: function () {
            return Number(this.$cookies.get('userId'))
        },
        getUserJwt: function () {
            return this.$cookies.get('jwt');
        },

        // 判断是否为普通用户
        isCommonUser: function () {
            return this.$cookies.get('userType') == 'user';
        },

        // 判断是否为竞赛发布者
        isSponsor: function () {
            return this.$cookies.get("userType") == 'sponsor';
        },

        // 判断是否为管理员
        isAdmin: function () {
            return this.$cookies.get("userType") == 'admin';
        },

        // 取得用户类别
        getUserType: function () {
            return this.$cookies.get("userType");
        },

        // 获取用户名
        getUsername: function () {
            return this.$cookies.get('username');

        },
        
        //TODO: 还需要写加密相关的代码
    }
}