# 飞书机器人配置指南

## 步骤 1: 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 登录企业账号
3. 点击「创建应用」
4. 选择「自建应用」

## 步骤 2: 创建 3 个机器人应用

### DevBot (开发助手)
- **应用名称**: DevOps 开发助手
- **应用描述**: 负责代码审查、Issue 管理、PR 创建
- **图标**: 🔧 (或自定义)

### CIBot (构建助手)
- **应用名称**: DevOps 构建助手
- **应用描述**: 负责 CI 流水线、测试执行、构建状态
- **图标**: 🏗️ (或自定义)

### CDBot (部署助手)
- **应用名称**: DevOps 部署助手
- **应用描述**: 负责部署执行、环境管理、监控告警
- **图标**: 🚀 (或自定义)

## 步骤 3: 配置应用权限

每个应用需要以下权限：

### 机器人权限
- [x] 发送消息
- [x] 读取消息
- [x] 管理群组

### 事件订阅
- [x] 接收消息
- [x] 群组消息

### 权限配置示例
```json
{
  "permissions": [
    "im:message",
    "im:chat",
    "contact:group:readonly"
  ]
}
```

## 步骤 4: 获取凭证

在每个应用的「凭证与基础信息」页面获取：

- **App ID** (格式：`cli_xxxxxxxxxxxxxxxx`)
- **App Secret**
- **Verification Token**

将这些值填入 `config/feishu.yaml` 文件。

## 步骤 5: 配置事件订阅

1. 进入「事件订阅」页面
2. 配置请求 URL：`https://your-gateway.com/webhook/feishu`
3. 订阅以下事件：
   - `im.message.receive_v1` - 接收消息
   - `im.chat.member.added_v1` - 成员加入群聊

## 步骤 6: 添加机器人到飞书群

### 创建 3 个飞书群

1. **DevOps 开发群**
   - 添加：DevBot
   - 用途：代码审查通知、PR 讨论

2. **DevOps 构建群**
   - 添加：CIBot
   - 用途：构建状态、测试结果

3. **DevOps 运维群**
   - 添加：CDBot
   - 用途：部署通知、监控告警

### 添加步骤
1. 打开飞书群
2. 点击右上角「...」
3. 选择「添加机器人」
4. 选择对应的机器人应用

## 步骤 7: 配置环境变量

```bash
# 复制到 .env 文件
cp .env.example .env

# 编辑 .env 文件，填入实际的密钥
vim .env
```

### .env 文件内容
```bash
# DevBot
FEISHU_DEVBOT_APP_ID=cli_a1b2c3d4e5f6g7h8
FEISHU_DEVBOT_APP_SECRET=your-secret-here
FEISHU_DEVBOT_TOKEN=your-token-here
FEISHU_DEVBOT_CHANNEL=oc_dev_channel_id

# CIBot
FEISHU_CIBOT_APP_ID=cli_b2c3d4e5f6g7h8i9
FEISHU_CIBOT_APP_SECRET=your-secret-here
FEISHU_CIBOT_TOKEN=your-token-here
FEISHU_CIBOT_CHANNEL=oc_ci_channel_id

# CDBot
FEISHU_CDBOT_APP_ID=cli_c3d4e5f6g7h8i9j0
FEISHU_CDBOT_APP_SECRET=your-secret-here
FEISHU_CDBOT_TOKEN=your-token-here
FEISHU_CDBOT_CHANNEL=oc_cd_channel_id

# GitHub
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_WEBHOOK_SECRET=your-webhook-secret
```

## 步骤 8: 测试机器人

在飞书群中发送测试命令：

```
@开发助手 /status
@构建助手 /status
@部署助手 /status
```

应该收到对应的状态回复。

## 常见问题

### Q: 机器人收不到消息？
A: 检查：
1. 机器人是否已添加到群
2. 事件订阅是否配置正确
3. 请求 URL 是否可访问

### Q: 机器人发送消息失败？
A: 检查：
1. App Secret 是否正确
2. 权限是否已授予
3. 消息格式是否正确

### Q: 如何调试？
A: 查看日志：
```bash
./logs.sh
```

## 下一步

配置完成后，运行：
```bash
./start.sh
```

启动 DevOps 多智能体系统！
