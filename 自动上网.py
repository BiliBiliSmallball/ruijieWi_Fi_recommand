import requests
from bs4 import BeautifulSoup
import time
import os

# 断开或连接以太网
def manage_ethernet(action):
    try:
        if action in ["disconnect", "disable", "dis"]:
            os.system('netsh interface set interface "以太网" admin=disable')
        elif action in ["connect", "enable", "en"]:
            os.system('netsh interface set interface "以太网" admin=enable')
        else:
            print("Invalid operation, choose 'disconnect' or 'connect'.")
    except Exception as e:
        print(f"Error managing Ethernet interface: {e}")

# 锐捷认证登录
def ruijie_login(url, username, password):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }
    session = requests.Session()
    try:
        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        form_data = {
            "userName": username,
            "userPassword": password,
            "serviceSuffixId": "-1",
            "dynamicPwdAuth": 'false',
            "code": "",
            "codeTime": "",
            "validateCode": "",
            "licenseCode": "",
            "userGroupId": 0,
            "validationType": 0,
            "guestManagerId": 19806,
            "shopIdE": 'null',
            "wlannasid": 'null'
        }

        login_response = session.post(url, headers=headers, data=form_data)
        if login_response.status_code == 200:
            print("登录成功")
            return True
        else:
            print("登录失败，状态码：", login_response.status_code)
            return False
    except Exception as e:
        print(f"登录时出错：{e}")
        return False

# 检查WiFi连接状态
def check_wifi_status():
    wifi_status = os.popen('netsh wlan show interfaces').read()
    return "状态 : 已连接" in wifi_status

# 开始连接过程
def start_connect(auth_url, username, password):
    manage_ethernet("disconnect")
    time.sleep(5)
    
    while not check_wifi_status():
        if ruijie_login(auth_url, username, password):
            print("认证成功，等待WiFi连接...")
            time.sleep(5)  # 确保有足够的时间完成WiFi连接
        else:
            print("认证失败，重试中...")
            time.sleep(5)  # 等待几秒后重试
    
    print("WiFi已连接")
    manage_ethernet("connect")
    time.sleep(5)

def main():
    auth_url = "http://10.30.12.10:30004/byod/byodrs/login/defaultLogin"
    username = "20224301003048"
    password = "MTIxMzM0"  # 请确保密码是正确的
    ssid = "gtxy_wifi"

    start_connect(auth_url, username, password, ssid)

if __name__ == '__main__':
    main()
