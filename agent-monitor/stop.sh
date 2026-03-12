#!/bin/bash

# OpenClaw Agent Monitor - 停止脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🛑 停止 OpenClaw Agent Monitor..."
echo ""

# 停止 Exporter
if [ -f exporter.pid ]; then
    EXPORTER_PID=$(cat exporter.pid)
    if kill -0 $EXPORTER_PID 2>/dev/null; then
        echo "📊 停止 Exporter (PID: $EXPORTER_PID)..."
        kill $EXPORTER_PID
        rm exporter.pid
        echo "   ✓ Exporter 已停止"
    else
        echo "   ⚠️  Exporter 未运行"
    fi
else
    # 尝试通过进程名停止
    pkill -f "python.*exporter.py" 2>/dev/null || true
    echo "   ✓ Exporter 已停止"
fi

# 停止 Docker 容器
echo "📦 停止 Docker 容器..."
docker-compose down
echo "   ✓ Docker 容器已停止"

echo ""
echo "✅ 所有组件已停止"
