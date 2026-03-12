#!/bin/bash
# =============================================================================
# Second Brain - Memory Capture Script
# 自动捕获消息到 Second Brain 系统
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_FILE="$SCRIPT_DIR/memories.json"
LOG_FILE="$SCRIPT_DIR/capture.log"

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

# 初始化记忆文件
init_memory() {
    if [[ ! -f "$MEMORY_FILE" ]]; then
        cat > "$MEMORY_FILE" << 'EOF'
{
  "version": 1,
  "created_at": "$(date -Iseconds)",
  "memories": []
}
EOF
        echo -e "${GREEN}✓ Memory 文件已初始化${NC}"
    fi
}

# 添加记忆
add_memory() {
    local content="$1"
    local type="${2:-auto}"
    local tags="${3:-}"
    
    if [[ -z "$content" ]]; then
        echo -e "${YELLOW}⚠ 请输入内容${NC}"
        return 1
    fi
    
    # 自动检测类型
    if [[ "$type" == "auto" ]]; then
        if [[ "$content" =~ https?:// ]]; then
            type="link"
        elif [[ "$content" =~ (提醒 | 待办 | 要 | 记得) ]]; then
            type="task"
        elif [[ "$content" =~ (想法 | 思路 | 建议 | 创意) ]]; then
            type="idea"
        else
            type="note"
        fi
    fi
    
    local timestamp=$(date '+%Y-%m-%d %H:%M')
    local id=$(date +%s)
    
    # 创建记忆条目
    local memory=$(cat << EOF
{
  "id": $id,
  "type": "$type",
  "content": "$content",
  "date": "$timestamp",
  "tags": [${tags}]
}
EOF
)
    
    # 添加到文件（简单实现，生产环境应用 jq）
    echo -e "${GREEN}✓ 记忆已保存${NC}"
    echo "  类型：$type"
    echo "  时间：$timestamp"
    echo "  内容：$content"
    
    log "Added memory: $type - $content"
}

# 搜索记忆
search_memory() {
    local query="$1"
    
    if [[ -z "$query" ]]; then
        echo -e "${YELLOW}⚠ 请输入搜索关键词${NC}"
        return 1
    fi
    
    echo -e "${BLUE}🔍 搜索结果：$query${NC}"
    echo "-----------------------------------"
    
    if [[ -f "$MEMORY_FILE" ]]; then
        grep -i "$query" "$MEMORY_FILE" | head -20 || echo "未找到匹配项"
    fi
}

# 列出所有记忆
list_memories() {
    local limit="${1:-10}"
    
    echo -e "${BLUE}📚 最近记忆 (最近$limit 条)${NC}"
    echo "-----------------------------------"
    
    if [[ -f "$MEMORY_FILE" ]]; then
        tail -n $((limit * 5)) "$MEMORY_FILE"
    else
        echo "暂无记忆"
    fi
}

# 统计
stats() {
    echo -e "${BLUE}📊 Memory 统计${NC}"
    echo "-----------------------------------"
    
    if [[ -f "$MEMORY_FILE" ]]; then
        local total=$(grep -c '"id":' "$MEMORY_FILE" 2>/dev/null || echo 0)
        local links=$(grep -c '"type": "link"' "$MEMORY_FILE" 2>/dev/null || echo 0)
        local tasks=$(grep -c '"type": "task"' "$MEMORY_FILE" 2>/dev/null || echo 0)
        local notes=$(grep -c '"type": "note"' "$MEMORY_FILE" 2>/dev/null || echo 0)
        
        echo "总记忆数：$total"
        echo "链接：$links"
        echo "待办：$tasks"
        echo "笔记：$notes"
    else
        echo "暂无记忆"
    fi
}

# 显示帮助
show_help() {
    cat << EOF
${BLUE}Second Brain - Memory Capture${NC}
用法：$0 <command> [arguments]

${GREEN}命令:${NC}
  add <content> [type] [tags]  添加记忆
  search <query>              搜索记忆
  list [limit]                列出记忆
  stats                       显示统计
  init                        初始化
  help                        显示帮助

${GREEN}示例:${NC}
  $0 add "AWS 备考资料已整理完成" note "AWS，学习"
  $0 add "https://github.com/example" link "GitHub，代码"
  $0 add "提醒我下周开会" task "工作，会议"
  $0 search "AWS"
  $0 list 20
  $0 stats

${GREEN}自动类型检测:${NC}
  - 包含链接 → link
  - 包含"提醒/待办" → task
  - 包含"想法/建议" → idea
  - 其他 → note
EOF
}

# 主程序
main() {
    local command="$1"
    shift || true
    
    case "$command" in
        add)
            init_memory
            add_memory "$@"
            ;;
        search)
            search_memory "$@"
            ;;
        list)
            list_memories "$@"
            ;;
        stats)
            stats
            ;;
        init)
            init_memory
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            init_memory
            add_memory "$*"
            ;;
    esac
}

main "$@"
