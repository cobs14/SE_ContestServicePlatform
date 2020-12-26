// 组件：发送请求
// 使用该组件将可以满足不同函数发送多种请求的需求
import axios from 'axios'
import qs from 'qs'

// requestPost用于传输JSON类的信息
export function requestPost(config, jwt = null) {
    return new Promise((resolve, reject) => {
        //创建axios实例
        const instance = axios.create({
            baseURL: '/api',
            method: "post",
            transformRequest: [function (data) {
                //后端采用JSON传输数据
                return JSON.stringify(data);
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
            reject(err);
        })
    })
}

// 上传图片
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
                    if (key == 'config') { continue };
                    formData.append(key, data[key]);
                }
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

// 上传任意类型的文件
export function requestFormdata(config, jwt = null) {
    return new Promise((resolve, reject) => {
        //创建axios实例
        const instance = axios.create({
            baseURL: '/api',
            method: "post",
            transformRequest: [function (data) {
                // 传输文件和图片
                let formData = new window.FormData();
                for (let key in data) {
                    formData.append(key, data[key]);
                }
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

// 文件下载（保存到本地、触发下载窗口）
export function downloadFile(data, suffix, fullname = undefined) {
    if (!data) {
        return
    }
    let url = window.URL.createObjectURL(new Blob([data]))
    let link = document.createElement('a')
    link.style.display = 'none'
    link.href = url
    // 获取文件名
    // download 属性定义了下载链接的地址而不是跳转路径
    let filename = 'File' + new Date().toLocaleString() + '.' + suffix;
    if (fullname != undefined) {
        filename = fullname;
    }
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    URL.revokeObjectURL(link.href) // 释放URL对象
    document.body.removeChild(link)
}
