import subprocess 

def is_process_running(process_name): 
    result = subprocess.run(['tasklist'], stdout=subprocess.PIPE, text=True) 
    return process_name in result.stdout 
def test_process(process_name): 
    if is_process_running(process_name): 
        print(f"{process_name} 正在运行。")
        return True 
    else: 
        print(f"{process_name} 未运行。")
        return False 
    
if __name__ == "__main__": 
    process_name = "clash-verge.exe"
    test_process(process_name)  # 确保进程名称与任务列表中显示的完全一致
    test_process('clash-verge-service.exe') 
    
    input("按下Enter键退出")
