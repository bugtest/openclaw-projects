# AWS AIP-C01 重点知识点整理

---

## Domain 1: Foundation Model Integration, Data Management, and Compliance (31%)

### 1.1 基础模型 (Foundation Models)

**关键概念**:
- **FM 类型**: 文本、图像、多模态、嵌入模型
- **Bedrock 支持的模型**: Claude, Llama, Titan, Jurassic, Command 等
- **模型选择标准**: 任务类型、上下文长度、成本、延迟、准确性

**重要服务**:
| 服务 | 用途 |
|------|------|
| Amazon Bedrock | FM 托管和推理 |
| Bedrock Playground | 模型测试和比较 |
| Model Invocation API | 编程调用模型 |

**考点**:
- 如何根据业务需求选择合适的 FM
- 理解不同模型的优缺点
- 模型版本管理和更新策略

---

### 1.2 RAG (Retrieval-Augmented Generation)

**架构组件**:
```
用户查询 → 嵌入模型 → 向量检索 → 上下文 + 查询 → FM → 生成回答
                ↓
           向量数据库
```

**关键技术**:
- **嵌入模型**: Titan Embeddings, Cohere Embed
- **向量数据库**: OpenSearch Serverless, Pinecone, pgvector
- **检索策略**: 语义搜索、混合搜索、重排序 (Reranking)
- **分块策略**: 固定大小、递归分块、语义分块

**最佳实践**:
- 选择合适的分块大小 (通常 256-512 tokens)
- 使用元数据过滤提高检索精度
- 实现混合检索 (语义 + 关键词)
- 添加引用和来源追溯

**考点**:
- RAG 架构设计
- 向量索引优化
- 检索质量评估指标

---

### 1.3 Knowledge Bases for Bedrock

**功能**:
- 托管的 RAG 解决方案
- 自动数据摄取和嵌入
- 与多种向量存储集成
- 内置检索和生成

**支持的数据源**:
- Amazon S3
- Salesforce
- Sharepoint
- 自定义数据源

**考点**:
- Knowledge Base 配置
- 数据同步策略
- 检索配置和优化

---

### 1.4 数据管理与合规

**数据预处理**:
- 数据清洗和标准化
- PII 检测和脱敏
- 文档格式转换

**合规要求**:
- GDPR (数据主体权利)
- HIPAA (医疗健康数据)
- SOC 2 (安全控制)
- 数据驻留要求

**考点**:
- 数据处理流程设计
- 合规性检查清单
- 数据生命周期管理

---

## Domain 2: Implementation and Integration (26%)

### 2.1 Bedrock Agents

**核心组件**:
- **Agent**: 自主执行任务的智能体
- **Action Group**: 定义可调用的函数
- **Knowledge Base**: 附加的知识源
- **Instruction**: 智能体的行为指南

**工作流程**:
```
用户输入 → Agent 解析 → 确定需要调用的 Action → 执行函数 → 整合结果 → 返回响应
```

**考点**:
- Agent 配置和部署
- Action Group 定义 (OpenAPI schema)
- 多步任务编排
- 会话状态管理

---

### 2.2 Function Calling

**实现方式**:
- Bedrock Agents Action Groups
- 直接 API 调用 (Converse API)
- Lambda 函数集成

**最佳实践**:
- 清晰的函数描述
- 严格的参数验证
- 错误处理和重试机制
- 超时和限流配置

**考点**:
- Function Calling 配置
- 参数映射和验证
- 错误处理策略

---

### 2.3 集成模式

**常见模式**:
1. **同步调用**: 实时响应，适合交互式应用
2. **异步调用**: 后台处理，适合长任务
3. **流式响应**: 逐步返回，改善用户体验
4. **批处理**: 批量请求，降低成本

**集成服务**:
| 服务 | 用途 |
|------|------|
| API Gateway | API 管理和安全 |
| Lambda | 无服务器计算 |
| Step Functions | 工作流编排 |
| EventBridge | 事件驱动架构 |
| SQS/SNS | 消息队列 |

**考点**:
- 选择合适的集成模式
- 服务间通信设计
- 错误处理和重试

---

### 2.4 多模态应用

**支持的能力**:
- 图像理解 (Claude 3, Llama 3.2 Vision)
- 图像生成 (Titan Image, Stable Diffusion)
- 文档分析 (PDF, 表格提取)

**考点**:
- 多模态模型选择
- 图像处理最佳实践
- 成本优化策略

---

## Domain 3: AI Safety, Security, and Governance (20%)

### 3.1 身份和访问管理 (IAM)

**关键策略**:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "bedrock:InvokeModel",
      "bedrock:InvokeModelWithResponseStream"
    ],
    "Resource": "arn:aws:bedrock:*::foundation-model/*"
  }]
}
```

**最佳实践**:
- 最小权限原则
- 使用 IAM Roles 而非 Access Keys
- 实施资源级权限
- 定期审计权限

**考点**:
- IAM 策略编写
- 跨账户访问配置
- 临时凭证管理

---

### 3.2 网络安全

**隔离策略**:
- VPC 端点 (PrivateLink)
- 安全组配置
- 网络 ACL
- 私有子网部署

**考点**:
- VPC 端点配置
- 网络隔离设计
- 数据传输加密

---

### 3.3 Guardrails for Bedrock

**功能**:
- 内容过滤 (敏感话题、仇恨言论等)
- PII 检测和屏蔽
- 自定义过滤规则
- 输入和输出过滤

**配置示例**:
- 屏蔽特定主题
- 检测并屏蔽 PII
- 自定义词汇过滤
- 内容 moderation 集成

**考点**:
- Guardrail 配置
- 过滤规则设计
- 误报和漏报处理

---

### 3.4 审计和监控

**服务**:
| 服务 | 用途 |
|------|------|
| CloudTrail | API 调用审计 |
| CloudWatch | 指标监控和告警 |
| AWS Config | 合规性检查 |

**关键指标**:
- Token 使用量 (输入/输出)
- 延迟 (首 token 时间，总时间)
- 错误率
- 成本

**考点**:
- 审计日志配置
- 监控仪表板设计
- 告警阈值设置

---

### 3.5 Responsible AI

**原则**:
- 公平性 (避免偏见)
- 可解释性 (理解决策)
- 隐私保护
- 安全性
- 问责制

**实践**:
- 模型偏见测试
- 人工审核流程
- 用户反馈机制
- 透明度报告

**考点**:
- Responsible AI 框架
- 偏见检测方法
- 伦理考量

---

## Domain 4: Operational Efficiency and Optimization (12%)

### 4.1 性能优化

**优化策略**:
- **Prompt 优化**: 精简提示，减少 token
- **缓存**: Prompt 缓存，响应缓存
- **批处理**: 批量嵌入，批量推理
- **模型选择**: 小模型处理简单任务

**指标**:
- 首 token 延迟 (Time to First Token)
- 总响应时间
- 吞吐量 (requests/second)

**考点**:
- 延迟优化技术
- 吞吐量提升方法
- 性能基准测试

---

### 4.2 成本优化

**成本组成**:
- 输入 token 费用
- 输出 token 费用
- 嵌入费用
- 向量存储费用

**优化策略**:
- 选择合适的模型 (成本/性能平衡)
- Prompt 压缩
- 响应缓存
- 使用 Spot 实例 (适用于自托管)
- 预留容量 (Provisioned Throughput)

**考点**:
- 成本估算
- 优化策略选择
- ROI 分析

---

### 4.3 监控和告警

**CloudWatch 指标**:
- `Invocations`: 调用次数
- `InputTokenCount`: 输入 token 数
- `OutputTokenCount`: 输出 token 数
- `Latency`: 延迟
- `Errors`: 错误数

**告警策略**:
- 错误率 > 5%
- 延迟 > 阈值
- 成本超预算
- 配额使用率 > 80%

**考点**:
- 监控指标理解
- 告警配置
- 仪表板设计

---

## Domain 5: Testing, Validation, and Troubleshooting (11%)

### 5.1 模型评估

**评估指标**:
- **准确性**: 回答正确率
- **相关性**: 检索内容相关性
- **完整性**: 回答覆盖度
- **毒性**: 有害内容检测
- **幻觉率**: 虚假信息比例

**评估方法**:
- 人工评估
- 自动化评估 (使用 FM 评估 FM)
- A/B 测试
- 用户反馈

**考点**:
- 评估指标选择
- 评估数据集构建
- 评估流程设计

---

### 5.2 测试策略

**测试类型**:
- 单元测试 (函数测试)
- 集成测试 (端到端流程)
- 负载测试 (压力测试)
- 回归测试 (变更后验证)

**测试工具**:
- Bedrock Model Evaluation
- 自定义测试框架
- 性能测试工具

**考点**:
- 测试用例设计
- 测试自动化
- 持续集成

---

### 5.3 故障排除

**常见问题**:
| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 超时 | 模型响应慢 | 增加超时，优化 prompt |
| 错误率高 | 配额限制 | 申请增加配额 |
| 质量差 | Prompt 不当 | 改进 prompt 工程 |
| 成本高 | Token 过多 | 优化 prompt，缓存 |

**调试工具**:
- CloudWatch Logs
- X-Ray 追踪
- Bedrock 日志

**考点**:
- 问题诊断流程
- 日志分析
- 常见错误代码

---

## 📝 快速复习卡片

### 重要数字
- 考试题目：65 道计分题
- 及格分数：750/1000
- 考试时长：170 分钟
- 证书有效期：3 年

### 核心服务
- **Bedrock**: FM 推理
- **Knowledge Bases**: 托管 RAG
- **Agents**: 自主智能体
- **Guardrails**: 安全过滤
- **OpenSearch Serverless**: 向量存储

### 关键概念
- RAG = 检索 + 生成
- Embedding = 文本→向量
- Function Calling = 模型调用外部 API
- Guardrails = 内容安全过滤

---

**持续更新中...**
