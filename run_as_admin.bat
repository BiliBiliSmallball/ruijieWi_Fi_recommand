net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 请以管理员身份运行此脚本
    pause
    exit
)

:: 获取当前脚本所在目录
cd /d "%~dp0"

:: 检测main.py是否正在运行
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "main.py" >NUL
if %errorlevel% equ 0 (
    echo main.py 正在运行。
) else (
    echo main.py 未运行。
)

:: 确认main.py是否已经停止运行
:confirm_main
echo 是否已经停止运行main.py? (Y/N)
choice /c YN /n
if errorlevel 2 (
    echo 请先停止运行main.py
    pause
    goto confirm_main
)

:: 检测zerotier是否正在运行
tasklist /FI "IMAGENAME eq zerotier.exe" 2>NUL | find /I "zerotier" >NUL
if %errorlevel% equ 0 (
    echo zerotier 正在运行。
) else (
    echo zerotier 未运行。
)

:: 确认zerotier是否已经停止运行
:confirm_zerotier
echo 是否已经停止运行zerotier等类似软件? (Y/N)
choice /c YN /n
if errorlevel 2 (
    echo 请先停止运行zerotier等类似软件
    pause
    goto confirm_zerotier
)

:: 以管理员身份运行Python脚本
python "cyber_rescue.py"

pause