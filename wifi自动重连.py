"""
-*- coding: utf-8 -*-
@Time    : 2024/12/09 10:38
@File    : wifi自动重连.py
@autor   : Ender_Zhu
@Software: vscode
@Desc    : 程序的主函数，wifi自动重连，检测的脚本。
"""
import subprocess
import time
import clash_monitor as clash

# 定义常量 
LOG_FILE = "wifi_reconnect_log.txt" 
ERR_LOG_FILE = "./err_log.txt" 
LOG_CLEAR_THRESHOLD = 1200
 
def is_wifi_connected(): 
    # 检查Wi-Fi是否连接 
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) 
    if "已连接" in result.stdout: 
        return True 
    return False 
def connect_to_wifi(ssid): 
    # 连接到指定的Wi-Fi网络 
    subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}'])

def log_message(level: bool, message: str, log_file: str):
    """将消息记录到日志文件 
    Args: level (bool): 日志等级：0为正常，1为警告 
    message (str):写入日志的信息 
    log_file (str): 文件路径，默认为log.txt 
    """ 
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S') 
    log_entry = f"{timestamp} - {message}\n" 
    if level == 0: 
        log_file.write(log_entry) 
    else: 
        log_file.write(f"[warning] {log_entry}") 

def err_dispose(log_path: str, err_log_path: str, clear_count: int): 
    """错误日志处理函数，将错误日志写入到单独的文件中，并删除原始日志文件
    Args: 
    log_path (str): 原始日志文件路径 
    err_log_path (str): 错误日志输出文件路径 
    clear_count (int): 日志已被清理的次数 
    """
    with open(log_path, "r") as log_file, open(err_log_path, "a") as err_log: 
        for line in log_file: 
            if '[warning]' in line: 
                err_log.write(line) 
        err_log.write(f"------Error logged {clear_count} time--------\n")  

def is_clash_running():
    if clash.test_process("clash-verge.exe"):
        log_message(0, "clash is running", open(LOG_FILE, "a"))
        return True
    else: 
        log_message(1, "clash is not running", open(LOG_FILE, "a"))
        return False 
def log_delet(log_file_path: str, err_log_path: str, clear_count: int): 
    """ 根据日志清理计数决定是否清理日志文件。
    参数: 
    log_file_path (str): 日志文件的路径。 
    err_log_path (str): 错误日志文件的路径。 
    clear_count (int): 日志已被清理的次数。 
    """ 
    err_dispose(log_file_path, err_log_path, clear_count)
    with open(log_file_path, "w") as log_file: 
        pass # 清空文件 
    log_message(1, f"Log cleared automatically. Log clear count: {clear_count}", open(log_file_path, "a"))

    
def main(ssid: str): 
    reconnect_count = 0 
    run_count = 0 
    log_clear_count = 1
     
    while True: 
        #日志时间判断
        t = time.localtime() 
        sleep_time = 10 if 15 <= t.tm_hour or t.tm_hour <= 2 else 1200
        
        #核心
        if not is_wifi_connected(): 
            print("Wi-Fi已断开连接，尝试重新连接...") 
            connect_to_wifi(ssid) 
            time.sleep(5) 
            if is_wifi_connected(): 
                print("重新连接成功。") 
                reconnect_count += 1 
                log_message(1, f"Automatic reconnect successful. Reconnect count: {reconnect_count}", open(LOG_FILE, "a")) 
            else:
                print("重新连接失败。") 
                log_message(1, "Automatic reconnect failed.", open(LOG_FILE, "a"))
        else: 
            print("Wi-Fi已连接。") 
            log_message(0, "Wi-Fi is connection", open(LOG_FILE, "a")) 
        
        run_count += 1 
        log_message(0, f"Run count: {run_count}", open(LOG_FILE, "a"))
        
        if run_count % 3 == 0:
            if not is_clash_running():
                clash.start_process("clash-verge.exe")
        
        #显示
        print(f"重连次数: {reconnect_count}\n") 
        print(f"运行次数: {run_count}\n") 
        print(f"运行时间: {t.tm_hour}:{t.tm_min}:{t.tm_sec}\n") 
        
        #日志清理
        if run_count >= LOG_CLEAR_THRESHOLD: 
            log_delet(LOG_FILE, ERR_LOG_FILE, log_clear_count) 
            log_clear_count += 1
            run_count = 0 # 重置运行次数 
            
        time.sleep(sleep_time) 


if __name__ == "__main__": 
    print("启动Wi-Fi重连服务。按Ctrl+C退出。") 
    ssid = 'gtxy_wifi' # 替换为你的Wi-Fi网络名称 
    try: 
        main(ssid) 
    except KeyboardInterrupt:
        print("\n停止服务") 
        log_message(1, "用户终止脚本。\n---------------------------------------", open(LOG_FILE, "a"))