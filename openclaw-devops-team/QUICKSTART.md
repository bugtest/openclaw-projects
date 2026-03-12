# 快速开始指南

## 1. 前置条件

- [ ] OpenClaw 已安装并运行
- [ ] 飞书企业账号
- [ ] GitHub 账号
- [ ] Node.js 18+

## 2. 配置飞书机器人 (10 分钟)

按照 [FEISHU-SETUP.md](FEISHU-SETUP.md) 创建 3 个飞书机器人：

1. **开发助手** (DevBot)
2. **构建助手** (CIBot)
3. **部署助手** (CDBot)

获取每个机器人的 App ID 和 App Secret。

## 3. 配置环境变量

```bash
cd openclaw-devops-team

# 复制示例配置
cp .env.example .env

# 编辑配置文件
vim .env
```

填入从飞书开放平台获取的凭证。

## 4. 配置 GitHub

### 4.1 创建 GitHub Token

```bash
# 访问 https://github.com/settings/tokens
# 创建 token，勾选以下权限:
# - repo (完整控制)
# - workflow
# - admin:repo_hook
```

### 4.2 配置 Webhook

在 GitHub 仓库设置中：
1. 进入 Settings → Webhooks
2. 添加 Webhook:
   - Payload URL: `https://your-gateway.com/webhook/github`
   - Content type: `application/json`
   - Secret: 你的 webhook 密钥
3. 选择事件：
   - [x] Pull requests
   - [x] Issues
   - [x] Pushes

## 5. 启动系统

```bash
# 启动 DevOps 多智能体系统
./start.sh

# 查看状态
./status.sh
```

## 6. 测试机器人

在对应的飞书群中发送：

### 开发群 (@开发助手)
```
/status
/review pr-123
```

### 构建群 (@构建助手)
```
/status
/build
```

### 运维群 (@部署助手)
```
/status
/deploy staging
```

## 7. 完整流程测试

### 测试 PR 审查流程
1. 在 GitHub 创建 PR
2. DevBot 自动审查并发送飞书通知
3. CIBot 自动触发构建
4. 构建成功后 CDBot 准备部署

### 测试部署流程
1. PR 合并到 main 分支
2. CIBot 自动构建生产版本
3. CDBot 部署到 staging
4. 健康检查通过后部署到 production

## 常用命令

### 飞书命令

| 命令 | Agent | 说明 |
|------|-------|------|
| `/status` | 全部 | 查看状态 |
| `/review <pr>` | DevBot | 审查 PR |
| `/build` | CIBot | 触发构建 |
| `/deploy staging` | CDBot | 部署到 staging |
| `/deploy prod` | CDBot | 部署到生产 |
| `/rollback` | CDBot | 回滚版本 |

### 本地命令

```bash
./start.sh      # 启动系统
./status.sh     # 查看状态
./stop.sh       # 停止系统
./logs.sh       # 查看日志
```

## 监控和日志

### 查看 Agent 日志
```bash
openclaw sessions list
openclaw sessions history <session-key>
```

### 查看 Blackboard
```bash
cat blackboard/STATUS.md
cat blackboard/TASKS.md
cat blackboard/DECISIONS.md
```

## 故障排查

### 机器人无响应
1. 检查 .env 配置是否正确
2. 检查飞书事件订阅 URL
3. 查看日志：`./logs.sh`

### 构建失败
1. 检查 GitHub Actions 配置
2. 查看构建日志
3. 检查测试代码

### 部署失败
1. 检查环境配置
2. 查看健康检查日志
3. 执行回滚：`/rollback`

## 下一步

- [ ] 配置监控告警
- [ ] 添加更多 CI 检查项
- [ ] 自定义部署策略
- [ ] 集成其他工具 (Jira, Slack 等)

## 获取帮助

- 查看文档：`cat README.md`
- 查看配置：`cat config/feishu.yaml`
- 查看工作流：`cat workflows/*.yaml`
