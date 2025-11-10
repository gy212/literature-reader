# 启动后端服务脚本
Write-Host "===================================" -ForegroundColor Green
Write-Host "启动Flask后端服务" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host ""

# 检查Python
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: 未找到Python，请先安装Python 3.9+" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "Python版本: $pythonVersion" -ForegroundColor Cyan

# 检查依赖
Write-Host "检查依赖..." -ForegroundColor Yellow
$flaskInstalled = pip show Flask 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: Flask未安装，请先运行: pip install -r requirements.txt" -ForegroundColor Red
    pause
    exit 1
}

# 检查.env文件
if (-not (Test-Path .env)) {
    Write-Host "警告: .env文件不存在，将使用默认配置" -ForegroundColor Yellow
    Write-Host "建议创建.env文件并配置API密钥" -ForegroundColor Yellow
    Write-Host ""
}

# 启动服务
Write-Host "正在启动Flask后端..." -ForegroundColor Green
Write-Host "服务地址: http://localhost:5000" -ForegroundColor Cyan
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

python server/main.py

