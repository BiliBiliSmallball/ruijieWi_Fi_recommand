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

def check_ping(ip, count=1, timeout=1000):
    """
    检查IP地址的连通性。

    参数:
    ip (str): 需要检查的IP地址。
    count (int, optional): 发送ping请求的次数。默认为1次。
    timeout (int, optional): 每次ping请求的超时时间（毫秒）。默认为1000毫秒。

    返回:
    str: 如果ping命令执行成功（返回值为0），则返回'ok'，否则返回'failed'。
    """
    # 构建ping命令，'-n'指定发送ping的次数，'-w'指定每次ping的超时时间，'NUL'用于忽略ping命令的输出
    cmd = 'ping -n %d -w %d %s > NUL' % (count, timeout, ip)
    # 执行ping命令，返回值为0表示成功，非0表示失败
    res = os.system(cmd)
    # 根据ping命令的返回值判断连通性并返回相应状态字符串
    return 'ok' if res == 0 else 'failed'

# 锐捷认证登录
def login_ruijie(session, username, password, login_url):
    # 获取登录页面以提取可能的隐藏字段（如 CSRF Token）
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取隐藏字段
    hidden_fields = {}
    for input_tag in soup.find_all('input', type='hidden'):
        hidden_fields[input_tag['name']] = input_tag.get('value', '')

    # 表单数据，包括用户名和密码以及其他可能需要的隐藏字段
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
        # 发送POST请求进行登录
        response = session.post(login_url, data=data)

        if response.status_code == 200:
            # 尝试获取登录结果
            query_url = "http://10.30.12.10:30004/byod/byodrs/login/queryResult"
            query_response = session.get(query_url)
            
            # 检查返回的JSON数据
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

# 检查WiFi连接状态
def check_wifi_status():
    wifi_status = os.popen('netsh wlan show interfaces').read()
    if check_ping("10.60.0.1") == "ok":
        return True
    else:
        return False

# 开始连接过程
def start_connect(auth_url, username, password, ssid):
    manage_ethernet("disconnect")
    time.sleep(5)
    
    session = requests.Session()
    while not check_wifi_status():
        if login_ruijie(session, username, password, auth_url):
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
