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
            os.system('netsh interface set interface "以太网" admin=disable')
        elif action in ["connect", "enable", "en"]:
            os.system('netsh interface set interface "以太网" admin=enable')
        else:
            print("Invalid operation, choose 'disconnect' or 'connect'.")
    except Exception as e:
        print(f"Error managing Ethernet interface: {e}")

# 检查IP地址的连通性
def check_ping(ip, count=1, timeout=1000):
    """
    使用ping命令检查指定IP地址的连通性
    
    参数:
    ip -- 需要检查的IP地址
    count -- 发送ping请求的次数，默认为1次
    timeout -- 每次ping请求的超时时间，默认为1000毫秒
    
    返回值:
    如果ping命令执行成功且没有丢包，则返回'ok'，否则返回'failed'
    """
    # 构造ping命令，其中-n指定发送的ping的数量，-w指定等待回复的时间（毫秒）
    cmd = 'ping -n %d -w %d %s' % (count, timeout, ip)
    
    # 执行ping命令，捕获输出结果
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # 获取ping命令的输出结果
    output = result.stdout
    
    # 分析ping命令的输出结果，判断是否没有丢包
    if '丢失 = 0' in output:
        return 'ok'
    else:
        return 'failed'

# 检查WiFi连接状态
def check_wifi_status(session, checkStatus, dataCheck):
    """
    检查WiFi当前是否处于在线状态。
    
    参数:
    session: requests.Session对象，用于保持会话状态。
    checkStatus: 字符串，检查WiFi状态的URL。
    dataCheck: 字典，发送请求时携带的数据。
    
    返回:
    布尔值，True表示在线状态，False表示已下线或发生错误。
    """
    try:
        # 使用requests发送请求检查状态
        response = session.post(url=checkStatus, headers=headers, data=dataCheck)
        response.encoding = 'utf-8'
        # 处理响应内容以适应解析
        content = str(response.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode())
        i = content.find('"result":"')

        # 根据响应内容判断WiFi状态
        if content[i + 10:i + 14] == 'wait' or content[i + 10 + 17] == 'success':
            print(time.asctime(time.localtime(time.time())), "当前处于在线状态。")
            return True
        else:
            print(time.asctime(time.localtime(time.time())), "当前已经下线，正在尝试登录！")
            return False
    except Exception as e:
        # 异常处理，打印错误信息
        print(f"检查WiFi连接状态时发生错误: {e}")
        return False

# 锐捷认证登录
def login_ruijie(session, username, password, login_url, dataLogin):
    """
    尝试使用给定的用户名和密码通过锐捷认证系统登录。
    
    参数:
    - session: 请求的会话对象，用于维持会话状态。
    - username: 用户名。
    - password: 密码。
    - login_url: 登录接口的URL。
    - dataLogin: 登录所需的数据字典。
    
    返回:
    - 成功登录后返回True，否则返回False。
    """
    try:
        # 发送POST请求到登录URL
        response = session.post(login_url, headers=headers, data=dataLogin)
        # 设置响应编码为utf-8
        response.encoding = 'utf-8'
        # 处理响应内容，使其可读
        content = str(response.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode())
        # 查找结果标记
        j = content.find('"result":"')
        
        # 根据服务器响应判断登录是否成功
        if content[j + 10 + 17] == 'success':
            # 登录成功时打印成功信息并返回True
            print(time.asctime(time.localtime(time.time())), "登录成功！")
            return True
        else:
            # 登录失败时打印错误信息并返回False
            print("登录失败，服务器返回错误信息：", content[j + 10:j + 17])
            return False
    except Exception as e:
        # 发生异常时打印错误信息并返回False
        print(f"发生错误: {e}")
        return False

# 检查WiFi是否已连接
def wifi_connected():
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "已连接" in result.stdout:
        print("Wi-Fi已连接\n")
        return True
    return False

# 开始连接
def start_connect(auth_url, username, password,checkStatus, dataCheck):
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

    start_connect(auth_url, username, password,checkStatus, dataCheck)

if __name__ == '__main__':
    main()
