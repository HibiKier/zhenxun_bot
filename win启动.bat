


:: 检查是否传入了端口号
if "%~1"=="" (
    echo 未传入端口号，跳过杀死进程操作。
    goto END
)

:: 获取传入的端口号
set PORT=%~1

:: 查找并杀死所有占用端口的进程
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r /c:"^ *[^ ]*:%PORT% " /c:"^ *[^ ]*:%PORT%$"') do (
    echo 正在杀死占用端口 %PORT% 的进程，PID: %%a
    taskkill /PID %%a /F
)

:END

:: 获取当前批处理文件所在的目录
set BAT_DIR=%~dp0

:: 设置 Python 可执行文件的完整路径
set PYTHON_EXE="%BAT_DIR%Python311\python.exe"

:: 检查 python.exe 是否存在
if not exist %PYTHON_EXE% (
    echo 错误：未找到 Python 可执行文件！
    echo 请确保 Python311 文件夹位于批处理文件所在目录中。
    pause
    exit /b 1
)

:: 使用指定的 Python 安装 Playwright 的 Chromium
echo start install Playwright 的 Chromium...
%PYTHON_EXE% -m playwright install chromium

:: 使用当前目录中的 python.exe 运行 bot.py
echo 正在启动 bot.py...
%PYTHON_EXE%  bot.py

:: 如果脚本运行完毕，暂停以便查看输出
pause