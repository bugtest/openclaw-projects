# OpenClaw 市场调研多智能体团队

基于 [Richchen-maker/openclaw-multi-agent-team](https://github.com/Richchen-maker/openclaw-multi-agent-team) 框架搭建

---

## 团队架构

```
市场调研团队 (Market Research Team)
├── 团队协调官 (Coordinator) - 主智能体
├── 定量研究Agent (Quantitative Agent)
├── 定性研究Agent (Qualitative Agent)
├── 数据分析Agent (Data Analysis Agent)
└── 行业监测Agent (Industry Monitor Agent)
```

---

## 文件夹结构

```
~/clawd-bots/market-research-team/
├── AGENTS.md              # 团队工作流和路由配置
├── SOUL.md                # 团队协调官的身份和价值观
├── USER.md                # 刚哥的背景和目标
├── MEMORY.md              # 长期记忆（共享）
├── memory/                # 每日日志
│   ├── 2025-10-29.md
│   └── ...
├── agents/
│   ├── coordinator/       # 协调官私有上下文
│   ├── quantitative/      # 定量研究 Agent
│   ├── qualitative/       # 定性研究 Agent
│   ├── data-analysis/     # 数据分析 Agent
│   └── industry-monitor/  # 行业监测 Agent
├── skills/                # 定制技能
│   ├── survey-runner/
│   ├── interview-scheduler/
│   ├── competitor-tracker/
│   └── report-generator/
└── reports/               # 输出报告
    ├── daily/
    ├── weekly/
    └── monthly/
```

---

## 智能体配置

### 1. 团队协调官 (Coordinator)

**agentId:** `mr-coordinator`

**模型:** `bailian/qwen3.5-plus` (策略和协调)

**SOUL.md 核心:**
```markdown
# SOUL.md - 市场调研团队协调官

## 核心职责
- 接收刚哥的市场调研需求
- 分解任务并分配给专业 Agent
- 汇总各 Agent 输出，形成完整报告
- 维护团队记忆和知识沉淀

## 工作原则
- 主动不越界：协调但不代替专业 Agent 工作
- 质量把关：所有输出必须经过校验
- 及时同步：关键发现立即通知刚哥
- 持续学习：从每次调研中提炼方法论

## 沟通风格
- 直接、清晰、数据驱动
- 重要结论前置
- 不确定时明确标注置信度
```

**Cron 任务:**
| 时间 (SGT) | 任务 |
|-----------|------|
| Daily 09:00 | 检查各 Agent 夜间工作成果 |
| Daily 18:00 | 汇总当日调研发现，生成日报 |
| Weekly Mon 10:00 | 周度市场洞察报告 |

---

### 2. 定量研究 Agent (Quantitative Agent)

**agentId:** `mr-quantitative`

**模型:** `bailian/qwen3.5-plus` (数据分析)

**专长:**
- 问卷设计和分发
- 大规模数据统计分析
- 市场规模测算
- 用户行为量化研究

**技能配置:**
```markdown
## 可用技能
- survey-runner: 问卷执行和回收
- data-collector: 数据采集和清洗
- statistical-analysis: 统计分析 (SPSS/R/Python)
- visualization: 数据可视化 (Tableau/PowerBI)
```

**Cron 任务:**
| 时间 (SGT) | 任务 |
|-----------|------|
| Daily 10:00 | 检查问卷回收进度 |
| Daily 15:00 | 更新数据面板 |
| Weekly Fri 16:00 | 周度数据汇总 |

---

### 3. 定性研究 Agent (Qualitative Agent)

**agentId:** `mr-qualitative`

**模型:** `bailian/qwen3.5-plus` (深度理解)

**专长:**
- 深度访谈 (IDI) 设计和执行
- 焦点小组 (Focus Group) 主持
- 用户民族志研究
- 竞品体验分析

**技能配置:**
```markdown
## 可用技能
- interview-scheduler: 访谈安排和记录
- focus-group-moderator: 焦点小组引导
- insight-extractor: 洞察提炼
- report-writer: 定性报告撰写
```

**Cron 任务:**
| 时间 (SGT) | 任务 |
|-----------|------|
| Daily 11:00 | 整理访谈记录 |
| Daily 17:00 | 更新用户画像 |
| Weekly Thu 14:00 | 定性研究发现汇总 |

---

### 4. 数据分析 Agent (Data Analysis Agent)

**agentId:** `mr-data-analysis`

**模型:** `bailian/qwen3.5-plus` (机器学习)

**专长:**
- 爬虫和数据采集
- 社交媒体监听
- NLP 文本分析
- 预测建模

**技能配置:**
```markdown
## 可用技能
- web-scraper: 网页数据采集
- social-listener: 社交媒体监控
- nlp-analyzer: 文本情感分析
- ml-predictor: 机器学习预测
```

**Cron 任务:**
| 时间 (SGT) | 任务 |
|-----------|------|
| Hourly | 社交媒体关键词监控 |
| Daily 08:00 | 竞品数据抓取 |
| Daily 20:00 | 数据模型训练和更新 |

---

### 5. 行业监测 Agent (Industry Monitor Agent)

**agentId:** `mr-industry-monitor`

**模型:** `bailian/qwen3.5-plus` (行业洞察)

**专长:**
- 行业报告撰写
- 政策环境监测
- 竞争对手跟踪
- 供应链分析

**技能配置:**
```markdown
## 可用技能
- news-monitor: 行业新闻监控
- policy-tracker: 政策变化追踪
- competitor-analyzer: 竞品分析
- report-generator: 行业报告生成
```

**Cron 任务:**
| 时间 (SGT) | 任务 |
|-----------|------|
| Daily 07:00 | 晨间新闻简报 |
| Daily 19:00 | 竞品动态更新 |
| Weekly Wed 15:00 | 行业周报 |

---

## 共享记忆系统

### GOALS.md (团队目标)
```markdown
# 市场调研团队 OKRs

## Q4 2025 目标

### O1: 建立完整的市场调研能力
- KR1: 完成 5 个定量调研项目
- KR2: 完成 10 场深度访谈
- KR3: 建立竞品监测数据库

### O2: 输出高质量市场洞察
- KR1: 周度报告采纳率 ≥80%
- KR2: 关键洞察被业务落地 ≥3 个
- KR3: 调研响应时间 <48 小时

### O3: 优化团队效率
- KR1: 自动化率 ≥70%
- KR2: 单次调研成本降低 50%
- KR3: 客户满意度 ≥4.5/5
```

### DECISIONS.md (决策日志)
```markdown
# 关键决策记录

## 2025-10-29
- 决定采用 5 Agent 架构，而非 3 Agent（增加数据分析和行业监测）
- 选择 qwen3.5-plus 作为主力模型（平衡成本和质量）
- 确定 Telegram 为主要指挥通道
```

### PROJECT_STATUS.md (项目状态)
```markdown
# 当前项目状态

## 进行中项目
1. [P001] 新能源汽车用户调研 - 定量阶段
2. [P002] 竞品功能对比分析 - 数据收集中
3. [P003] 行业政策影响评估 - 等待政策发布

## 待启动项目
1. [P004] 消费者购买决策路径研究
2. [P005] 品牌健康度追踪
```

---

## AGENTS.md 配置示例

```markdown
# AGENTS.md - 市场调研团队工作流

## 团队信息
- **团队名称:** 市场调研多智能体团队
- **创建时间:** 2025-10-29
- **指挥通道:** Telegram
- **共享记忆:** ~/clawd-bots/market-research-team/

## Agent 列表

| Agent ID | 角色 | 模型 | 工作空间 |
|----------|------|------|----------|
| mr-coordinator | 团队协调官 | qwen3.5-plus | ~/.openclaw/agents/mr-coordinator |
| mr-quantitative | 定量研究 | qwen3.5-plus | ~/.openclaw/agents/mr-quantitative |
| mr-qualitative | 定性研究 | qwen3.5-plus | ~/.openclaw/agents/mr-qualitative |
| mr-data-analysis | 数据分析 | qwen3.5-plus | ~/.openclaw/agents/mr-data-analysis |
| mr-industry-monitor | 行业监测 | qwen3.5-plus | ~/.openclaw/agents/mr-industry-monitor |

## 任务分配规则

### 定量调研任务 → mr-quantitative
- 问卷设计
- 样本招募
- 数据统计
- 可视化报告

### 定性调研任务 → mr-qualitative
- 访谈提纲
- 焦点小组
- 用户观察
- 洞察提炼

### 数据采集任务 → mr-data-analysis
- 爬虫任务
- API 调用
- 数据清洗
- 模型训练

### 行业分析任务 → mr-industry-monitor
- 新闻监控
- 政策解读
- 竞品跟踪
- 报告撰写

### 复杂任务 → mr-coordinator 协调
- 多 Agent 协作项目
- 跨领域研究
- 紧急任务调度

## 通信协议

### 内部通信
- Agent 间通过共享记忆文件同步
- 每日 09:00 协调官检查各 Agent 状态
- 紧急事项使用 @mention 标记

### 对外通信
- 所有输出经协调官审核后发送
- 日报/周报自动推送到 Telegram
- 紧急发现即时通知刚哥

## 质量检查

### 输出校验清单
- [ ] 数据来源标注清晰
- [ ] 分析方法说明完整
- [ ] 结论有数据支撑
- [ ] 置信度明确标注
- [ ] 建议可执行

### 审核流程
1. Agent 自检
2. 协调官复审
3. 关键报告刚哥终审

## 活跃 Cron 任务

| 时间 (SGT) | Agent | 任务 |
|-----------|-------|------|
| Daily 07:00 | mr-industry-monitor | 晨间新闻简报 |
| Daily 08:00 | mr-data-analysis | 竞品数据抓取 |
| Daily 09:00 | mr-coordinator | 检查各 Agent 状态 |
| Daily 10:00 | mr-quantitative | 问卷进度检查 |
| Daily 11:00 | mr-qualitative | 访谈记录整理 |
| Daily 15:00 | mr-quantitative | 数据面板更新 |
| Daily 17:00 | mr-qualitative | 用户画像更新 |
| Daily 18:00 | mr-coordinator | 生成日报 |
| Daily 19:00 | mr-industry-monitor | 竞品动态更新 |
| Daily 20:00 | mr-data-analysis | 模型训练更新 |
| Weekly Mon 10:00 | mr-coordinator | 周度报告 |
| Weekly Wed 15:00 | mr-industry-monitor | 行业周报 |
| Weekly Fri 16:00 | mr-quantitative | 数据汇总 |
| Weekly Thu 14:00 | mr-qualitative | 定性发现汇总 |

## 成本优化

### 模型选择策略
- 策略性任务：qwen3.5-plus
- 执行性任务：qwen3.5-plus
- 例行任务：考虑本地模型

### 目标成本
- 日均成本：<¥50 (5 Agent)
- 单项目成本：根据规模预算

## 风险与应对

| 风险 | 应对措施 |
|------|----------|
| Agent 输出质量波动 | 定期审核 SOUL.md，更新记忆 |
| 任务冲突 | 协调官统一调度 |
| 记忆文件混乱 | 每周清理，归档旧日志 |
| API 限流 | 错峰执行，设置重试 |
```

---

## 部署步骤

### 第 1 周：基础搭建

```bash
# 1. 创建团队协调官
openclaw agents add mr-coordinator

# 2. 创建专业 Agent
openclaw agents add mr-quantitative
openclaw agents add mr-qualitative
openclaw agents add mr-data-analysis
openclaw agents add mr-industry-monitor

# 3. 配置各 Agent 的 SOUL.md 和 AGENTS.md
# (使用上面提供的模板)

# 4. 创建共享记忆目录
mkdir -p ~/clawd-bots/market-research-team/{memory,agents,skills,reports}

# 5. 初始化共享文件
touch ~/clawd-bots/market-research-team/{GOALS.md,DECISIONS.md,PROJECT_STATUS.md,MEMORY.md}
```

### 第 2 周：技能开发

- 开发定制技能（问卷、访谈、爬虫等）
- 配置各 Agent 的技能调用
- 测试单 Agent 工作流

### 第 3 周：集成测试

- 测试多 Agent 协作
- 优化任务分配逻辑
- 调整 Cron 时间表

### 第 4 周：正式运营

- 承接第一个真实项目
- 建立报告模板
- 收集反馈并优化

---

## 使用示例

### 启动一个调研项目

**刚哥在 Telegram 发送:**
```
/start_project
项目名称：新能源汽车用户调研
目标：了解潜在用户的购买决策因素
时间：2 周内完成
预算：中等
优先级：P0
```

**协调官响应:**
```
✅ 项目已创建 [P001]

任务分解:
1. mr-quantitative: 设计问卷，目标样本 N=500 (3 天)
2. mr-qualitative: 深度访谈 8 人 (4 天)
3. mr-data-analysis: 竞品数据抓取 (2 天)
4. mr-industry-monitor: 政策环境分析 (2 天)

预计完成：2025-11-12
下一步：各 Agent 开始执行，每日 18:00 同步进度
```

### 查看日报

**刚哥发送:**
```
/daily_report
```

**协调官响应:**
```
📊 市场调研日报 - 2025-10-29

【今日完成】
✅ mr-quantitative: 问卷设计完成，已发送 200 份
✅ mr-qualitative: 完成 2 场访谈，发现关键洞察 x3
✅ mr-data-analysis: 抓取竞品数据 1500 条
✅ mr-industry-monitor: 监测到政策变化 2 项

【进行中】
🔄 问卷回收中 (200/500, 40%)
🔄 访谈安排中 (2/8 完成)

【关键发现】
💡 价格敏感度比预期低 15%
💡 充电便利性是首要顾虑 (提及率 78%)

【明日计划】
📋 继续问卷回收
📋 安排 3 场访谈
📋 开始数据清洗

详细报告：~/clawd-bots/market-research-team/reports/daily/2025-10-29.md
```

---

## 成本估算

| Agent | 日均调用 | 单次成本 | 日均成本 |
|-------|---------|---------|---------|
| mr-coordinator | 20 次 | ¥0.08 | ¥1.60 |
| mr-quantitative | 30 次 | ¥0.08 | ¥2.40 |
| mr-qualitative | 25 次 | ¥0.08 | ¥2.00 |
| mr-data-analysis | 50 次 | ¥0.08 | ¥4.00 |
| mr-industry-monitor | 40 次 | ¥0.08 | ¥3.20 |
| **合计** | **165 次** | | **¥13.20/天** |

**月度成本:** ~¥400
**年度成本:** ~¥4,800

*注：基于 qwen3.5-plus 定价估算，实际成本根据使用量浮动*

---

## 关键成功因素

1. **清晰的 Agent 分工** - 避免职责重叠
2. **高效的共享记忆** - 确保信息同步
3. **严格的质量控制** - 协调官审核机制
4. **灵活的调度能力** - 应对紧急任务
5. **持续的学习优化** - 从项目中迭代

---

## 常见问题

**Q: 需要 5 个 Agent 同时运行吗？**
A: 建议从 1-2 个 Agent 开始（协调官 + 最需要的专业 Agent），逐步扩展。

**Q: 可以共用一个模型吗？**
A: 可以，但不同 Agent 的 SOUL.md 会赋予不同人格和专长。

**Q: 如何保证输出质量？**
A: 通过协调官审核 + 定期回顾 SOUL.md + 记忆维护。

**Q: Agent 之间会冲突吗？**
A: 通过文件读写权限设计避免（一人写入，多人读取）。

---

*文档版本：v1.0*
*创建时间：2025-10-29*
*基于：Richchen-maker/openclaw-multi-agent-team*
