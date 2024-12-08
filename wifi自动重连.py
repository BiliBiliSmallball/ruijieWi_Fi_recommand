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

# 定义常量
LOG_FILE = "wifi_reconnect_log.txt"
ERR_LOG_FILE = "./err_log.txt"
LOG_CLEAR_THRESHOLD = 2000

def is_wifi_connected():
    # 检查Wi-Fi是否连接
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "已连接" in result.stdout:
        return True
    return False

def connect_to_wifi(ssid):
    # 连接到指定的Wi-Fi网络
    subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}'])

def log_message(level:bool, message:str,log_file:str):
    """将消息记录到日志文件

    Args:
        level (bool): 日志等级：0为正常，1为警告
        message (str):写入日志的信息
        log_file (str): 文件路径，默认为log.txt
    """  
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {message}\n"
    if level == 0:
        log_file.write(log_entry)
    else:
        log_file.write(f"[warning] {log_entry}")

def err_dispose(log_path:str, err_log_path:str):
    """错误日志处理函数，将错误日志写入到单独的文件中，并删除原始日志文件
    Args:
        log_path (str): 原始日志文件路径
        err_log_path (str): 错误日志输出文件路径
    """
    with open(log_path, "r") as log_file, open(err_log_path, "a") as err_log:
        for line in log_file:
            if '[warning]' in line:
                err_log.write(line)
    os.remove(log_path)

def log_delet(log_file_path:str, err_log_path:str, log_clear_count:str):
    """
    根据日志清理计数决定是否清理日志文件。
    
    参数:
    log_file_path (str): 日志文件的路径。
    err_log_path (str): 错误日志文件的路径。
    log_clear_count (int): 日志已被清理的次数。
    """
    if log_clear_count > LOG_CLEAR_THRESHOLD:
        err_dispose(log_file_path, err_log_path)
        with open(log_file_path, "w") as log_file:
            pass  # 清空文件
        log_message(1, f"Log cleared automatically. Log clear count: {log_clear_count + 1}", open(log_file_path, "a"))


async def manual_check():
    """
    本函数原先是为了进行手动触发检测，现在作废
    """ 
    pass

def main(ssid):
    reconnect_count = 0# 运行次数统计
    run_count = 0
    log_delet_tic = 0  # 日志清除次数

    while True:
        t = time.localtime()

        if 15 <= t.tm_hour or t.tm_hour <= 2:
            sleep_time = 10
        else:
            sleep_time = 1200

        if not is_wifi_connected():
            print("Wi-Fi is disconnected. Attempting to reconnect...")
            connect_to_wifi(ssid)
            time.sleep(5)
            if is_wifi_connected():
                print("Reconnected successfully.")
                reconnect_count += 1
                log_message(0, f"Automatic reconnect successful. Reconnect count: {reconnect_count}", open(LOG_FILE, "a"))
            else:
                print("Failed to reconnect.")
                log_message(1, "Automatic reconnect failed.", open(LOG_FILE, "a"))
        else:
            print("Wi-Fi is connected.")
            log_message(0, "Wi-Fi is connected.", open(LOG_FILE, "a"))

        run_count += 1
        log_message(0, f"Run count: {run_count}", open(LOG_FILE, "a"))

        print(f"Reconnect count: {reconnect_count}\n")
        print(f"Run count: {run_count}\n")
        print(f"Run time: {t.tm_hour}:{t.tm_min}:{t.tm_sec}\n")

        log_delet(LOG_FILE, ERR_LOG_FILE, log_clear_count)
        log_clear_count += 1
        time.sleep(sleep_time)

if __name__ == "__main__":
    print("Starting Wi-Fi reconnection service. Press Ctrl+C to exit.")
    ssid = 'gtxy_wifi'  # 替换为你的Wi-Fi网络名称
    try:
        main(ssid)
    except KeyboardInterrupt:
        print("\n停止运行")
        log_message(1, "Script terminated by user.\n---------------------------------------", open(LOG_FILE, "a"))

