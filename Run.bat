@echo off 
:: 检查当前脚本是否在管理员权限下运行 
NET SESSION >nul 2>&1 
if %errorlevel% neq 0 ( 
    echo 错误: 该脚本需要管理员权限运行。请以管理员身份重新运行该脚本。 
    pause 
    exit /b 
) 
 
:: 如果已经有管理员权限，继续执行下面的命令 
:: 切换到批处理文件所在的目录 
cd /d "%~dp0" 
 
:: 获取当前目录的完整路径 
set SCRIPT_PATH=%cd%\updateHosts.py 
 
:: 检查文件是否存在 
if not exist "%SCRIPT_PATH%" ( 
    echo 错误: 找不到 Python 脚本文件 "%SCRIPT_PATH%" 
    pause 
    exit /b 
) 
 
echo 正在使用管理员权限运行 Python 脚本... 
python "%SCRIPT_PATH%"  :: 使用绝对路径运行 Python 脚本 
 
pause
