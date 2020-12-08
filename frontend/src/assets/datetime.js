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