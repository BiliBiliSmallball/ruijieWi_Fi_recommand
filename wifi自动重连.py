import subprocess
import time
import os

# 运行次数统计
reconnect_count = 0
run_count = 0

def is_wifi_connected():
    # 检查Wi-Fi是否连接
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "已连接" in result.stdout:
        return True
    return False

def connect_to_wifi(ssid):
    # 连接到指定的Wi-Fi网络
    subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}'])

def log_message(message):
    # 将消息记录到日志文件
    with open("wifi_reconnect_log.txt", "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def manual_check():
    input("按Enter进行手动检测Wi-Fi连接...")
    if not is_wifi_connected():
        print("Wi-Fi is disconnected. Attempting to reconnect...")
        connect_to_wifi(ssid)
        time.sleep(5)  # 等待一段时间，让系统尝试连接
        if is_wifi_connected():
            print("Reconnected successfully.")
            reconnect_count += 1
            log_message(f"Manual reconnect successful. Reconnect count: {reconnect_count}")
        else:
            print("Failed to reconnect.")
            log_message("Manual reconnect failed.")
    else:
        print("Wi-Fi is connected.")

def main():
    global reconnect_count, run_count
    ssid = 'gtxy_wifi'  # 替换为你的Wi-Fi网络名称

    while True:
        t = time.localtime()
        if 16 <= t.tm_hour or t.tm_hour <= 2:
            sleep_time = 10  # 夜间每10秒检测一次
        else:
            sleep_time = 1200  # 白天每20分钟检测一次

        if not is_wifi_connected():
            print("Wi-Fi is disconnected. Attempting to reconnect...")
            connect_to_wifi(ssid)
            time.sleep(5)  # 等待一段时间，让系统尝试连接
            if is_wifi_connected():
                print("Reconnected successfully.")
                reconnect_count += 1
                log_message(f"Automatic reconnect successful. Reconnect count: {reconnect_count}")
            else:
                print("Failed to reconnect.")
                log_message("Automatic reconnect failed.")
        else:
            print("Wi-Fi is connected.")
            log_message("Wi-Fi is connected.")

        run_count += 1
        log_message(f"Run count: {run_count}")

        print(f"重连次数: {reconnect_count}\n")
        print(f"运行次数: {run_count}\n")
        
        print(f"运行时间：{t.tm_hour}：{t.tm_min}：{t.tm_sec}\n")
        time.sleep(sleep_time)  # 根据时间调整检测频率
        #manual_check()  # 手动检测功能

if __name__ == "__main__":
    print("Starting Wi-Fi reconnection service. press Ctrl+C to exit.")
    try:
        main()
    except KeyboardInterrupt:
        print("\n服务截止")
        log_message("Script terminated by user.\n---------------------------------------")
