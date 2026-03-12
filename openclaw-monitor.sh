#!/bin/bash

# OpenClaw Gateway 监控脚本
LOG_FILE="$HOME/openclaw-gateway-monitor.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查进程是否存在
if ! pgrep -f "openclaw-gateway" > /dev/null 2>&1; then
    log "⚠️  openclaw-gateway 进程未运行，尝试重启..."
    
    # 尝试重启
    if openclaw gateway restart >> "$LOG_FILE" 2>&1; then
        log "✅ 重启成功"
    else
        log "❌ 重启失败"
    fi
else
    log "✓ 进程运行正常"
fi
