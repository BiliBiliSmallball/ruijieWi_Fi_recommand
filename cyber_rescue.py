import requests
from bs4 import BeautifulSoup
import time
import os
import subprocess

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
    'Cookie': 'userip=10.60.82.213'
}

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

# 检查IP地址的连通性
def check_ping(ip, count=1, timeout=1000):
    cmd = 'ping -n %d -w %d %s > NUL' % (count, timeout, ip)
    res = os.system(cmd)
    return 'ok' if res == 0 else 'failed'

# 检查WiFi连接状态
def check_wifi_status():
    try:
        wifi_status = os.popen('netsh wlan show interfaces').read()
        if "已连接" in wifi_status:
            print("Wi-Fi接口已连接")
            if check_ping("10.60.0.1") == "ok":
                print("与10.60.0.1的连通性正常")
                return True
            else:
                print("无法连接到10.60.0.1")
                return False
        else:
            print("Wi-Fi接口未连接")
            return False
    except Exception as e:
        print(f"检查WiFi连接状态时发生错误: {e}")
        return False

# 锐捷认证登录
def login_ruijie(session, username, password, login_url):
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    hidden_fields = {}
    for input_tag in soup.find_all('input', type='hidden'):
        hidden_fields[input_tag['name']] = input_tag.get('value', '')

    data = {
        "userName": username,
        "userPassword": password,
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
    data.update(hidden_fields)

    try:
        response = session.post(login_url, data=data, headers=headers)
        if response.status_code == 200:
            query_url = "http://10.30.12.10:30004/byod/byodrs/login/queryResult"
            query_response = session.get(query_url)
            if query_response.status_code == 200:
                result = query_response.json()
                if result.get("code") == 0 and result.get("msg") == "success":
                    print("登录成功！")
                    return True
                else:
                    print("登录失败，服务器返回错误信息：", result.get("msg"))
                    return False
            else:
                print("无法获取登录结果，状态码：", query_response.status_code)
                return False
        else:
            print("登录失败，请检查用户名和密码是否正确。")
            return False
    except Exception as e:
        print(f"发生错误: {e}")
        return False

def wifi_connected():
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "已连接" in result.stdout:
        print("Wi-Fi已连接\n")
        return True
    return False

def start_connect(auth_url, username, password):
    tic = 0
    manage_ethernet("disconnect")
    time.sleep(3)
    
    wifi_connected()
    session = requests.Session()
    while not check_wifi_status():
        if login_ruijie(session, username, password, auth_url):
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
    username = "20224301003048"
    password = "MTIxMzM0"
    ssid = "gtxy_wifi"

    start_connect(auth_url, username, password)

if __name__ == '__main__':
    main()
