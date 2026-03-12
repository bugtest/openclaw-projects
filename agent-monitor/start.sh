#!/bin/bash

# OpenClaw Agent Monitor - 快速启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🤖 OpenClaw Agent Monitor 启动脚本"
echo "=================================="
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查 Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 选择启动方式
echo "选择启动方式:"
echo "1. 完整启动 (Exporter + Prometheus + Grafana)"
echo "2. 只启动 Exporter (已有 Prometheus/Grafana)"
echo "3. 只启动 Prometheus + Grafana (已有 Exporter)"
echo ""
read -p "请输入选项 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "🚀 完整启动所有组件..."
        
        # 启动 Exporter (后台运行)
        echo "📊 启动 Exporter..."
        nohup python3 exporter.py > exporter.log 2>&1 &
        EXPORTER_PID=$!
        echo $EXPORTER_PID > exporter.pid
        echo "   ✓ Exporter 已启动 (PID: $EXPORTER_PID)"
        
        # 等待 Exporter 就绪
        sleep 2
        
        # 启动 Prometheus + Grafana
        echo "📦 启动 Prometheus + Grafana..."
        docker-compose up -d
        echo "   ✓ Docker 容器已启动"
        
        ;;
    2)
        echo ""
        echo "📊 只启动 Exporter..."
        nohup python3 exporter.py > exporter.log 2>&1 &
        EXPORTER_PID=$!
        echo $EXPORTER_PID > exporter.pid
        echo "   ✓ Exporter 已启动 (PID: $EXPORTER_PID)"
        echo ""
        echo "📌 Metrics 端点：http://localhost:9090/metrics"
        ;;
    3)
        echo ""
        echo "📦 只启动 Prometheus + Grafana..."
        docker-compose up -d prometheus grafana
        echo "   ✓ Docker 容器已启动"
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "=================================="
echo "✅ 启动完成!"
echo ""
echo "📊 访问地址:"
echo "   - Exporter Metrics: http://localhost:9090/metrics"
echo "   - Exporter Health:  http://localhost:9090/health"
echo "   - Prometheus:       http://localhost:9091"
echo "   - Grafana:          http://localhost:3000 (admin/admin)"
echo ""
echo "📝 日志文件:"
echo "   - Exporter: $SCRIPT_DIR/exporter.log"
echo ""
echo "🛑 停止命令:"
echo "   ./stop.sh"
echo ""
