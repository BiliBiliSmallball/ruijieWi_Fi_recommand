import requests
from bs4 import BeautifulSoup
import time
import os
import subprocess
import json
from log_config import log_message

# 定义请求头部信息
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'connection':'keep-alive',
    'Cache-Control': 'no-cache',
    "cookie":"testcookie=yes; userip=10.20.172.199",
    'host': '10.30.12.10:30004',
    'pragma':'no-cache',
    'Referer': 'http://10.30.12.10:30004/byod/index.html?usermac=00-13-EF-5F-40-4A&userip=10.20.172.199&userurl=http://www.msftconnecttest.com/redirect&original=http://www.msftconnecttest.com/redirect&ssid=gtxy_wifi',
    "upgrade-insecure-requests": '1'
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
        log_message(0, f"正在执行以太网操作: {action}", "wifi_reconnect_log.txt", "cyber_rescue.py")
        if action in ["disconnect", "disable", "dis"]:
            result = os.system('netsh interface set interface "以太网" admin=disable')
            if result != 0:
                log_message(1, "Failed to disable Ethernet.", "wifi_reconnect_log.txt", "cyber_rescue.py")
        elif action in ["connect", "enable", "en"]:
            result = os.system('netsh interface set interface "以太网" admin=enable')
            if result != 0:
                log_message(1, "Failed to enable Ethernet.", "wifi_reconnect_log.txt", "cyber_rescue.py")
        else:
            log_message(1, "Invalid operation, choose 'disconnect' or 'connect'.", "wifi_reconnect_log.txt", "cyber_rescue.py")
    except Exception as e:
        log_message(1, f"Error managing Ethernet interface: {e}", "wifi_reconnect_log.txt", "cyber_rescue.py")

# 检查IP地址的连通性
def check_ping(ip, count=1, timeout=1000):
    log_message(0, f"正在ping IP地址: {ip}", "wifi_reconnect_log.txt", "cyber_rescue.py")
    cmd = 'ping -n %d -w %d %s' % (count, timeout, ip)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = result.stdout
    if '丢失 = 0' in output:
        return 'ok'
    else:
        return 'failed'

# 检查WiFi连接状态
def check_wifi_status(session, checkStatus, dataCheck):
    log_message(0, "正在检查WiFi连接状态...", "wifi_reconnect_log.txt", "cyber_rescue.py")
    try:
        response = session.post(url=checkStatus, headers=headers, data=json.dumps(dataCheck), timeout=5)
        response.encoding = 'utf-8'
        content = response.text
        try:
            content_json = json.loads(content)
            if content_json.get("result") in ["wait", "success"]:
                log_message(0, "当前处于在线状态。", "wifi_reconnect_log.txt", "cyber_rescue.py")
                return True
            else:
                log_message(1, "当前已经下线，正在尝试登录！", "wifi_reconnect_log.txt", "cyber_rescue.py")
                return False
        except json.JSONDecodeError:
            log_message(1, f"无法解析JSON响应：{content}", "wifi_reconnect_log.txt", "cyber_rescue.py")
            return False
    except (requests.ConnectionError, requests.Timeout) as e:
        log_message(1, f"检查WiFi连接状态时发生网络错误: {e}", "wifi_reconnect_log.txt", "cyber_rescue.py")
        return False
    except Exception as e:
        log_message(1, f"检查WiFi连接状态时发生错误: {e}", "wifi_reconnect_log.txt", "cyber_rescue.py")
        return False

# 锐捷认证登录
def login_ruijie(session, username, password, login_url, dataLogin):
    log_message(0, "正在尝试登录锐捷...", "wifi_reconnect_log.txt", "cyber_rescue.py")
    try:
        response = session.post(login_url, headers=headers, data=json.dumps(dataLogin), timeout=5)
        response.encoding = 'utf-8'
        content = response.text
        try:
            content_json = json.loads(content)
            if content_json.get("result") == "success":
                log_message(0, "登录成功！", "wifi_reconnect_log.txt", "cyber_rescue.py")
                return True
            else:
                log_message(1, f"登录失败，服务器返回错误信息：{content_json}", "wifi_reconnect_log.txt", "cyber_rescue.py")
                return False
        except json.JSONDecodeError:
            log_message(1, f"无法解析JSON响应：{content}", "wifi_reconnect_log.txt", "cyber_rescue.py")
            return False
    except (requests.ConnectionError, requests.Timeout) as e:
        log_message(1, f"登录时发生网络错误: {e}", "wifi_reconnect_log.txt", "cyber_rescue.py")
        return False
    except Exception as e:
        log_message(1, f"登录时发生错误: {e}", "wifi_reconnect_log.txt", "cyber_rescue.py")
        return False

# 检查WiFi是否已连接
def wifi_connected():
    log_message(0, "正在检查WiFi是否已连接...", "wifi_reconnect_log.txt", "cyber_rescue.py")
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "已连接" in result.stdout:
        log_message(0, "Wi-Fi已连接", "wifi_reconnect_log.txt", "cyber_rescue.py")
        return True
    log_message(1, "Wi-Fi未连接", "wifi_reconnect_log.txt", "cyber_rescue.py")
    return False

# 开始连接
def start_connect(auth_url, username, password, checkStatus, dataCheck):
    tic = 0
    log_message(0, "开始连接流程...", "wifi_reconnect_log.txt", "cyber_rescue.py")
    manage_ethernet("disconnect")
    time.sleep(3)
    
    session = requests.Session()
    wifi_connected()
    while not check_wifi_status(session, checkStatus, dataCheck):
        if login_ruijie(session, username, password, auth_url, dataLogin):
            log_message(0, "认证成功，等待WiFi连接...", "wifi_reconnect_log.txt", "cyber_rescue.py")
            tic += 1
            if tic > 3:
                break
            time.sleep(5)
        else:
            log_message(1, "认证失败，重试中...", "wifi_reconnect_log.txt", "cyber_rescue.py")
            tic += 1
            if tic >= 5:
                log_message(1, "尝试连接5次失败，重新开启以太网并停止运行。", "wifi_reconnect_log.txt", "cyber_rescue.py")
                manage_ethernet("connect")
                return
            time.sleep(5)
    
    manage_ethernet("connect")
    time.sleep(5)

def main():
    auth_url = "http://10.30.12.10:30004/byod/view/byod/byodLogin.html"
    checkStatus = "http://10.30.12.10:30004/byod/byodrs/login/queryResult"
    username = "20224301003048"
    password = "MTIxMzM0"

    log_message(0, "程序开始运行...", "wifi_reconnect_log.txt", "cyber_rescue.py")
    start_connect(auth_url, username, password, checkStatus, dataCheck)
    log_message(0, "程序运行结束。", "wifi_reconnect_log.txt", "cyber_rescue.py")

if __name__ == '__main__':
    main()