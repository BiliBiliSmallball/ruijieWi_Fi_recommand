# if __name__ == "__main__":
#     auth_url = "http://10.30.12.10:30004/byod/byodrs/login/defaultLogin"
#     username = "20224301003048"
#     password = "MTIxMzM0"  # 请确保密码是正确的

#     manage_ethernet("disconnect")
#     time.sleep(5)
#     # 调用函数进行登录
#     login_success = ruijie_login(auth_url, username, password)
#     manage_ethernet("connect")

#     time.sleep(5)

import subprocess
import requests
from bs4 import BeautifulSoup
import time
import os

# 检查是否连接到指定Wi-Fi网络
def isShuForAll(ssid):
    lines = []
    with os.popen("iwconfig 2>&1 | grep '%s'" % ssid, "r") as out:
        lines = out.readlines()
    return len(lines) > 0

# 断开或连接以太网
def manage_ethernet(action):
    if action in ["disconnect", "disable", "dis"]:
        subprocess.run(["netsh", "interface", "set", "interface", "name=以太网", "admin=disable"])
    elif action in ["connect", "enable", "en"]:
        subprocess.run(["netsh", "interface", "set", "interface", "name=以太网", "admin=enable"])
    else:
        print("Invalid operation, choose 'disconnect' or 'connect'.")

# 锐捷认证登录
def ruijie_login(url, username, password):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }
    session = requests.Session()
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 准备表单数据
    form_data = {
    "userName": username,
    "userPassword": password,
    "serviceSuffixId": "-1",
    "dynamicPwdAuth": false,
    "code": "",
    "codeTime": "",
    "validateCode": "",
    "licenseCode": "",
    "userGroupId": 0,
    "validationType": 0,
    "guestManagerId": 19806,
    "shopIdE": null,
    "wlannasid": null
}

    login_response = session.post(url, headers=headers, data=form_data)
    if login_response.status_code == 200:
        print("登录成功")
        return True
    else:
        print("登录失败")
        return False

# 开始连接过程
def start_connect(auth_url, username, password, ssid):
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    if not isShuForAll(ssid):
        print("%s not connected to %s" % (t, ssid))
        return
    manage_ethernet("disconnect")
    time.sleep(5)
    if ruijie_login(auth_url, username, password):
        print("%s connected successfully" % t)
    else:
        print("%s connection failed" % t)
    manage_ethernet("connect")
    time.sleep(5)

def main():
    auth_url = "http://10.30.12.10:30004/byod/byodrs/login/defaultLogin"
    username = "20224301003048"
    password = "MTIxMzM0"  # 请确保密码是正确的
    ssid = "gtxy_wifi"

    try:
        start_connect(auth_url, username, password, ssid)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
