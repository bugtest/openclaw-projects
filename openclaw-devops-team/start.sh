#!/bin/bash

# OpenClaw DevOps 多智能体系统启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 启动 OpenClaw DevOps 多智能体系统..."
echo ""

# 检查配置
echo "📋 检查配置..."
if [ ! -f "config/feishu.yaml" ]; then
    echo "❌ 飞书配置缺失：config/feishu.yaml"
    exit 1
fi

if [ ! -f "config/github.yaml" ]; then
    echo "❌ GitHub 配置缺失：config/github.yaml"
    exit 1
fi

# 初始化 blackboard
echo "📝 初始化共享黑板..."
mkdir -p blackboard
touch blackboard/TASKS.md
touch blackboard/STATUS.md
touch blackboard/DECISIONS.md

# 启动 Agent 会话
echo ""
echo "🤖 启动 Agent 会话..."

# DevBot
echo "   → 启动 DevBot (开发助手)..."
openclaw sessions spawn \
    --label devbot \
    --task "DevBot: OpenClaw DevOps 开发助手，负责代码审查、Issue 管理、PR 创建。配置文件：agents/devbot.md" \
    --mode session \
    --cleanup keep

# CIBot
echo "   → 启动 CIBot (构建助手)..."
openclaw sessions spawn \
    --label cibot \
    --task "CIBot: OpenClaw DevOps 构建助手，负责 CI 流水线、测试执行、构建状态。配置文件：agents/cibot.md" \
    --mode session \
    --cleanup keep

# CDBot
echo "   → 启动 CDBot (部署助手)..."
openclaw sessions spawn \
    --label cdbot \
    --task "CDBot: OpenClaw DevOps 部署助手，负责部署执行、环境管理、监控告警。配置文件：agents/cdbot.md" \
    --mode session \
    --cleanup keep

echo ""
echo "✅ DevOps 多智能体系统启动完成!"
echo ""
echo "📊 查看状态：./status.sh"
echo "📱 飞书群配置:"
echo "   - 开发群：@开发助手 (DevBot)"
echo "   - 构建群：@构建助手 (CIBot)"
echo "   - 运维群：@部署助手 (CDBot)"
echo ""
echo "🔧 常用命令:"
echo "   /review <pr>     - 审查 PR"
echo "   /build           - 触发构建"
echo "   /deploy staging  - 部署到 staging"
echo "   /deploy prod     - 部署到生产"
echo "   /status          - 查看状态"
