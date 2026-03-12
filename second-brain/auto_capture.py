#!/usr/bin/env python3
# =============================================================================
# Second Brain - Auto Capture Hook for OpenClaw (Enhanced)
# 自动捕获聊天内容到 Second Brain，支持去重
# =============================================================================

import json
import sys
import os
from datetime import datetime
from pathlib import Path
import hashlib

# Second Brain 目录
SECOND_BRAIN_DIR = Path("/home/wcg/.openclaw/workspace/second-brain")
MEMORY_FILE = SECOND_BRAIN_DIR / "memories.json"
LOG_FILE = SECOND_BRAIN_DIR / "auto_capture.log"

# 自动捕获关键词
AUTO_CAPTURE_KEYWORDS = [
    "保存", "记住", "收藏", "mark", "mark 一下",
    "提醒", "待办", "记得", "别忘了",
    "想法", "思路", "建议", "创意",
    "https://", "http://",
    "github.com", "docs.", "tutorial", "教程"
]

# 忽略的消息模式
IGNORE_PATTERNS = [
    "/new", "/reset", "/help", "/status",
    "HEARTBEAT_OK", "NO_REPLY"
]

def log_message(message):
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
            "config": {"dedup_enabled": True, "dedup_window_seconds": 3600}
        }
    
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"version": 2, "created_at": datetime.now().isoformat(), "memories": []}

def save_memories(data):
    """保存记忆"""
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def content_hash(content):
    """生成内容哈希"""
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

def should_capture(content):
    """判断是否应该捕获"""
    # 太短的消息不捕获
    if len(content) < 5:
        return False
    
    # 忽略命令
    for pattern in IGNORE_PATTERNS:
        if pattern in content:
            return False
    
    # 检查关键词
    for keyword in AUTO_CAPTURE_KEYWORDS:
        if keyword in content.lower():
            return True
    
    return False

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

def capture_message(content, source="chat"):
    """捕获消息到 Second Brain"""
    if not should_capture(content):
        return False
    
    data = load_memories()
    
    # 去重检查
    if is_duplicate(content, data.get("config", {})):
        log_message(f"Skipped duplicate: {content[:50]}")
        return False
    
    memory = {
        "id": int(datetime.now().timestamp()),
        "hash": content_hash(content),
        "type": detect_type(content),
        "content": content[:500],
        "date": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "tags": extract_tags(content),
        "source": source
    }
    
    data["memories"].insert(0, memory)
    save_memories(data)
    
    log_message(f"Captured [{memory['type']}]: {content[:100]}")
    
    return True

def process_input():
    """处理输入（从 stdin 读取）"""
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return
        
        data = json.loads(input_data)
        
        message = data.get('message', '')
        channel = data.get('channel', 'unknown')
        user = data.get('user', 'unknown')
        
        if capture_message(message, f"{channel}:{user}"):
            print(json.dumps({
                "success": True,
                "message": "已自动保存到 Second Brain",
                "type": detect_type(message)
            }))
        else:
            print(json.dumps({
                "success": False,
                "message": "不符合捕获条件或内容重复"
            }))
    
    except json.JSONDecodeError:
        content = sys.stdin.read().strip()
        if capture_message(content):
            print("✓ 已保存到 Second Brain")
        else:
            print("⊘ 未捕获（不符合条件或重复）")
    except Exception as e:
        log_message(f"Error: {str(e)}")
        print(json.dumps({"error": str(e)}))

if __name__ == '__main__':
    process_input()
