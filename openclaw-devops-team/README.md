# OpenClaw DevOps 多智能体系统

## 系统架构

基于 OpenClaw 的多智能体 DevOps 自动化系统，每个 agent 以飞书机器人形式出现，负责 DevOps 流程的不同阶段。

### 三个核心 Agent

| Agent | 飞书机器人 | 职责 |
|-------|-----------|------|
| **DevBot** | 开发助手 | 代码审查、Issue 管理、PR 创建、分支管理 |
| **CIBot** | 构建助手 | CI 流水线、测试执行、构建状态、质量检查 |
| **CDBot** | 部署助手 | 部署执行、环境管理、监控告警、回滚 |

### DevOps 流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   DevBot    │────▶│   CIBot     │────▶│   CDBot     │
│  (开发阶段)  │     │  (构建阶段)  │     │  (部署阶段)  │
│             │     │             │     │             │
│ • 代码审查   │     │ • CI 流水线  │     │ • 部署执行   │
│ • Issue 管理 │     │ • 测试执行   │     │ • 环境管理   │
│ • PR 创建    │     │ • 构建状态   │     │ • 监控告警   │
│ • 分支管理   │     │ • 质量检查   │     │ • 回滚操作   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
  飞书群：开发群        飞书群：构建群        飞书群：运维群
```

## 协作机制

### Blackboard (共享黑板)
所有 agent 共享的状态板，用于：
- 任务传递
- 状态同步
- 决策记录
- 指标追踪

### 触发方式
1. **GitHub Webhook** → DevBot
2. **CI 事件** → CIBot
3. **部署请求** → CDBot
4. **飞书命令** → 任意 Agent

## 文件结构

```
openclaw-devops-team/
├── AGENTS.md           # 多 agent 配置
├── orchestrator.md     # 编排器配置
├── agents/
│   ├── devbot.md       # DevBot 配置
│   ├── cibot.md        # CIBot 配置
│   └── cdbot.md        # CDBot 配置
├── config/
│   ├── feishu.yaml     # 飞书配置
│   └── github.yaml     # GitHub 配置
├── workflows/
│   ├── pr-review.yaml  # PR 审查流程
│   ├── ci-pipeline.yaml # CI 流水线
│   └── cd-deploy.yaml  # CD 部署流程
├── blackboard/
│   ├── TASKS.md        # 任务列表
│   ├── STATUS.md       # 当前状态
│   └── DECISIONS.md    # 决策记录
└── output/             # 输出目录
```

## 快速启动

```bash
# 启动 DevOps 团队
cd openclaw-devops-team
./start.sh

# 查看状态
./status.sh
```

## 飞书机器人配置

需要在飞书开放平台创建 3 个机器人，获取 App ID 和 App Secret。
