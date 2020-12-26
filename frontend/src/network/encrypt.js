// 加密相关算法
import CryptoJS from 'crypto-js';
import JSEncrypt from 'jsencrypt';

export default {
    //随机生成指定长度的16进制AES算法的key
    AESgeneratekey(num = 16) {
        let library = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        let key = "";
        for (var i = 0; i < num; i++) {
            let randomPoz = Math.floor(Math.random() * library.length);
            key += library.substring(randomPoz, randomPoz + 1);
        }
        return key;
    },

    //AES加密
    AESencrypt(word, keyStr) {
        var key = CryptoJS.enc.Utf8.parse(keyStr);
        var srcs = CryptoJS.enc.Utf8.parse(word);
        var encrypted = CryptoJS.AES.encrypt(srcs, key, { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7 });
        return encrypted.toString();
    },

    //AES解密
    AESdecrypt(word, keyStr) {
        var key = CryptoJS.enc.Utf8.parse(keyStr);
        var decrypt = CryptoJS.AES.decrypt(word, key, { mode: CryptoJS.mode.ECB, padding: CryptoJS.pad.Pkcs7 });
        return CryptoJS.enc.Utf8.stringify(decrypt).toString();
    },

    //RSA加密
    RSAencrypt(word, pubKey) {
        let encryptor = new JSEncrypt();
        encryptor.setPublicKey(pubKey); // 设置 加密公钥
        let encrypted = encryptor.encrypt(word.toString());  // 加密
        return encrypted;
    }
}