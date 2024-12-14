@echo off
:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 请以管理员身份运行此脚本
    pause
    exit
)

:: 获取当前脚本所在目录
cd /d "%~dp0"

:: 以管理员身份运行Python脚本
python "cyber_rescue.py"
pause
