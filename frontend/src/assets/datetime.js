export function stringToDateObject(str) {
    let res = str.split('-').map((x) => parseInt(x));
    console.log('parsed res', res);
    let commonTime = new Date(Date.UTC(res[0], res[1] - 1, res[2], 0, 0, 0));
    console.log('common time is', commonTime);
    return commonTime;

}

// TODO: not tested
export function toLocaleTimeString(timestamp) {
    let unixTimestamp = new Date(timestamp * 1000);
    commonTime = unixTimestamp.toLocaleString();
    console.log(commonTime);
    return commonTime;
}

export function dateStringToTimestamp(str) {
    let res = str.split('-').map((x) => parseInt(x));
    console.log('parsed res', res);
    let commonTime = new Date(Date.UTC(res[0], res[1] - 1, res[2], 0, 0, 0));
    console.log('common time is', commonTime);
    return Math.floor(commonTime.getTime() / 1000);
}

// timestamp的单位为秒
export function secondTimestampParser(timestamp) {
    return millisecondTimestampParser(1000 * timestamp);
}

// timestamp的单位为毫秒
export function millisecondTimestampParser(timestamp) {
    let tmp = new Date();
    let cur = tmp.getTime();
    let delta = cur - timestamp;
    if (delta > 0) {
        if (delta < 1000) return "刚刚";
        else if ((delta /= 1000) < 60) return Math.round(delta) + "秒前";
        else if ((delta /= 60) < 60) return Math.round(delta) + "分钟前";
        else if ((delta /= 60) < 24) return Math.round(delta) + "小时前";
        else if ((delta /= 24) < 30) return Math.round(delta) + "天前";
        else {
            tmp = new Date();
            tmp.setTime(timestamp);
            return tmp.toLocaleString();
        }
    }
    else {
        delta = Math.abs(delta);
        if (delta < 1000) return "少于一秒";
        else if ((delta /= 1000) < 60) return Math.round(delta) + "秒后";
        else if ((delta /= 60) < 60) return Math.round(delta) + "分钟后";
        else if ((delta /= 60) < 24) return Math.round(delta) + "小时后";
        else if ((delta /= 24) < 30) return Math.round(delta) + "天后";
        else {
            tmp = new Date();
            tmp.setTime(timestamp);
            return tmp.toLocaleString();
        }
    }
}