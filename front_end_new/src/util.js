//获取当前日期函数
function getNowFormatDate() {
    let date = new Date(),
        year = date.getFullYear(), //获取完整的年份(4位)
        month = date.getMonth() + 1, //获取当前月份(0-11,0代表1月)
        strDate = date.getDate() // 获取当前日(1-31)
    if (month < 10) month = `0${month}` // 如果月份是个位数，在前面补0
    if (strDate < 10) strDate = `0${strDate}` // 如果日是个位数，在前面补0

    return `${year}-${month}-${strDate}`
}

// 获取最近14天的日期，间隔一天，返回数组
function getLast14Days() {
    const result = [];
    const today = new Date();

    for (let i = 13; i >= 0; i = i - 1) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);

        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');

        // result.push(`${year}-${month}-${day}`);
        result.push(`${month}-${day}`);

    }

    return result;
}




function dataURLToFile(dataUrl, fileName) {
    const dataArr = dataUrl.split(',');
    const mime = dataArr[0].match(/:(.*?);/)[1];
    const bstr = atob(dataArr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], fileName, { type: mime });
}

function blobToFile(blob, filename, type) {
    return new File([blob], filename, { type })
}


//
function getCookie(name) {
    if (document.cookie.length > 0) {
        let arr = document.cookie.split('; '); // 通过; 将数据转成数组
        for (let i = 0; i < arr.length; i++) {
            let index = arr[i].indexOf("="); // 返回第一个“=”所在的位置
            let key = arr[i].substring(0, index);
            if (key === name) {
                return decodeURIComponent(arr[i].substring(index + 1));
            }
        }
    }
    return "";
}


export default {
    getNowFormatDate,
    getLast14Days,
    dataURLToFile,
    blobToFile,
    getCookie
}