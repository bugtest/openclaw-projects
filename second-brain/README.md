# 🧠 Second Brain - 个人知识库 v2

> 捕获应该像发短信一样简单，检索应该像搜索一样容易

**Enhanced v2** — 新增去重、编辑、删除、导出功能

---

## 🎯 这是什么？

Second Brain 是一个基于 OpenClaw 的个人知识管理系统，帮你：
- **零摩擦捕获** - 发短信一样简单
- **自动分类** - AI 自动检测类型和标签
- **智能去重** - 1 小时内重复内容自动跳过
- **全局搜索** - Cmd+K 快速搜索
- **Web Dashboard** - 美观的管理界面

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Second Brain System                       │
│                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐│
│  │   捕获层     │     │   存储层     │     │   检索层     ││
│  │  Capture     │────▶│   Storage    │────▶│  Retrieval   ││
│  └──────────────┘     └──────────────┘     └──────────────┘│
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│  - 钉钉/飞书消息      - JSON 文件存储    - Web Dashboard    │
│  - 命令行工具        - 去重机制         - 全局搜索         │
│  - 自动分类          - 标签系统         - 类型过滤         │
│  - 编辑/删除         - 版本管理         - 导出功能         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 1. 打开 Dashboard

```bash
# 在浏览器打开
google-chrome /home/wcg/.openclaw/workspace/second-brain/dashboard.html
```

### 2. 添加记忆

```bash
cd /home/wcg/.openclaw/workspace/second-brain

# 添加笔记
python3 memory_manager.py add "AWS 备考资料已整理完成" note "AWS，学习"

# 添加链接
python3 memory_manager.py add "https://github.com/example" link "GitHub"

# 添加待办
python3 memory_manager.py add "提醒我下周开会" task "工作"

# 添加想法
python3 memory_manager.py add "有个想法：用 AI 管理服务器" idea "创意"
```

### 3. 搜索记忆

```bash
# 搜索关键词
python3 memory_manager.py search "AWS"

# 列出最近
python3 memory_manager.py list 10

# 按类型过滤
python3 memory_manager.py list 10 task

# 查看统计
python3 memory_manager.py stats
```

---

## 📝 记忆类型

| 类型 | 自动检测关键词 | 示例 |
|------|--------------|------|
| 💡 **idea** | 想法，思路，建议，创意 | "有个想法：做个 AI 助手" |
| 🔗 **link** | 包含 URL | "https://example.com 这篇文章不错" |
| ✅ **task** | 提醒，待办，记得，要 | "提醒我明天买牛奶" |
| 📝 **note** | 默认类型 | "今天学习了 OpenClaw" |
| 🧠 **memory** | 记住，记忆，保存 | "记住刚哥的偏好" |

---

## 💡 使用场景

### 场景 1: 学习笔记
```bash
python3 memory_manager.py add "AWS GenAI 认证包含 65 道题，90 分钟，及格线 750" note "AWS，GenAI，认证"
```

### 场景 2: 收藏链接
```bash
python3 memory_manager.py add "https://docs.openclaw.ai - OpenClaw 官方文档" link "文档，OpenClaw"
```

### 场景 3: 待办提醒
```bash
python3 memory_manager.py add "提醒我下周一和刚哥讨论 AWS 认证考试" task "工作，会议"
```

### 场景 4: 灵感记录
```bash
python3 memory_manager.py add "想法：用钉钉机器人自动管理服务器监控" idea "创意，自动化"
```

### 场景 5: 编辑记忆
```bash
python3 memory_manager.py edit 1771944506 "更新后的内容"
python3 memory_manager.py edit 1771944506 --tags "新标签 1，新标签 2"
```

### 场景 6: 删除记忆
```bash
python3 memory_manager.py delete 1771944506
```

### 场景 7: 导出记忆
```bash
# 导出为 JSON
python3 memory_manager.py export json memories.json

# 导出为 Markdown
python3 memory_manager.py export md memories.md
```

---

## 🎨 Dashboard 功能

### 主要特性
- ✅ **全局搜索** (Cmd+K)
- ✅ **类型过滤** (全部/想法/链接/笔记/待办/记忆)
- ✅ **统计概览** (总数/今日/本周/链接数)
- ✅ **快速添加** (一键保存)
- ✅ **响应式设计** (支持手机)
- ✅ **去重显示** (唯一记忆数)

### 快捷键
| 快捷键 | 功能 |
|--------|------|
| `Cmd+K` | 聚焦搜索框 |
| `Ctrl+Enter` | 快速添加记忆 |

---

## 📊 当前状态

```
📊 Memory 统计
--------------------------------------------------
总记忆数：7
唯一记忆：6  (去重后)
今日新增：4

按类型:
  💡 idea: 2
  🔗 link: 2
  📝 note: 1
  ✅ task: 2
```

---

## 🔧 技术细节

### 文件结构
```
second-brain/
├── dashboard.html       # Web Dashboard (19KB)
├── memory_manager.py    # Python 管理器 (增强版)
├── auto_capture.py      # 自动捕获 Hook
├── capture.sh           # Bash 脚本 (备用)
├── SKILL.md             # OpenClaw Skill
├── README.md            # 本文档
├── memories.json        # 记忆存储 (v2 格式)
├── capture.log          # 操作日志
└── auto_capture.log     # 自动捕获日志
```

### 数据存储 (v2)
```json
{
  "version": 2,
  "created_at": "2026-02-24T22:48:00+08:00",
  "memories": [
    {
      "id": 1771944493,
      "hash": "f6g7h8i9j0k1l2m3n4o5",
      "type": "note",
      "content": "AWS GenAI 备考资料已整理完成",
      "date": "2026-02-24 22:48",
      "tags": ["AWS", "学习", "GenAI"]
    }
  ],
  "config": {
    "dedup_enabled": true,
    "dedup_window_seconds": 3600
  }
}
```

### 去重机制
- **哈希比对**: 使用 MD5 哈希值比对内容
- **时间窗口**: 默认 1 小时内重复内容自动跳过
- **可配置**: 通过 `config.dedup_window_seconds` 调整

---

## 🔗 集成 OpenClaw

### 自动捕获
通过钉钉/飞书给 OpenClaw 发消息，自动捕获：
```text
保存：AWS 备考资料已整理完成
记住：https://example.com
提醒：下周开会
```

### 搜索记忆
```text
搜索：AWS
统计
```

---

## 🎯 最佳实践

### 1. 每天使用
- 有任何想法立即保存
- 看到好链接马上收藏
- 待办事项随时记录

### 2. 定期回顾
- 每周查看统计
- 每月整理标签
- 每季度清理过期内容
- 运行 `dedup` 清理重复

### 3. 善用标签
- 保持标签简洁 (2-5 个)
- 使用一致的命名
- 避免过度分类

### 4. 定期导出
- 每月导出备份：`python3 memory_manager.py export md backup-2026-02.md`
- 重要内容同步到其他系统

---

## 📚 灵感来源

- [Building a Second Brain - Tiago Forte](https://www.buildingasecondbrain.com/)
- [Alex Finn 的 OpenClaw 用例视频](https://www.youtube.com/watch?v=41_TNGDDnfQ)
- [OpenClaw Memory System](https://github.com/openclaw/openclaw)

---

## 🤖 v2 更新日志

**Enhanced v2** (2026-02-25)
- ✅ 新增去重机制（哈希 + 时间窗口）
- ✅ 新增编辑功能 (`edit` 命令)
- ✅ 新增删除功能 (`delete` 命令)
- ✅ 新增导出功能 (`export` 命令，支持 JSON/Markdown)
- ✅ 新增手动去重 (`dedup` 命令)
- ✅ 新增内容哈希字段
- ✅ 修复 `created_at` 字段
- ✅ 优化自动捕获逻辑

---

**开始构建你的第二大脑吧！** 🧠✨
