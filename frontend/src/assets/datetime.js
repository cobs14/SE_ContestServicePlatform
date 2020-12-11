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
export function secondTimestampParser(timestamp, nonNegative = false) {
    return millisecondTimestampParser(1000 * timestamp, nonNegative);
}

// timestamp的单位为毫秒
export function millisecondTimestampParser(timestamp, nonNegative = false) {
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
        if (nonNegative) {
            return '刚刚';
        }
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

// 根据state（见查看竞赛的response），返回状态描述
export function getStateDescription(state) {
    console.log('what state do we got?', state);
    let cur = new Date().getTime() / 1000;
    if (cur < state.apply[0]) {
        return ['apply', 1, '报名未开始', secondTimestampParser(state.apply[0]) + '开始报名', 0];
    } else if (cur < state.apply[1]) {
        return ['apply', 2, '正在报名', secondTimestampParser(state.apply[1]) + '结束报名', 1];
    } else if (cur < state.contest[0]) {
        return ['contest', 1, '比赛未开始', secondTimestampParser(state.contest[0]) + '开始比赛', 2];
    } else if (cur < state.contest[0]) {
        return ['contest', 2, '比赛进行中', secondTimestampParser(state.contest[1]) + '结束比赛', 3];
    } else if (cur < state.review[0]) {
        return ['review', 1, '等待评审', secondTimestampParser(state.review[0]) + '开始评审', 4];
    } else if (cur < state.review[0]) {
        return ['review', 2, '评审进行中', secondTimestampParser(state.review[1]) + '结束评审', 5];
    } else if (cur < state.review[0]) {
        return ['review', 3, '评审已结束', '评审已经结束', 6];
    }
}