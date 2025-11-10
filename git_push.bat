@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ====================================
echo 正在推送到GitHub
echo ====================================
echo.

echo [1/4] 添加所有更改...
git add -A
if %errorlevel% neq 0 (
    echo 错误: 添加文件失败
    pause
    exit /b 1
)
echo ✓ 文件已添加
echo.

echo [2/4] 检查状态...
git status --short
echo.

echo [3/4] 提交更改...
git commit -m "feat: 添加全文显示全屏功能、分批翻译和双栏对照视图，删除临时脚本文件"
if %errorlevel% neq 0 (
    echo 警告: 提交可能失败或没有更改需要提交
)
echo.

echo [4/4] 推送到GitHub...
git push origin main
if %errorlevel% equ 0 (
    echo.
    echo ====================================
    echo ✓ 推送成功！
    echo ====================================
) else (
    echo.
    echo ====================================
    echo ✗ 推送失败，请检查网络连接和GitHub认证
    echo ====================================
)
echo.
pause

