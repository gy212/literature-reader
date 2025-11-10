@echo off
echo ====================================
echo 检查Git状态
echo ====================================
echo.
git status
echo.
echo ====================================
echo 最近的提交记录
echo ====================================
echo.
git log --oneline -3
echo.
echo ====================================
echo 远程仓库信息
echo ====================================
echo.
git remote -v
echo.
pause

