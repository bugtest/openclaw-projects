# OpenClaw DevOps 多智能体配置

## 会话配置

```yaml
sessions:
  - key: devbot-session
    label: devbot
    agentId: devbot
    model: bailian/qwen3.5-plus
    thinking: on
    
  - key: cibot-session
    label: cibot
    agentId: cibot
    model: bailian/qwen3.5-plus
    thinking: on
    
  - key: cdbot-session
    label: cdbot
    agentId: cdbot
    model: bailian/qwen3.5-plus
    thinking: on
```

## Agent 定义

### DevBot (开发助手)
- **会话 Key**: `devbot-session`
- **职责**: 代码审查、Issue 管理、PR 创建
- **飞书机器人**: 开发助手
- **触发**: GitHub webhook (push, pull_request, issues)

### CIBot (构建助手)
- **会话 Key**: `cibot-session`
- **职责**: CI 流水线、测试执行、构建状态
- **飞书机器人**: 构建助手
- **触发**: CI 事件、DevBot 任务传递

### CDBot (部署助手)
- **会话 Key**: `cdbot-session`
- **职责**: 部署执行、环境管理、监控告警
- **飞书机器人**: 部署助手
- **触发**: 部署请求、CIBot 构建成功

## 消息路由

```yaml
routing:
  feishu:
    devbot:
      channelId: "oc_abcdef123456"  # 开发群
      mentions: ["@DevBot"]
    cibot:
      channelId: "oc_abcdef123457"  # 构建群
      mentions: ["@CIBot"]
    cdbot:
      channelId: "oc_abcdef123458"  # 运维群
      mentions: ["@CDBot"]
```

## 共享状态 (Blackboard)

所有 agent 共享以下文件：
- `blackboard/TASKS.md` - 任务队列
- `blackboard/STATUS.md` - 当前状态
- `blackboard/DECISIONS.md` - 决策记录
- `blackboard/METRICS.md` - 指标追踪
