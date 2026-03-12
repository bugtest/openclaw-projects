# GitHub CI/CD + OpenClaw Agent

最简的 GitHub Actions 与 OpenClaw Agent 集成工作流。

## 架构

```
GitHub Push/PR → Actions 触发 → 调用 OpenClaw API → Agent 执行 → 返回结果
```

## 配置步骤

### 1. 在 GitHub 仓库添加 Secrets

进入仓库 → Settings → Secrets and variables → Actions → New repository secrets:

| Secret 名称 | 说明 |
|------------|------|
| `OPENCLAW_API_KEY` | OpenClaw API 密钥 |
| `OPENCLAW_ENDPOINT` | OpenClaw API 端点 (如 `http://your-server:8080`) |

### 2. 在 OpenClaw 端配置接收

OpenClaw 需要暴露一个 HTTP endpoint 来接收 GitHub 的 task 请求。

### 3. 触发方式

- **自动触发**: push 或 PR 到 main/master 分支
- **手动触发**: Actions 页面 → "OpenClaw Agent Trigger" → Run workflow

## Agent 任务示例

Agent 收到任务后可以：

- Review 代码变更
- 运行测试并分析结果
- 生成变更摘要
- 检查代码规范
- 自动修复简单问题

## 扩展方向

- 添加 webhook 回调，让 agent 完成后更新 GitHub Status
- 支持 issue 自动处理
- 多 agent 分工（review agent、deploy agent 等）
