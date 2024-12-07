import requests
from bs4 import BeautifulSoup

# 设置锐捷认证网页的URL，添加协议头
auth_url = "http://10.30.12.10:30004/byod/byodrs/login/defaultLogin"
#user-agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
# 设置你的用户名和密码
username = "20224301003048"
password = "121334"

# 发送登录请求
session = requests.Session()
response = session.get(auth_url)
soup = BeautifulSoup(response.content, 'html.parser')

form_data = {
    "userName": "20224301003048",
    "userPassword": "MTIxMzM0",
    "serviceSuffixId": "-1",
    "dynamicPwdAuth": "false",
    "code": "",
    "codeTime": "",
    "validateCode": "",
    "licenseCode": "",
    "userGroupId": 0,
    "validationType": 0,
    "guestManagerId": 19806,
    "shopIdE": "null",
    "wlannasid": "null"
}

# 提交表单
login_response = session.post(auth_url, data=form_data)

# 检查登录结果
if login_response.status_code != 200:
    print("登录失败")
else:
    print("登录成功")
