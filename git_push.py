#!/usr/bin/env python3
"""
Git推送脚本
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """执行命令并显示输出"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print('='*60)
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return False

def main():
    # 切换到项目目录
    os.chdir(r'f:\桌面\wenxian')
    
    print("\n" + "="*60)
    print("GitHub推送脚本")
    print("="*60)
    
    # 1. 添加所有更改
    if not run_command("git add -A", "[1/4] 添加所有更改"):
        print("❌ 添加文件失败")
        return
    
    # 2. 检查状态
    run_command("git status --short", "[2/4] 检查状态")
    
    # 3. 提交更改
    commit_msg = """feat: 添加全文显示全屏功能、分批翻译和双栏对照视图，删除临时脚本文件

- 添加全文显示和双栏对照的全屏功能
- 实现分批翻译，实时显示翻译进度
- 优化翻译全文生成算法，支持基于layout数据构建
- 添加LaTeX数学公式支持（MathJax）
- 优化HTML表格显示，支持rowspan和colspan
- 删除测试和诊断文件
- 删除临时批处理脚本文件
- 改进UI布局和用户体验"""
    
    if not run_command(f'git commit -m "{commit_msg}"', "[3/4] 提交更改"):
        print("⚠️  提交可能失败或没有更改需要提交")
    
    # 4. 推送到GitHub
    if run_command("git push origin main", "[4/4] 推送到GitHub"):
        print("\n" + "="*60)
        print("✅ 推送成功！")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ 推送失败，请检查网络连接和GitHub认证")
        print("="*60)

if __name__ == '__main__':
    main()

