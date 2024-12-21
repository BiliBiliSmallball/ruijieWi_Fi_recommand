"""
-*- coding: utf-8 -*-
@Time    : 2024/12/11 19:51
@File    : log_config.py
@autor   : Ender_Zhu
@Software: vscode
@Desc    :日志配置模块

该模块主要用于处理程序运行过程中的日志记录，包括正常日志和错误日志的记录与管理。
主要功能包括：
- 将日志消息记录到指定的日志文件中。
- 处理错误日志，将其从普通日志文件中分离并记录到单独的错误日志文件中。 
"""
import os
import time

def log_conuter(log_file_path: str):
    """获取日志文件行数
    Args: 
    log_file_path (str): 日志文件的路径
    Returns: 
    int: 日志文件的行数
    """
    with open(log_file_path, "r") as log_file:
        tic = (len(log_file.readlines())-1) // 2
        
    return tic

def ensure_log_file_exists(log_file_path: str):
    """确保日志文件存在"""
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w") as log_file:
            log_file.write("")

def log_message(level: bool, message: str, log_file_path: str, script_name: str):
    """将消息记录到日志文件 
    Args: level (bool): 日志等级：0为正常，1为警告 
    message (str):写入日志的信息 
    log_file_path (str): 文件路径，默认为log.txt 
    script_name (str): 脚本名称
    """ 
    ensure_log_file_exists(log_file_path)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S') 
    log_entry = f"{timestamp} - {script_name} [{'warning' if level else 'info'}] {message}\n" 

    try:
        with open(log_file_path, "a") as log_file:
            log_file.write(log_entry)
    except PermissionError as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def err_dispose(log_path: str, err_log_path: str, clear_count: int): 
    """错误日志处理函数，将错误日志写入到单独的文件中，并删除原始日志文件
    Args: 
    log_path (str): 原始日志文件路径 
    err_log_path (str): 错误日志输出文件路径 
    clear_count (int): 日志已被清理的次数 
    """
    ensure_log_file_exists(err_log_path)
    with open(log_path, "r") as log_file, open(err_log_path, "a") as err_log: 
        for line in log_file: 
            if '[warning]' in line: 
                err_log.write(line) 
        err_log.write(f"------Error logged {clear_count} time--------\n")
         
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
    log_message(1, f"Log cleared automatically. Log clear count: {clear_count}", log_file_path, __file__)

def log_clear_tic_get(err_log_path: str):
    """获取日志清理计数
    Returns: 
    int: 日志已被清理的次数
    """
    try:
        return_tic = 0
        with open(err_log_path, "r") as tic_file:
            for line in tic_file:
                if "Error logged" in line: 
                    return_tic += 1
        
        print(f"\nLog clear count: {return_tic}\n")
    except FileNotFoundError as reason:
        print(f"Error: {reason}")
    
    return return_tic

if __name__ == "__main__":
    log_conuter("wifi_reconnect_log.txt")