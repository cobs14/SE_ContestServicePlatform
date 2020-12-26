// 组件：登录状态管理
// 提供了全局的登录状态管理接口
// 使得任意位置的函数都能更方便地管理用户登录状态
// 及获取登录用户的相关信息
export const logState = {
    inject: ['softReload'],
    data() {
        return {
            loggingIn: false,
        }
    },
    methods: {
        // 用户主动退出登录时调用
        userLogout: function () {
            let keys = this.$cookies.keys();
            for (let key in keys) {
                this.$cookies.remove(keys[key]);
            }
            this.softReload();
            this.snackbar("您已成功退出登录", "success");
        },
        // 用户登录信息过期时调用
        clearLogInfo: function () {
            //Used when server noticed that our loginfo is not valid
            if (!this.hasLogin()) return;
            let keys = this.$cookies.keys()
            for (let key in keys) {
                this.$cookies.remove(keys[key]);
            }
            this.softReload('/login');
            this.snackbar("您的登录信息已过期，请重新登录", "warning");
        },
        // 判断用户是否已经登录
        hasLogin: function () {
            return this.$cookies.isKey('jwt');
        },
        // 获取登录用户的ID
        getUserId: function () {
            return Number(this.$cookies.get('userId'))
        },
        // 获取登录用户的身份凭证（JWT）
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
        // 获取头像
        getUserAvatar: function () {
            return this.$cookies.get('avatar');
        },
    }
}