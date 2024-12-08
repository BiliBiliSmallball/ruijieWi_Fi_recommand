import subprocess
def is_process_running(process_name):
    result = subprocess.run(['tasklist'], stdout=subprocess.PIPE, text=True)
    return process_name in result.stdout

def start_process(process_name):
    if is_process_running(process_name):
        print(f"{process_name} is running.")
    else:
        print(f"{process_name} is not running.")