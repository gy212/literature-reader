# 🚀 项目启动指南

## 一、环境准备

### 1. Python环境（后端）

确保已安装 Python 3.9+：

```bash
python --version
# 或
python3 --version
```

### 2. Node.js环境（前端）

确保已安装 Node.js 18+：

```bash
node --version
npm --version
```

## 二、安装依赖

### 1. 安装后端依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 安装前端依赖

```bash
cd client
npm install
cd ..
```

## 三、配置环境变量

### 1. 复制环境变量模板

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 2. 编辑 `.env` 文件

打开 `.env` 文件，填入您的API密钥：

```bash
# 通义千问API配置（必须）
QWEN_API_KEY=your_qwen_api_key_here

# MinerU API配置（必须）
MINERU_TOKEN=your_mineru_token_here
```

**获取API密钥：**
- 通义千问：访问 https://dashscope.console.aliyun.com/
- MinerU：访问 https://mineru.net/

## 四、启动项目

### 方式一：分别启动（推荐开发环境）

**终端1 - 启动后端：**

```bash
# 确保在项目根目录
python server/main.py
```

后端将在 `http://localhost:5000` 启动

**终端2 - 启动前端：**

```bash
# 进入前端目录
cd client

# 启动开发服务器
npm run dev
```

前端将在 `http://localhost:3000` 启动

### 方式二：使用Flask CLI启动后端

```bash
# 设置环境变量
export FLASK_APP=server.main:app  # Linux/Mac
# 或
set FLASK_APP=server.main:app      # Windows

# 启动
flask run --reload
```

## 五、访问应用

打开浏览器访问：**http://localhost:3000**

## 六、验证服务

### 检查后端健康状态

```bash
# 浏览器访问
http://localhost:5000/api/health

# 或使用curl
curl http://localhost:5000/api/health
```

应该返回：
```json
{
  "success": true,
  "message": "服务运行正常",
  "data": {
    "status": "ok"
  }
}
```

### 检查前端

访问 `http://localhost:3000`，应该看到文献阅读器界面。

## 七、常见问题

### 1. 端口被占用

**后端端口5000被占用：**

```bash
# 修改 server/main.py 中的端口
app.run(host='0.0.0.0', port=5001)  # 改为5001
```

**前端端口3000被占用：**

```bash
# 修改 client/vite.config.js
server: {
  port: 3001  # 改为3001
}
```

### 2. API密钥未配置

如果看到错误提示：
- 检查 `.env` 文件是否存在
- 确认API密钥已正确填入
- 重启后端服务

### 3. 依赖安装失败

**Python依赖：**

```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像（可选）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**Node依赖：**

```bash
# 清除缓存
npm cache clean --force

# 使用国内镜像（可选）
npm install --registry=https://registry.npmmirror.com
```

### 4. 前端无法连接后端

检查 `client/vite.config.js` 中的代理配置：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',  // 确保端口正确
      changeOrigin: true,
    }
  }
}
```

## 八、生产环境部署

### 后端（使用gunicorn）

```bash
# 安装gunicorn
pip install gunicorn

# 启动
gunicorn server.main:app -w 4 -b 0.0.0.0:5000
```

### 前端（构建静态文件）

```bash
cd client
npm run build

# 构建后的文件在 client/dist 目录
# 可以使用nginx等服务器托管
```

## 九、开发建议

1. **使用虚拟环境**：避免依赖冲突
2. **配置热重载**：后端使用 `--reload`，前端Vite自动支持
3. **查看日志**：后端日志会显示在终端
4. **API测试**：使用Postman或curl测试API接口

## 十、快速启动脚本

### Windows (start.bat)

```batch
@echo off
echo 启动后端...
start cmd /k "python server/main.py"
timeout /t 3
echo 启动前端...
cd client
start cmd /k "npm run dev"
cd ..
```

### Linux/Mac (start.sh)

```bash
#!/bin/bash
echo "启动后端..."
python server/main.py &
sleep 3
echo "启动前端..."
cd client && npm run dev
```

---

**提示**：首次启动前，请确保：
1. ✅ 已安装所有依赖
2. ✅ 已配置 `.env` 文件
3. ✅ API密钥已正确填入
4. ✅ 端口未被占用

祝使用愉快！🎉

