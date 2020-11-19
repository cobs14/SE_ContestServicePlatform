import axios from 'axios'
import qs from 'qs'
export function request(config, jwt = null) {
    return new Promise((resolve, reject) => {
        //创建axios实例
        const instance = axios.create({
            baseURL: 'http://localhost:8000/api/',
            transformRequest: [function (data) {
                const d = qs.stringify(data)
                return d;
            }],
            headers: (jwt == null ? { 'Content-Type': 'text/plain;charset=UTF-8', } : {
                'Content-Type': 'text/plain;charset=UTF-8',
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