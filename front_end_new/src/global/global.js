
//文件上传的api
const cosApi = "http://43.143.226.11:8003/cos/upload";
// 用户的登陆状态
let loginStatus = false;
// 当前登陆的用户信息
let user = {
    nickname: "admin",
    avatar: '',
    id: 1,
};

// 修改登陆状态
function setLoginStatus(status) {
    this.loginStatus = status;
}
// 修改当前登陆的用户信息
function setUser(user) {
    this.user = user;
}
export default {
    cosApi,
    loginStatus,
    user,
    setLoginStatus,
    setUser
}