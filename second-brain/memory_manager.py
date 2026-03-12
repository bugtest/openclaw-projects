#!/usr/bin/env python3
# =============================================================================
# Second Brain - Memory Manager (Enhanced)
# 支持去重、编辑、删除、导出功能
# =============================================================================

import json
import sys
import os
from datetime import datetime
from pathlib import Path
import hashlib

SCRIPT_DIR = Path(__file__).parent
MEMORY_FILE = SCRIPT_DIR / "memories.json"
LOG_FILE = SCRIPT_DIR / "capture.log"

# ANSI 颜色
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
NC = '\033[0m'

def log(message):
    """写入日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

def load_memories():
    """加载记忆"""
    if not MEMORY_FILE.exists():
        return {
            "version": 2,
            "created_at": datetime.now().isoformat(),
            "memories": [],
            "config": {
                "dedup_enabled": True,
                "dedup_window_seconds": 3600  # 1 小时内重复内容忽略
            }
        }
    
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 升级到 v2
            if data.get("version", 1) == 1:
                data["version"] = 2
                data["config"] = {
                    "dedup_enabled": True,
                    "dedup_window_seconds": 3600
                }
                save_memories(data)
            return data
    except Exception as e:
        print(f"{RED}⚠ 加载失败：{e}{NC}")
        return {"version": 2, "created_at": datetime.now().isoformat(), "memories": []}

def save_memories(data):
    """保存记忆"""
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def content_hash(content):
    """生成内容哈希（用于去重）"""
    return hashlib.md5(content.strip().encode()).hexdigest()

def is_duplicate(content, config):
    """检查是否重复"""
    if not config.get("dedup_enabled", True):
        return False
    
    window = config.get("dedup_window_seconds", 3600)
    data = load_memories()
    current_hash = content_hash(content)
    now = datetime.now().timestamp()
    
    for mem in data["memories"]:
        mem_hash = mem.get("hash", content_hash(mem["content"]))
        mem_time = mem.get("id", 0)
        
        if mem_hash == current_hash and (now - mem_time) < window:
            return True
    
    return False

def detect_type(content):
    """自动检测类型"""
    content_lower = content.lower()
    
    if 'http' in content_lower or 'github' in content_lower or 'docs' in content_lower:
        return 'link'
    elif any(kw in content for kw in ['提醒', '待办', '记得', '别忘了', '要']):
        return 'task'
    elif any(kw in content for kw in ['想法', '思路', '建议', '创意']):
        return 'idea'
    elif any(kw in content for kw in ['记住', '记忆', '保存', '收藏']):
        return 'memory'
    else:
        return 'note'

def extract_tags(content):
    """自动提取标签"""
    tags = []
    
    if any(kw in content.lower() for kw in ['aws', 'genai', 'ai', 'ml', 'cloud']):
        tags.append('技术')
    if any(kw in content for kw in ['工作', '会议', '项目', '任务']):
        tags.append('工作')
    if any(kw in content for kw in ['学习', '考试', '认证', '资料']):
        tags.append('学习')
    if 'github' in content.lower() or '代码' in content:
        tags.append('代码')
    if 'openclaw' in content.lower() or 'claw' in content.lower():
        tags.append('OpenClaw')
    
    return tags if tags else ['自动捕获']

def add_memory(content, mem_type='auto', tags=None, skip_dedup=False):
    """添加记忆（支持去重）"""
    if not content:
        print(f"{YELLOW}⚠ 请输入内容{NC}")
        return
    
    # 去重检查
    data = load_memories()
    if not skip_dedup and is_duplicate(content, data.get("config", {})):
        print(f"{YELLOW}⊘ 检测到重复内容（1 小时内已存在），已跳过{NC}")
        return
    
    # 自动检测类型
    if mem_type == 'auto':
        mem_type = detect_type(content)
    
    # 解析标签
    if tags and isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',')]
    elif not tags:
        tags = extract_tags(content)
    
    memory = {
        "id": int(datetime.now().timestamp()),
        "hash": content_hash(content),
        "type": mem_type,
        "content": content,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "tags": tags
    }
    
    data["memories"].insert(0, memory)
    save_memories(data)
    
    print(f"{GREEN}✓ 记忆已保存{NC}")
    print(f"  类型：{mem_type}")
    print(f"  时间：{memory['date']}")
    print(f"  内容：{content[:80]}{'...' if len(content) > 80 else ''}")
    print(f"  标签：{', '.join(tags)}")
    
    log(f"Added {mem_type}: {content}")

def edit_memory(memory_id, new_content=None, new_type=None, new_tags=None):
    """编辑记忆"""
    data = load_memories()
    
    for mem in data["memories"]:
        if mem["id"] == memory_id:
            if new_content:
                mem["content"] = new_content
                mem["hash"] = content_hash(new_content)
            if new_type:
                mem["type"] = new_type
            if new_tags:
                if isinstance(new_tags, str):
                    new_tags = [t.strip() for t in new_tags.split(',')]
                mem["tags"] = new_tags
            
            mem["edited_at"] = datetime.now().strftime('%Y-%m-%d %H:%M')
            save_memories(data)
            
            print(f"{GREEN}✓ 记忆已更新{NC}")
            print(f"  ID: {memory_id}")
            print(f"  内容：{mem['content'][:80]}{'...' if len(mem['content']) > 80 else ''}")
            log(f"Edited memory {memory_id}")
            return
    
    print(f"{RED}⚠ 未找到 ID 为 {memory_id} 的记忆{NC}")

def delete_memory(memory_id):
    """删除记忆"""
    data = load_memories()
    original_count = len(data["memories"])
    
    data["memories"] = [m for m in data["memories"] if m["id"] != memory_id]
    
    if len(data["memories"]) < original_count:
        save_memories(data)
        print(f"{GREEN}✓ 已删除记忆 {memory_id}{NC}")
        log(f"Deleted memory {memory_id}")
    else:
        print(f"{RED}⚠ 未找到 ID 为 {memory_id} 的记忆{NC}")

def search_memories(query):
    """搜索记忆"""
    if not query:
        print(f"{YELLOW}⚠ 请输入搜索关键词{NC}")
        return
    
    data = load_memories()
    query_lower = query.lower()
    
    results = [
        m for m in data["memories"]
        if query_lower in m["content"].lower() or 
           any(query_lower in tag.lower() for tag in m.get("tags", []))
    ]
    
    print(f"{BLUE}🔍 搜索结果：{query}{NC}")
    print("-" * 60)
    
    if not results:
        print("未找到匹配项")
        return
    
    for i, mem in enumerate(results[:20], 1):
        type_icon = {
            'idea': '💡',
            'link': '🔗',
            'note': '📝',
            'task': '✅',
            'memory': '🧠'
        }.get(mem['type'], '📌')
        
        print(f"{i}. [{type_icon} {mem['type']}] {mem['content'][:60]}...")
        print(f"   ID: {mem['id']} | 时间：{mem['date']} | 标签：{', '.join(mem.get('tags', []))}")
        if mem.get("edited_at"):
            print(f"   编辑于：{mem['edited_at']}")
        print()

def list_memories(limit=10, mem_type=None):
    """列出记忆"""
    data = load_memories()
    memories = data["memories"]
    
    if mem_type:
        memories = [m for m in memories if m.get('type') == mem_type]
    
    memories = memories[-limit:]
    
    print(f"{BLUE}📚 最近记忆 (最近{limit}条){NC}")
    print("-" * 60)
    
    if not memories:
        print("暂无记忆")
        return
    
    for mem in reversed(memories):
        type_icon = {
            'idea': '💡',
            'link': '🔗',
            'note': '📝',
            'task': '✅',
            'memory': '🧠'
        }.get(mem['type'], '📌')
        
        print(f"[{type_icon} {mem['type']}] {mem['content'][:50]}")
        print(f"  ID: {mem['id']} | 时间：{mem['date']} | 标签：{', '.join(mem.get('tags', []))}")
        print()

def show_stats():
    """显示统计"""
    data = load_memories()
    memories = data["memories"]
    
    total = len(memories)
    by_type = {}
    for mem in memories:
        t = mem.get('type', 'note')
        by_type[t] = by_type.get(t, 0) + 1
    
    today = datetime.now().strftime('%Y-%m-%d')
    today_count = sum(1 for m in memories if m['date'].startswith(today))
    
    # 去重统计
    unique_hashes = set(m.get('hash', '') for m in memories)
    
    print(f"{BLUE}📊 Memory 统计{NC}")
    print("-" * 60)
    print(f"总记忆数：{total}")
    print(f"唯一记忆：{len(unique_hashes)}")
    print(f"今日新增：{today_count}")
    print(f"\n按类型:")
    for t, count in sorted(by_type.items()):
        icon = {'idea': '💡', 'link': '🔗', 'note': '📝', 'task': '✅', 'memory': '🧠'}.get(t, '📌')
        print(f"  {icon} {t}: {count}")
    
    # 配置信息
    config = data.get("config", {})
    print(f"\n{BLUE}配置:{NC}")
    print(f"  去重：{'✓ 启用' if config.get('dedup_enabled', True) else '⚠ 禁用'}")
    print(f"  窗口：{config.get('dedup_window_seconds', 3600)}秒")

def export_memories(format='json', output_file=None):
    """导出记忆"""
    data = load_memories()
    
    if format == 'json':
        output = json.dumps(data, ensure_ascii=False, indent=2)
    elif format == 'markdown':
        lines = ["# Second Brain - Memory Export\n"]
        for mem in data["memories"]:
            icon = {'idea': '💡', 'link': '🔗', 'note': '📝', 'task': '✅', 'memory': '🧠'}.get(mem['type'], '📌')
            lines.append(f"### {icon} [{mem['type']}] {mem['date']}")
            lines.append(f"\n{mem['content']}\n")
            lines.append(f"*标签：{', '.join(mem.get('tags', []))}*\n")
            lines.append("---\n")
        output = '\n'.join(lines)
    else:
        print(f"{RED}⚠ 不支持的格式：{format}{NC}")
        return
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"{GREEN}✓ 已导出到 {output_file}{NC}")
    else:
        print(output)

def deduplicate():
    """手动去重"""
    data = load_memories()
    seen_hashes = {}
    unique = []
    removed = 0
    
    for mem in data["memories"]:
        h = mem.get("hash", content_hash(mem["content"]))
        if h not in seen_hashes:
            seen_hashes[h] = mem
            unique.append(mem)
        else:
            removed += 1
    
    if removed > 0:
        data["memories"] = unique
        save_memories(data)
        print(f"{GREEN}✓ 清理了 {removed} 条重复记忆{NC}")
        log(f"Deduplicated: removed {removed} entries")
    else:
        print(f"{BLUE}ℹ 没有发现重复记忆{NC}")

def show_help():
    """显示帮助"""
    help_text = f"""
{BLUE}Second Brain - Memory Manager (Enhanced v2){NC}
用法：python3 memory_manager.py <command> [arguments]

{GREEN}核心命令:{NC}
  add <content> [type] [tags]     添加记忆
  edit <id> [content] [type] [tags]  编辑记忆
  delete <id>                   删除记忆
  search <query>                搜索记忆
  list [limit] [type]           列出记忆
  stats                         显示统计
  dedup                         手动去重

{GREEN}导出命令:{NC}
  export [json|md] [file]       导出记忆

{GREEN}示例:{NC}
  python3 memory_manager.py add "AWS 备考资料" note "AWS，学习"
  python3 memory_manager.py add "https://github.com" link "GitHub"
  python3 memory_manager.py add "提醒我开会" task "工作"
  python3 memory_manager.py edit 1771944506 "新内容"
  python3 memory_manager.py delete 1771944506
  python3 memory_manager.py search "AWS"
  python3 memory_manager.py list 20
  python3 memory_manager.py list 10 task
  python3 memory_manager.py stats
  python3 memory_manager.py dedup
  python3 memory_manager.py export md memories.md

{GREEN}自动类型检测:{NC}
  - 包含链接 → link
  - 包含"提醒/待办" → task
  - 包含"想法/建议" → idea
  - 包含"记住/保存" → memory
  - 其他 → note

{GREEN}配置 (memories.json):{NC}
  config.dedup_enabled: true/false     启用去重
  config.dedup_window_seconds: 3600    去重时间窗口
"""
    print(help_text)

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'add':
        content = sys.argv[2] if len(sys.argv) > 2 else ""
        mem_type = sys.argv[3] if len(sys.argv) > 3 else 'auto'
        tags = sys.argv[4] if len(sys.argv) > 4 else None
        add_memory(content, mem_type, tags)
    
    elif cmd == 'edit':
        if len(sys.argv) < 3:
            print(f"{YELLOW}⚠ 用法：edit <id> [content] [type] [tags]{NC}")
            return
        mem_id = int(sys.argv[2])
        content = sys.argv[3] if len(sys.argv) > 3 else None
        mem_type = sys.argv[4] if len(sys.argv) > 4 else None
        tags = sys.argv[5] if len(sys.argv) > 5 else None
        edit_memory(mem_id, content, mem_type, tags)
    
    elif cmd == 'delete':
        if len(sys.argv) < 3:
            print(f"{YELLOW}⚠ 用法：delete <id>{NC}")
            return
        mem_id = int(sys.argv[2])
        delete_memory(mem_id)
    
    elif cmd == 'search':
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        search_memories(query)
    
    elif cmd == 'list':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        mem_type = sys.argv[3] if len(sys.argv) > 3 else None
        list_memories(limit, mem_type)
    
    elif cmd == 'stats':
        show_stats()
    
    elif cmd == 'dedup':
        deduplicate()
    
    elif cmd == 'export':
        format = sys.argv[2] if len(sys.argv) > 2 else 'json'
        output = sys.argv[3] if len(sys.argv) > 3 else None
        export_memories(format, output)
    
    elif cmd == 'help' or cmd == '--help':
        show_help()
    
    else:
        # 默认添加到记忆
        content = ' '.join(sys.argv[1:])
        add_memory(content)

if __name__ == '__main__':
    main()
