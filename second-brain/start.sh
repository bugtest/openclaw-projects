#!/bin/bash
# =============================================================================
# Second Brain - Quick Launch Script
# 快速启动 Second Brain 系统
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DASHBOARD="$SCRIPT_DIR/dashboard.html"

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  🧠 Second Brain - 个人知识库${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# 检查文件
if [[ ! -f "$DASHBOARD" ]]; then
    echo -e "${YELLOW}⚠ Dashboard 文件不存在${NC}"
    exit 1
fi

# 显示统计
echo -e "${BLUE}📊 当前状态:${NC}"
python3 "$SCRIPT_DIR/memory_manager.py" stats
echo

# 打开 Dashboard
echo -e "${GREEN}✓ 打开 Dashboard...${NC}"
echo -e "  路径：$DASHBOARD"
echo

# 尝试不同的打开方式
if command -v google-chrome &> /dev/null; then
    google-chrome "$DASHBOARD" &
    echo -e "${GREEN}→ 已在 Chrome 中打开${NC}"
elif command -v chromium &> /dev/null; then
    chromium "$DASHBOARD" &
    echo -e "${GREEN}→ 已在 Chromium 中打开${NC}"
elif command -v xdg-open &> /dev/null; then
    xdg-open "$DASHBOARD" &
    echo -e "${GREEN}→ 已在默认浏览器中打开${NC}"
elif command -v open &> /dev/null; then
    open "$DASHBOARD" &
    echo -e "${GREEN}→ 已在浏览器中打开${NC}"
else
    echo -e "${YELLOW}⚠ 无法自动打开浏览器${NC}"
    echo -e "  请手动访问：file://$DASHBOARD"
fi

echo
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}💡 提示:${NC}"
echo -e "  - 搜索快捷键：Cmd+K / Ctrl+K"
echo -e "  - 快速添加：Ctrl+Enter"
echo -e "  - 命令行：python3 memory_manager.py <command>"
echo -e "${BLUE}========================================${NC}"
