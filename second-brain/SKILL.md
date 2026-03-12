---
name: second-brain
description: |
  Second Brain memory capture and retrieval system. Activate when user wants to save notes, links, ideas, tasks, or memories. Supports: (1) Saving memories via message, (2) Searching existing memories, (3) Viewing memory statistics.
---

# Second Brain Skill

Personal knowledge management system with zero-friction capture and semantic search.

## Overview

Turn OpenClaw into a memory-capture system:
- **Capture**: Text anything to save (ideas, links, tasks, notes)
- **Store**: Automatic categorization and tagging
- **Retrieve**: Search across all memories with Cmd+K
- **Dashboard**: Web UI to browse and manage memories

## Memory Types

| Type | Trigger | Example |
|------|---------|---------|
| `idea` | 想法，思路，建议 | "有个想法：做个 AI 助手" |
| `link` | 包含 URL | "https://github.com/example" |
| `task` | 提醒，待办，记得 | "提醒我下周开会" |
| `note` | 默认类型 | "今天学习了 OpenClaw" |
| `memory` | 记住，记忆 | "记住刚哥的偏好" |

## Usage

### Save Memory

```text
保存：AWS 备考资料已整理完成
类型：note
标签：AWS，学习，GenAI
```

### Search Memories

```text
搜索：AWS
```

### View Statistics

```text
统计
```

### Quick Capture Patterns

User can text naturally:
- "提醒我明天买牛奶" → Auto-detected as task
- "https://example.com 这篇文章不错" → Auto-detected as link
- "有个想法：用 Bash 写多智能体框架" → Auto-detected as idea
- "今天学会了 OpenClaw 配置" → Auto-detected as note

## Dashboard

Access the web dashboard at:
```
file:///home/wcg/.openclaw/workspace/second-brain/dashboard.html
```

Features:
- Global search (Cmd+K)
- Filter by type
- Statistics overview
- Quick add form

## Integration

### DingTalk/iMessage/Telegram

Messages are automatically captured when user sends:
- "保存：[内容]"
- "记住：[内容]"
- "提醒：[内容]"

### Memory File

Location: `/home/wcg/.openclaw/workspace/second-brain/memories.json`

Format:
```json
{
  "version": 1,
  "created_at": "2026-02-24T14:00:00+08:00",
  "memories": [
    {
      "id": 1771911600,
      "type": "note",
      "content": "AWS 备考资料已整理完成",
      "date": "2026-02-24 14:00",
      "tags": ["AWS", "学习", "GenAI"]
    }
  ]
}
```

## Commands

```bash
# Add memory
bash /home/wcg/.openclaw/workspace/second-brain/capture.sh add "内容" note "标签 1，标签 2"

# Search
bash /home/wcg/.openclaw/workspace/second-brain/capture.sh search "关键词"

# List recent
bash /home/wcg/.openclaw/workspace/second-brain/capture.sh list 10

# Statistics
bash /home/wcg/.openclaw/workspace/second-brain/capture.sh stats
```

## Auto-Detection Rules

```bash
if content contains "http" → type: link
elif content contains "提醒 | 待办 | 记得 | 要" → type: task
elif content contains "想法 | 思路 | 建议 | 创意" → type: idea
elif content contains "记住 | 记忆" → type: memory
else → type: note
```

## Examples

### Example 1: Save Link
```
User: 保存这个链接 https://github.com/bugtest/multiagent-framework
Assistant: ✅ 已保存链接
  类型：link
  标签：GitHub，代码
```

### Example 2: Save Task
```
User: 提醒我下周和刚哥开会
Assistant: ✅ 已保存待办
  类型：task
  标签：工作，会议
```

### Example 3: Save Idea
```
User: 有个想法：用钉钉机器人管理服务器
Assistant: ✅ 已保存想法
  类型：idea
  标签：创意，自动化
```

### Example 4: Search
```
User: 搜索 AWS
Assistant: 🔍 找到 3 条相关记忆:
  1. [note] AWS 备考资料已整理完成 (2026-02-24)
  2. [link] https://aws.amazon.com/genai (2026-02-23)
  3. [task] 提醒考 AWS 认证 (2026-02-22)
```

## Related Files

- Dashboard: `/home/wcg/.openclaw/workspace/second-brain/dashboard.html`
- Capture Script: `/home/wcg/.openclaw/workspace/second-brain/capture.sh`
- Memory Storage: `/home/wcg/.openclaw/workspace/second-brain/memories.json`
- Log: `/home/wcg/.openclaw/workspace/second-brain/capture.log`
