import requests
from bs4 import BeautifulSoup
import time
import os
import subprocess
import json

# 定义请求头部信息
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'http://10.30.12.10:30004',
    'Referer': 'http://10.30.12.10:30004/byod/view/byod/template/templatePc.html?customId=16&usermac=00-13-EF-8F-69-E9&userip=10.60.82.213&userurl=http://www.msftconnecttest.com/redirect&original=http://www.msftconnecttest.com/redirect&ssid=gtxy_wifi&nasRedirectUrl=http://10.30.12.10:30004/byod/index.html?usermac=00-13-EF-8F-69-E9&userip=10.60.82.213&userurl=http://www.msftconnecttest.com/redirect&original=http://www.msftconnecttest.com/redirect&ssid=gtxy_wifi',
    'X-Requested-With': 'XMLHttpRequest',
    #'Cookie': 'userip=10.60.82.213'
}

# 登录和检查状态的数据
dataLogin = {
    "code": 0,
    "msg": "success",
    "data": {
        "showLoginDown": True
    }
}

dataCheck = {
    "userName": "20224301003048",
    "userPassword": "MTIxMzM0",
    "serviceSuffixId": "-1",
    "dynamicPwdAuth": False,
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

# 断开或连接以太网
def manage_ethernet(action):
    try:
        if action in ["disconnect", "disable", "dis"]:
            result = os.system('netsh interface set interface "以太网" admin=disable')
            if result != 0:
                print("Failed to disable Ethernet.")
        elif action in ["connect", "enable", "en"]:
            result = os.system('netsh interface set interface "以太网" admin=enable')
            if result != 0:
                print("Failed to enable Ethernet.")
        else:
            print("Invalid operation, choose 'disconnect' or 'connect'.")
    except Exception as e:
        print(f"Error managing Ethernet interface: {e}")

# 检查IP地址的连通性
def check_ping(ip, count=1, timeout=1000):
    cmd = 'ping -n %d -w %d %s' % (count, timeout, ip)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout
    if '丢失 = 0' in output:
        return 'ok'
    else:
        return 'failed'

# 检查WiFi连接状态
def check_wifi_status(session, checkStatus, dataCheck):
    try:
        response = session.post(url=checkStatus, headers=headers, data=json.dumps(dataCheck), timeout=5)
        response.encoding = 'utf-8'
        content = response.text
        try:
            content_json = json.loads(content)
            if content_json.get("result") in ["wait", "success"]:
                print(time.asctime(time.localtime(time.time())), "当前处于在线状态。")
                return True
            else:
                print(time.asctime(time.localtime(time.time())), "当前已经下线，正在尝试登录！")
                return False
        except json.JSONDecodeError:
            print(f"无法解析JSON响应：{content}")
            return False
    except (requests.ConnectionError, requests.Timeout) as e:
        print(f"检查WiFi连接状态时发生网络错误: {e}")
        return False
    except Exception as e:
        print(f"检查WiFi连接状态时发生错误: {e}")
        return False

# 锐捷认证登录
def login_ruijie(session, username, password, login_url, dataLogin):
    try:
        response = session.post(login_url, headers=headers, data=json.dumps(dataLogin), timeout=5)
        response.encoding = 'utf-8'
        content = response.text
        try:
            content_json = json.loads(content)
            if content_json.get("result") == "success":
                print(time.asctime(time.localtime(time.time())), "登录成功！")
                return True
            else:
                print(f"登录失败，服务器返回错误信息：{content_json}")
                return False
        except json.JSONDecodeError:
            print(f"无法解析JSON响应：{content}")
            return False
    except (requests.ConnectionError, requests.Timeout) as e:
        print(f"登录时发生网络错误: {e}")
        return False
    except Exception as e:
        print(f"登录时发生错误: {e}")
        return False

# 检查WiFi是否已连接
def wifi_connected():
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "已连接" in result.stdout:
        print("Wi-Fi已连接\n")
        return True
    return False

# 开始连接
def start_connect(auth_url, username, password, checkStatus, dataCheck):
    tic = 0
    manage_ethernet("disconnect")
    time.sleep(3)
    
    session = requests.Session()
    wifi_connected()
    while not check_wifi_status(session, checkStatus, dataCheck):
        if login_ruijie(session, username, password, auth_url, dataLogin):
            print("认证成功，等待WiFi连接...")
            tic += 1
            if tic > 3:
                break
            time.sleep(5)
        else:
            print("认证失败，重试中...")
            time.sleep(5)
    
    manage_ethernet("connect")
    time.sleep(5)

def main():
    auth_url = "http://10.30.12.10:30004/byod/byodrs/login/defaultLogin"
    checkStatus = "http://10.30.12.10:30004/byod/byodrs/login/queryResult"
    username = "20224301003048"
    password = "MTIxMzM0"

    start_connect(auth_url, username, password, checkStatus, dataCheck)

if __name__ == '__main__':
    main()