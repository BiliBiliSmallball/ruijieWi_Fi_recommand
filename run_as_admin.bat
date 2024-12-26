@echo off
echo 请确认是否已经关闭main.py
:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 请以管理员身份运行此脚本
    pause
    exit
)

:: 获取当前脚本所在目录
cd /d "%~dp0"

:: 确认main.py是否已经停止运行
:confirm
echo 是否已经停止运行main.py? (Y/N)
choice /c YN /n
if errorlevel 2 (
    echo 请先停止运行main.py
    pause
    goto confirm
)

:: 以管理员身份运行Python脚本
python "cyber_rescue.py"

pause