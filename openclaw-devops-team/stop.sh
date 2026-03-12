#!/bin/bash

# OpenClaw DevOps 多智能体系统停止脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🛑 停止 OpenClaw DevOps 多智能体系统..."
echo ""

# 停止 Agent 会话
echo "停止 Agent 会话..."

# DevBot
echo "   → 停止 DevBot..."
openclaw subagents kill --target devbot 2>/dev/null || true

# CIBot
echo "   → 停止 CIBot..."
openclaw subagents kill --target cibot 2>/dev/null || true

# CDBot
echo "   → 停止 CDBot..."
openclaw subagents kill --target cdbot 2>/dev/null || true

echo ""
echo "✅ DevOps 多智能体系统已停止"
