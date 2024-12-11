import subprocess
import requests
from bs4 import BeautifulSoup
import time

def manage_ethernet(action):
    if action == "disconnect" or 'disable' or 'dis': 
        # 断开以太网连接
        subprocess.run(["netsh", "interface", "set", "interface", "name=以太网", "admin=disable"]) 
    elif action == "connect" or 'enable' or 'en': 
        # 连接以太网 
        subprocess.run(["netsh", "interface", "set", "interface", "name=以太网", "admin=enable"]) 
    else: 
        print("Invalid operation, choose 'disconnect' or 'connect'.")

def ruijie_login(url, username, password):
    """
    锐捷认证登录函数。
    
    参数:
    url -- 锐捷认证网页的URL
    username -- 用户名
    password -- 密码
    
    返回:
    True if 登录成功，否则 False
    """
    # 设置协议头
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }
    
    # 发送登录请求
    session = requests.Session()
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 准备表单数据
    form_data = {
        "userName": username,
        "userPassword": password,
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
    login_response = session.post(url, headers=headers, data=form_data)

    # 检查登录结果
    if login_response.status_code == 200:
        print("登录成功")
        return True
    else:
        print("登录失败")
        return False

if __name__ == "__main__":
    auth_url = "http://10.30.12.10:30004/byod/byodrs/login/defaultLogin"
    username = "20224301003048"
    password = "MTIxMzM0"  # 请确保密码是正确的

    manage_ethernet("disconnect")
    time.sleep(5)
    # 调用函数进行登录
    login_success = ruijie_login(auth_url, username, password)
    manage_ethernet("connect")

    time.sleep(5)
