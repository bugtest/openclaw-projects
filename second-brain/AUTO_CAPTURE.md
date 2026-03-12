# 🤖 Second Brain 自动捕获配置指南

---

## 📋 当前状态

| 功能 | 状态 | 说明 |
|------|------|------|
| **手动添加** | ✅ 可用 | `python3 memory_manager.py add` |
| **自动捕获脚本** | ✅ 已创建 | `auto_capture.py` |
| **OpenClaw 集成** | ⚠️ 需配置 | 需要添加 hook |

---

## 🔧 配置方法

### 方法 1: OpenClaw Hook 配置（推荐）

编辑 `~/.openclaw/openclaw.json`，添加 hook：

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "session-memory": {
          "enabled": true
        },
        "second-brain": {
          "enabled": true,
          "script": "/home/wcg/.openclaw/workspace/second-brain/auto_capture.py",
          "events": ["message.received", "message.sent"]
        }
      }
    }
  }
}
```

然后重启 OpenClaw：
```bash
openclaw gateway restart
```

---

### 方法 2: 使用关键词触发（无需配置）

在聊天中使用特定关键词，我会自动保存：

| 关键词 | 示例 | 类型 |
|--------|------|------|
| **保存** | "保存：AWS 备考资料" | note |
| **记住** | "记住这个链接 https://..." | link |
| **提醒** | "提醒我下周开会" | task |
| **想法** | "有个想法：用 AI 管理服务器" | idea |
| **收藏** | "收藏：这篇文档不错" | note |

**示例对话：**
```
你：保存：AWS GenAI 认证包含 65 道题，90 分钟
我：✅ 已保存到 Second Brain
   类型：note
   标签：AWS，学习，GenAI

你：记住 https://docs.openclaw.ai 官方文档
我：✅ 已保存到 Second Brain
   类型：link
   标签：文档，OpenClaw

你：提醒我下周一和刚哥开会
我：✅ 已保存到 Second Brain
   类型：task
   标签：工作，会议
```

---

### 方法 3: 手动命令（最可靠）

```bash
cd /home/wcg/.openclaw/workspace/second-brain

# 添加记忆
python3 memory_manager.py add "内容" type "标签 1，标签 2"

# 查看统计
python3 memory_manager.py stats
```

---

## 📊 自动捕获规则

### 会自动捕获的消息

| 条件 | 示例 | 类型 |
|------|------|------|
| 包含"保存/记住/收藏" | "保存这个资料" | memory |
| 包含"提醒/待办/记得" | "提醒我买牛奶" | task |
| 包含"想法/建议/创意" | "有个想法..." | idea |
| 包含 URL | "https://example.com" | link |
| 包含"github/docs" | "github.com/xxx" | link |

### 不会捕获的消息

- ❌ 太短的消息（< 5 字）
- ❌ 命令消息（如 `/status`）
- ❌ 系统消息
- ❌ 问候语（如"你好"）

---

## 🎯 实际使用流程

### 场景 1: 聊天中保存链接

```
你：https://github.com/bugtest/multiagent-framework 这个项目不错
我：✅ 已自动保存到 Second Brain
   类型：link
   标签：代码，GitHub
   
   要查看吗？
   - Dashboard: file:///home/wcg/.openclaw/workspace/second-brain/dashboard.html
   - 命令行：python3 memory_manager.py list
```

### 场景 2: 聊天中记录待办

```
你：提醒我下周一和刚哥开会讨论 AWS 认证
我：✅ 已保存到 Second Brain
   类型：task
   标签：工作，会议，AWS
   
   需要我设置定时提醒吗？
```

### 场景 3: 聊天中记录想法

```
你：有个想法：用钉钉机器人自动管理服务器监控
我：✅ 已保存到 Second Brain
   类型：idea
   标签：创意，自动化，运维
   
   好想法！要展开讲讲吗？
```

---

## 📝 查看已保存的内容

### Dashboard
```
file:///home/wcg/.openclaw/workspace/second-brain/dashboard.html
```

### 命令行
```bash
cd /home/wcg/.openclaw/workspace/second-brain

# 查看统计
python3 memory_manager.py stats

# 搜索
python3 memory_manager.py search "AWS"

# 列出最近
python3 memory_manager.py list 10
```

---

## ⚙️ 高级配置

### 自定义捕获关键词

编辑 `auto_capture.py`，修改 `AUTO_CAPTURE_KEYWORDS`：

```python
AUTO_CAPTURE_KEYWORDS = [
    "保存", "记住", "收藏",  # 现有
    "你的关键词",           # 添加新的
    "mark", "todo"
]
```

### 自定义标签规则

编辑 `extract_tags()` 函数：

```python
def extract_tags(content):
    tags = []
    
    # 添加你的规则
    if '你的关键词' in content:
        tags.append('你的标签')
    
    return tags if tags else ['自动捕获']
```

---

## 🎊 当前记忆库状态

```
📊 Memory 统计
--------------------------------------------------
总记忆数：7
今日新增：3

按类型:
  💡 idea: 2  - 想法、创意
  🔗 link: 2  - GitHub、文档链接
  📝 note: 1  - 学习笔记
  ✅ task: 2  - 待办、会议提醒
```

---

## 💡 建议

### 推荐配置
1. **启用自动捕获** - 聊天时自动保存重要信息
2. **定期回顾** - 每周查看 Dashboard
3. **整理标签** - 每月整理一次标签

### 隐私注意
- 个人敏感信息不会被捕获（如密码、token）
- 可以手动删除不想保存的记忆
- 记忆文件位置：`/home/wcg/.openclaw/workspace/second-brain/memories.json`

---

**需要我帮你配置 OpenClaw hook 吗？** 或者先用关键词触发的方式？🤖
