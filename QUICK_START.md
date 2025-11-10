# 🚀 快速开始指南

## 一、项目已就绪 ✅

项目结构已完整创建，包括：

- ✅ Flask后端（使用Blueprint架构）
- ✅ React前端（Vite + Tailwind）
- ✅ MinerU解析模块
- ✅ LLM翻译模块
- ✅ API路由和错误处理
- ✅ GitHub配置文件

## 二、使用GitHub管理代码

### 方式一：使用脚本（推荐）

**Windows用户：**
```bash
# 双击运行或在命令行执行
setup_git.bat
```

**Linux/Mac用户：**
```bash
chmod +x setup_git.sh
./setup_git.sh
```

### 方式二：手动执行

```bash
# 1. 初始化Git（如果还没初始化）
git init

# 2. 添加所有文件
git add .

# 3. 创建初始提交
git commit -m "feat: 初始项目提交 - 文献阅读器全栈应用"

# 4. 在GitHub上创建新仓库后，添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/literature-reader.git

# 5. 推送到GitHub
git branch -M main
git push -u origin main
```

## 三、后续开发流程

### 日常提交代码

```bash
# 1. 查看变更
git status

# 2. 添加文件
git add .

# 3. 提交（使用有意义的提交信息）
git commit -m "feat: 添加新功能"  # 新功能
git commit -m "fix: 修复bug"      # 修复bug
git commit -m "docs: 更新文档"    # 文档更新

# 4. 推送到GitHub
git push
```

### 创建功能分支

```bash
# 创建并切换到新分支
git checkout -b feature/新功能名称

# 开发完成后
git add .
git commit -m "feat: 新功能描述"
git push origin feature/新功能名称

# 在GitHub上创建Pull Request
```

## 四、重要文件说明

- `README.md` - 项目说明文档
- `GITHUB_SETUP.md` - GitHub详细使用指南
- `CONTRIBUTING.md` - 贡献指南
- `.gitignore` - Git忽略文件配置
- `.github/workflows/python.yml` - CI/CD工作流

## 五、启动项目

### 快速启动

**1. 配置环境变量**
```bash
# 复制模板文件
copy .env.example .env  # Windows
# 或
cp .env.example .env    # Linux/Mac

# 编辑 .env 文件，填入API密钥
```

**2. 安装依赖**
```bash
# 后端依赖
pip install -r requirements.txt

# 前端依赖
cd client
npm install
cd ..
```

**3. 启动服务**

**终端1 - 启动后端：**
```bash
python server/main.py
```
后端运行在：http://localhost:5000

**终端2 - 启动前端：**
```bash
cd client
npm run dev
```
前端运行在：http://localhost:3000

**4. 访问应用**
打开浏览器访问：http://localhost:3000

### 详细启动指南

查看 `START_GUIDE.md` 获取完整的启动说明和故障排除指南。

## 📚 更多帮助

- GitHub使用：查看 `GITHUB_SETUP.md`
- 贡献代码：查看 `CONTRIBUTING.md`
- 项目文档：查看 `README.md`

---

祝开发愉快！🎉

