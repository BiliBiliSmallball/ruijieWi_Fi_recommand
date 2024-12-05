import subprocess
import time

# 运行次数统计
reconnect_count = 0

def is_wifi_connected():
    try:
        # 检查Wi-Fi是否连接
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "已连接" in result.stdout:
            return True
        return False
    except KeyError as e:
        print(f"KeyError: {e}")
        return False

def connect_to_wifi(ssid):
    try:
        # 连接到指定的Wi-Fi网络
        subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}'])
    except KeyError as e:
        print(f"KeyError: {e}")

def main():
    global reconnect_count
    ssid = 'gtxy_wifi'  # 替换为你的Wi-Fi网络名称

    while True:
        t = time.localtime()
        if 2 <= t.tm_hour < 10:
            sleep_time = 1200  # 夜间每20分钟检测一次
        else:
            sleep_time = 30  # 白天每30秒检测一次

        if not is_wifi_connected():
            print("Wi-Fi is disconnected. Attempting to reconnect...")
            connect_to_wifi(ssid)
            time.sleep(5)  # 等待一段时间，让系统尝试连接
            if is_wifi_connected():
                print("Reconnected successfully.")
                reconnect_count += 1
            else:
                print("Failed to reconnect.")
        else:
            print("Wi-Fi is connected.")
        
        print(f"Reconnection attempts: {reconnect_count}\n")
        print(f"运行时间：{t.tm_hour}：{t.tm_min}：{t.tm_sec}\n")
        time.sleep(sleep_time)  # 根据时间调整检测频率

try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt as reason:
    print("结束运行。")

