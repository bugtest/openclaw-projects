# OpenClaw 离线文档汇总

**抓取时间：** 2026-03-07  
**文档总数：** 259  
**成功：** 258  
**失败：** 1  

---

## 📊 分类统计

| 分类 | 文档数 |
|---|---|
| 🚀 Get Started (入门) | 8 篇 |
| 📦 Install (安装) | 15 篇 |
| 💬 Channels (消息渠道) | 27 篇 |
| 🤖 Agents (代理) | 14 篇 |
| 🛠️ Tools (工具) | 45 篇 |
| 🧠 Models (模型) | 22 篇 |
| 📱 Platforms (平台) | 33 篇 |
| 🔧 Gateway & Ops | 39 篇 |
| 📚 Reference (参考) | 51 篇 |
| **总计** | **254 篇** |

---

## ❌ 抓取失败的文档

| 文档 | 原因 |
|---|---|
| /start/quickstart | HTTP 307 重定向 |

---

## 📁 目录结构

```
openclaw-offline-docs/
├── index.html          # 离线索引页面（可搜索、可阅读）
├── server.js           # HTTP 服务器
├── SUMMARY.md          # 本文件
├── fetch-docs.js       # 抓取脚本
├── get-started/        # 入门文档 (8 篇)
├── install/            # 安装文档 (15 篇)
├── channels/           # 渠道文档 (27 篇)
├── agents/             # Agent 文档 (14 篇)
├── tools/              # 工具文档 (45 篇)
├── models/             # 模型文档 (22 篇)
├── platforms/          # 平台文档 (33 篇)
├── gateway-ops/        # 网管运维 (39 篇)
└── reference/          # 参考文档 (51 篇)
```

---

## 🌐 访问方式

**HTTP 服务：**
```bash
cd ~/workspace/openclaw-offline-docs
node server.js
```

然后访问：http://localhost:8766

**直接阅读：**
- 每个分类目录下的 `.md` 文件
- 使用任意 Markdown 阅读器打开

---

*所有文档已完全本地化，无需联网即可查阅！*
