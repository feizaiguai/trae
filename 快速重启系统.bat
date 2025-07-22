@echo off
chcp 65001 >nul
echo ========================================
echo      智能快速重启系统工具 v2.0
echo ========================================
echo.
echo 正在检查重要工作文件并自动保存...
echo.

REM 检测并保存重要工作文件
echo [检测] 正在扫描重要工作程序...

REM 检测Office程序并尝试保存
set office_found=0
tasklist /fi "imagename eq winword.exe" 2>nul | find /i "winword.exe" >nul
if not errorlevel 1 (
    echo [发现] Microsoft Word 正在运行，尝试自动保存...
    set office_found=1
    REM 发送Ctrl+S保存快捷键到Word
    powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^s')"
    timeout /t 2 /nobreak >nul
)

tasklist /fi "imagename eq excel.exe" 2>nul | find /i "excel.exe" >nul
if not errorlevel 1 (
    echo [发现] Microsoft Excel 正在运行，尝试自动保存...
    set office_found=1
    powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^s')"
    timeout /t 2 /nobreak >nul
)

tasklist /fi "imagename eq powerpnt.exe" 2>nul | find /i "powerpnt.exe" >nul
if not errorlevel 1 (
    echo [发现] Microsoft PowerPoint 正在运行，尝试自动保存...
    set office_found=1
    powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^s')"
    timeout /t 2 /nobreak >nul
)

REM 检测代码编辑器并尝试保存
set editor_found=0
tasklist /fi "imagename eq code.exe" 2>nul | find /i "code.exe" >nul
if not errorlevel 1 (
    echo [发现] Visual Studio Code 正在运行，尝试自动保存...
    set editor_found=1
    powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^s')"
    timeout /t 2 /nobreak >nul
)

tasklist /fi "imagename eq notepad++.exe" 2>nul | find /i "notepad++.exe" >nul
if not errorlevel 1 (
    echo [发现] Notepad++ 正在运行，尝试自动保存...
    set editor_found=1
    powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^s')"
    timeout /t 2 /nobreak >nul
)

tasklist /fi "imagename eq devenv.exe" 2>nul | find /i "devenv.exe" >nul
if not errorlevel 1 (
    echo [发现] Visual Studio 正在运行，尝试自动保存...
    set editor_found=1
    powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^s')"
    timeout /t 2 /nobreak >nul
)

tasklist /fi "imagename eq idea64.exe" 2>nul | find /i "idea64.exe" >nul
if not errorlevel 1 (
    echo [发现] IntelliJ IDEA 正在运行，尝试自动保存...
    set editor_found=1
    powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^s')"
    timeout /t 2 /nobreak >nul
)

REM 检测其他重要程序
tasklist /fi "imagename eq photoshop.exe" 2>nul | find /i "photoshop.exe" >nul
if not errorlevel 1 (
    echo [发现] Adobe Photoshop 正在运行，尝试自动保存...
    powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('^s')"
    timeout /t 2 /nobreak >nul
)

if %office_found%==1 echo [完成] Office 文档保存完成
if %editor_found%==1 echo [完成] 代码文件保存完成

echo.
echo 文件保存检查完成，开始关闭程序...
echo.

REM 强制关闭常见的可能影响重启的程序
echo [1/8] 关闭浏览器进程...
taskkill /f /im chrome.exe >nul 2>&1
taskkill /f /im firefox.exe >nul 2>&1
taskkill /f /im msedge.exe >nul 2>&1
taskkill /f /im opera.exe >nul 2>&1

echo [2/9] 温和关闭办公软件...
REM 先尝试温和关闭，给程序时间保存
taskkill /im winword.exe >nul 2>&1
taskkill /im excel.exe >nul 2>&1
taskkill /im powerpnt.exe >nul 2>&1
taskkill /im outlook.exe >nul 2>&1
timeout /t 3 /nobreak >nul
REM 如果还在运行则强制关闭
taskkill /f /im winword.exe >nul 2>&1
taskkill /f /im excel.exe >nul 2>&1
taskkill /f /im powerpnt.exe >nul 2>&1
taskkill /f /im outlook.exe >nul 2>&1

echo [3/9] 关闭媒体播放器...
taskkill /f /im vlc.exe >nul 2>&1
taskkill /f /im wmplayer.exe >nul 2>&1
taskkill /f /im potplayer.exe >nul 2>&1

echo [4/9] 关闭下载工具...
taskkill /f /im thunder.exe >nul 2>&1
taskkill /f /im utorrent.exe >nul 2>&1
taskkill /f /im qbittorrent.exe >nul 2>&1

echo [5/9] 关闭游戏平台...
taskkill /f /im steam.exe >nul 2>&1
taskkill /f /im epicgameslauncher.exe >nul 2>&1
taskkill /f /im origin.exe >nul 2>&1

echo [6/9] 关闭虚拟机软件...
taskkill /f /im vmware.exe >nul 2>&1
taskkill /f /im virtualbox.exe >nul 2>&1

echo [7/9] 关闭数据库服务...
net stop mysql >nul 2>&1
net stop postgresql >nul 2>&1
net stop mongodb >nul 2>&1

echo [8/9] 温和关闭开发工具...
REM 先尝试温和关闭开发工具
taskkill /im notepad++.exe >nul 2>&1
taskkill /im code.exe >nul 2>&1
taskkill /im devenv.exe >nul 2>&1
taskkill /im idea64.exe >nul 2>&1
timeout /t 3 /nobreak >nul
REM 强制关闭仍在运行的开发工具
taskkill /f /im notepad++.exe >nul 2>&1
taskkill /f /im code.exe >nul 2>&1
taskkill /f /im devenv.exe >nul 2>&1
taskkill /f /im idea64.exe >nul 2>&1

echo [9/9] 关闭其他设计软件...
taskkill /f /im photoshop.exe >nul 2>&1
taskkill /f /im illustrator.exe >nul 2>&1
taskkill /f /im afterfx.exe >nul 2>&1
taskkill /f /im premiere.exe >nul 2>&1

echo.
echo 程序关闭完成！
echo.
echo 所有重要文件已保存，程序已安全关闭！
echo 等待5秒后开始重启系统...
echo 如需取消重启，请按 Ctrl+C
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo           正在重启系统...
echo ========================================
echo.

REM 强制立即重启系统（不等待程序响应）
shutdown /r /f /t 0

REM 如果上面的命令失败，尝试备用方法
if errorlevel 1 (
    echo 尝试备用重启方法...
    wmic os where Primary=TRUE call Reboot
)

REM 如果还是失败，显示错误信息
if errorlevel 1 (
    echo.
    echo 错误：无法重启系统，请检查管理员权限！
    echo 请右键以管理员身份运行此批处理文件。
    pause
)