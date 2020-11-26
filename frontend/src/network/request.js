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

export function requestUploadPictures(config, jwt = null) {
    return new Promise((resolve, reject) => {
        //创建axios实例
        const instance = axios.create({
            baseURL: '/api/handlepic/upload',
            method: "post",
            transformRequest: [function (data) {
                // 传输文件和图片
                let formData = new window.FormData();
                formData.append('config', JSON.stringify(data['config']));
                for (let key in data) {
                    formData.append(key, data[key]);
                }
                console.log('origin data:', data, 'form data:', formData, formData.get('config'));
                return formData;
            }],
            headers: (jwt == null ? { 'Content-Type': 'multipart/form-data', } : {
                'Content-Type': 'multipart/form-data',
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
