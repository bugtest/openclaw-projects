#!/bin/bash

# OpenClaw DevOps 多智能体系统状态脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📊 OpenClaw DevOps 多智能体系统状态"
echo "=================================="
echo ""

# 检查 Agent 会话状态
echo "🤖 Agent 会话状态:"
echo ""

# DevBot
echo "DevBot (开发助手):"
openclaw sessions list --label devbot --limit 1 2>/dev/null || echo "   ⚪ 未运行"
echo ""

# CIBot
echo "CIBot (构建助手):"
openclaw sessions list --label cibot --limit 1 2>/dev/null || echo "   ⚪ 未运行"
echo ""

# CDBot
echo "CDBot (部署助手):"
openclaw sessions list --label cdbot --limit 1 2>/dev/null || echo "   ⚪ 未运行"
echo ""

# 查看 blackboard 状态
echo "📋 共享黑板状态:"
echo ""

if [ -f "blackboard/STATUS.md" ]; then
    echo "当前系统状态:"
    grep -A 20 "## 当前状态" blackboard/STATUS.md | head -20
else
    echo "⚠️ 状态板未初始化"
fi

echo ""
echo "📝 最近活动:"
if [ -f "blackboard/STATUS.md" ]; then
    grep -A 10 "## 最近活动" blackboard/STATUS.md | head -10
else
    echo "暂无活动记录"
fi

echo ""
echo "=================================="
echo "💡 提示:"
echo "   启动系统：./start.sh"
echo "   停止系统：./stop.sh"
echo "   查看日志：./logs.sh"
