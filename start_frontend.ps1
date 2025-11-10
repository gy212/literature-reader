# 启动前端服务脚本
Write-Host "===================================" -ForegroundColor Green
Write-Host "启动React前端服务" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host ""

# 检查Node.js
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: 未找到Node.js，请先安装Node.js 18+" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "Node.js版本: $nodeVersion" -ForegroundColor Cyan

# 检查是否在项目根目录
if (-not (Test-Path client)) {
    Write-Host "错误: 未找到client目录，请在项目根目录运行此脚本" -ForegroundColor Red
    pause
    exit 1
}

# 检查依赖
Write-Host "检查依赖..." -ForegroundColor Yellow
if (-not (Test-Path client/node_modules)) {
    Write-Host "警告: node_modules不存在，正在安装依赖..." -ForegroundColor Yellow
    Set-Location client
    npm install
    Set-Location ..
}

# 启动服务
Write-Host "正在启动React前端..." -ForegroundColor Green
Write-Host "服务地址: http://localhost:3000" -ForegroundColor Cyan
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

Set-Location client
npm run dev

