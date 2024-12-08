"""
-*- coding: utf-8 -*-
@Time    : 2023/7/27 15:07
@File    : wifi自动重连.py
@autor   : Ender_Zhu
@Software: vscode
@Desc    : 程序的主函数，wifi自动重连，检测的脚本。
"""
import subprocess
import time
import os

# 运行次数统计
reconnect_count = 0
run_count = 0
log_delet_tic = 0  # 日志清除次数

def is_wifi_connected():
    # 检查Wi-Fi是否连接
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "已连接" in result.stdout:
        return True
    return False

def connect_to_wifi(ssid):
    # 连接到指定的Wi-Fi网络
    subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}'])

def log_message(level, message):
    # 将消息记录到日志文件
    with open("wifi_reconnect_log.txt", "a") as log_file:
        if level == 0:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        else:
            log_file.write(f"[warning] {time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def err_dispose(log_path):
    # 逐行读取日志，在提取其中错误的加入err_log.txt中，并清除当前日志内容
    with open(log_path, "r") as log_file:
        lines = log_file.readlines()
    with open("./err_log.txt", "a") as err_log:
        for line in lines:
            if '[warning]' in line:
                err_log.write(line)

def log_delet():
    # 清空日志
    global log_delet_tic
    if run_count > 2000:
        err_dispose("wifi_reconnect_log.txt")  # 在清空之前处理日志
        with open("wifi_reconnect_log.txt", "w") as log_file:
            log_file.write("")
        log_delet_tic += 1
        log_message(1, f"Log cleared automatically. Log clear count: {log_delet_tic}")

async def manual_check():
    """
    本函数原先是为了进行手动触发检测，现在作废
    """ 
    pass

def main():
    global reconnect_count, run_count
    ssid = 'gtxy_wifi'  # 替换为你的Wi-Fi网络名称

    while True:
        t = time.localtime()
        sleep_time = 10  # 测试每10秒检测一次
        # if 15 <= t.tm_hour or t.tm_hour <= 2:
        #     sleep_time = 10  # 夜间每10秒检测一次
        # else:
        #     sleep_time = 1200  # 白天每20分钟检测一次

        if not is_wifi_connected():
            print("Wi-Fi is disconnected. Attempting to reconnect...")
            connect_to_wifi(ssid)
            time.sleep(5)  # 等待一段时间，让系统尝试连接
            if is_wifi_connected():
                print("Reconnected successfully.")
                reconnect_count += 1
                log_message(1, f"Automatic reconnect successful. Reconnect count: {reconnect_count}")
            else:
                print("Failed to reconnect.")
                log_message(1, "Automatic reconnect failed.")
        else:
            print("Wi-Fi is connected.")
            log_message(0, "Wi-Fi is connected.")

        run_count += 1
        log_message(0, f"Run count: {run_count}")

        print(f"重连次数: {reconnect_count}\n")
        print(f"运行次数: {run_count}\n")
        print(f"运行时间：{t.tm_hour}：{t.tm_min}：{t.tm_sec}\n")

        log_delet()
        time.sleep(sleep_time)  # 根据时间调整检测频率

if __name__ == "__main__":
    print("Starting Wi-Fi reconnection service. press Ctrl+C to exit.")
    try:
        main()
    except KeyboardInterrupt:
        print("\n服务截止")
        log_message(1, "Script terminated by user.\n---------------------------------------")
