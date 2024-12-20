import subprocess
import time
import clash_monitor as clash
import log_config

# 定义常量
LOG_CLEAR_THRESHOLD = 600
LOG_FILE = "wifi_reconnect_log.txt"
ERR_LOG_FILE = "./err_log.txt"
SSID = 'gtxy_wifi'  # 替换为你的Wi-Fi网络名称
GATEWAY_IP = '192.168.1.1'  # 替换为你指定的网关IP地址

def is_wifi_connected():
    # 检查Wi-Fi是否连接
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "已连接" in result.stdout:
        return True
    return False

def ping_gateway():
    # 检查是否能ping通指定网关
    result = subprocess.run(['ping', GATEWAY_IP, '-n', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "TTL=" in result.stdout:
        return True
    return False

def disconnect_ethernet():
    # 断开指定有线网网关
    subprocess.run(['netsh', 'interface', 'set', 'interface', 'Ethernet', 'admin=disable'])

def connect_ethernet():
    # 重新连接有线网
    subprocess.run(['netsh', 'interface', 'set', 'interface', 'Ethernet', 'admin=enable'])

def close_network_software():
    # 关闭网络连接软件（假设软件名为network_software.exe）
    subprocess.run(['taskkill', '/F', '/IM', 'network_software.exe'])

def open_network_software():
    # 重新打开网络连接软件（假设软件路径为C:\Program Files\network_software\network_software.exe）
    subprocess.run(['start', 'C:\\Program Files\\network_software\\network_software.exe'])

def connect_to_wifi(ssid):
    # 连接到指定的Wi-Fi网络
    subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}'])

def login_to_network():
    # 登入指定网络并提交表单数据（假设使用requests库）
    import requests
    login_url = 'http://example.com/login'  # 替换为你的登录URL
    login_data = {
        'username': 'your_username',  # 替换为你的用户名
        'password': 'your_password'   # 替换为你的密码
    }
    requests.post(login_url, data=login_data)

def is_clash_running():
    if clash.test_process("clash-verge.exe"):
        log_config.log_message(0, "clash is running", open(LOG_FILE, "a"))
        return True
    else:
        log_config.log_message(1, "clash is not running", open(LOG_FILE, "a"))
        return False

def main():
    reconnect_count = 0
    run_count = 0
    log_clear_count = log_config.log_clear_tic_get(ERR_LOG_FILE)

    while True:
        # 日志时间判断
        t = time.localtime()
        sleep_time = 10 if 14 <= t.tm_hour <= 2 else 1200

        # 核心
        if not is_wifi_connected() or not ping_gateway():
            print("Wi-Fi已断开连接或无法ping通网关，尝试重新连接...")
            disconnect_ethernet()
            close_network_software()
            connect_to_wifi(SSID)
            time.sleep(5)
            if is_wifi_connected():
                login_to_network()
                connect_ethernet()
                open_network_software()
                print("重新连接成功。")
                reconnect_count += 1
                log_config.log_message(1, f"Automatic reconnect successful. Reconnect count: {reconnect_count}", open(LOG_FILE, "a"))
            else:
                print("重新连接失败。")
                log_config.log_message(1, "Automatic reconnect failed.", open(LOG_FILE, "a"))
        else:
            print("Wi-Fi已连接且网关可达。")
            log_config.log_message(0, "Wi-Fi is connected and gateway is reachable", open(LOG_FILE, "a"))

        run_count += 1
        log_config.log_message(0, f"Run count: {run_count}", open(LOG_FILE, "a"))

        if run_count % 3 == 0:
            if not is_clash_running():
                clash.start_process("C:\\Program Files\\Clash Verge\\clash-verge.exe")

        # 显示
        print(f"重连次数: {reconnect_count}\n")
        print(f"运行次数: {run_count}\n")
        print(f"运行时间: {t.tm_hour}:{t.tm_min}:{t.tm_sec}\n")

        # 日志清理
        if run_count > LOG_CLEAR_THRESHOLD:
            log_config.log_delet(LOG_FILE, ERR_LOG_FILE, log_clear_count)
            log_clear_count += 1
            run_count = 0  # 重置运行次数

        time.sleep(sleep_time)

if __name__ == "__main__":
    print("启动Wi-Fi重连服务。按Ctrl+C退出。")
    try:
        main()
    except KeyboardInterrupt:
        print("\n停止服务")
        log_config.log_message(1, "The script is terminated by the user\n---------------------------------------", open(LOG_FILE, "a"))
    except Exception as e:
        print(f"\n未知错误: {e}")
        log_config.log_message(1, f"Unknown error: {e}\n---------------------------------------", open(LOG_FILE, "a"))