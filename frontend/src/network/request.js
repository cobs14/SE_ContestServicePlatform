import axios from 'axios'
import qs from 'qs'

//TODO: 重要事项：
//      requestPost和requestGet只保证传输文本OK
//      二进制流和文件未经测试
export function requestPost(config, jwt = null) {
    return new Promise((resolve, reject) => {
        //创建axios实例
        const instance = axios.create({
            baseURL: '/api',
            method: "post",
            transformRequest: [function (data) {
                //后端采用JSON传输数据
                return JSON.stringify(data);
                const d = qs.stringify(data)
                return d;
            }],
            headers: (jwt == null ? { 'Content-Type': 'application/json', } : {
                'Content-Type': 'application/json',
                'jwt': jwt
            }),
        })
        // 发送网络请求
        instance(config).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err)
        })
    })
}
