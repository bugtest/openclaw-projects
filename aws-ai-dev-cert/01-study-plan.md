# AWS Certified Generative AI Developer (AIP-C01) 备考学习计划

## 📋 考试概览

- **考试代码**: AIP-C01
- **考试时长**: 170 分钟
- **题目数量**: 65 道计分题 + 10 道不计分题
- **及格分数**: 750/1000
- **考试费用**: $300 USD
- **有效期**: 3 年

## 🎯 前提条件

- ✅ 2 年以上 AWS 生产级应用开发经验
- ✅ 1 年以上 GenAI 解决方案实战经验
- ✅ 熟悉 AWS 计算、存储、网络服务
- ✅ 理解 AWS 安全和身份管理最佳实践

---

## 📅 8 周备考计划

### 第 1-2 周：Foundation Model Integration & Data Management (31%)

**目标**: 掌握 FM 集成、RAG、向量存储、知识图谱

**学习内容**:
- [ ] Amazon Bedrock 基础和服务概览
- [ ] 基础模型选择和评估方法
- [ ] 向量数据库原理 (OpenSearch Serverless, Pinecone, etc.)
- [ ] RAG 架构设计和实现
- [ ] Knowledge Bases for Bedrock
- [ ] 数据预处理和嵌入策略
- [ ] Prompt 工程基础

**实践任务**:
- [ ] 在 Bedrock 中部署一个 FM 应用
- [ ] 实现一个完整的 RAG 流水线
- [ ] 创建向量索引并测试检索效果

**推荐资源**:
- AWS Bedrock 官方文档
- AWS Workshop: Generative AI with Bedrock
- 论文: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"

---

### 第 3-4 周：Implementation & Integration (26%)

**目标**: 掌握 GenAI 应用开发和集成

**学习内容**:
- [ ] Bedrock Agents 和 Action Groups
- [ ] Function Calling 和工具集成
- [ ] API 设计和集成模式
- [ ] 事件驱动架构 (EventBridge, SQS, Lambda)
- [ ] 流式响应处理
- [ ] 多模态应用开发
- [ ] 自定义应用集成 (SDK, CLI)

**实践任务**:
- [ ] 创建一个 Bedrock Agent
- [ ] 实现 Function Calling 集成外部 API
- [ ] 构建流式响应的聊天应用

**推荐资源**:
- AWS Bedrock Agents 文档
- AWS Lambda 与 Bedrock 集成示例
- AWS SDK for Python (Boto3) Bedrock 示例

---

### 第 5 周：AI Safety, Security & Governance (20%)

**目标**: 掌握安全、治理和负责任的 AI 实践

**学习内容**:
- [ ] IAM 角色和策略配置
- [ ] 数据加密 (KMS, 传输中/静态)
- [ ] VPC 端点和网络隔离
- [ ] Guardrails for Bedrock
- [ ] 内容过滤和审核
- [ ] 审计和日志 (CloudTrail, CloudWatch)
- [ ] 合规性要求 (GDPR, HIPAA 等)
- [ ] Responsible AI 原则

**实践任务**:
- [ ] 配置 Bedrock Guardrails
- [ ] 设置 VPC 端点访问 Bedrock
- [ ] 实现完整的审计日志方案

**推荐资源**:
- AWS Security Best Practices for GenAI
- Bedrock Guardrails 文档
- AWS Well-Architected Framework - AI Lens

---

### 第 6 周：Operational Efficiency & Optimization (12%)

**目标**: 掌握成本优化和性能调优

**学习内容**:
- [ ] 模型推理优化 (延迟、吞吐量)
- [ ] 成本估算和优化策略
- [ ] 缓存策略 (Prompt 缓存、响应缓存)
- [ ] 批量处理和异步执行
- [ ] 监控指标和告警
- [ ] 自动扩展策略

**实践任务**:
- [ ] 使用 CloudWatch 监控 Bedrock 应用
- [ ] 实现响应缓存机制
- [ ] 优化 Prompt 长度和 token 使用

**推荐资源**:
- AWS Cost Optimization for GenAI
- Bedrock 定价模型
- CloudWatch Metrics for Bedrock

---

### 第 7 周：Testing, Validation & Troubleshooting (11%)

**目标**: 掌握测试、验证和故障排除

**学习内容**:
- [ ] 模型评估指标 (准确性、相关性、毒性)
- [ ] A/B 测试和金丝雀发布
- [ ] 调试技巧和工具
- [ ] 常见错误和解决方案
- [ ] 性能基准测试
- [ ] 用户反馈收集和分析

**实践任务**:
- [ ] 创建模型评估框架
- [ ] 实现 A/B 测试流程
- [ ] 模拟并解决常见问题

**推荐资源**:
- AWS Bedrock Model Evaluation
- ML Ops best practices

---

### 第 8 周：综合复习 + 模拟考试

**目标**: 全面复习和模拟实战

**学习计划**:
- [ ] 复习所有领域的关键概念
- [ ] 完成 3 套模拟考试 (每套 65 题)
- [ ] 分析错题，查漏补缺
- [ ] 复习 AWS 官方 Sample Questions
- [ ] 调整心态，准备考试

**模拟考试安排**:
- 模拟考 1: 第 8 周周一 (计时 170 分钟)
- 模拟考 2: 第 8 周周三 (计时 170 分钟)
- 模拟考 3: 第 8 周周五 (计时 170 分钟)

---

## 📚 每日学习建议

| 时间段 | 建议活动 |
|--------|----------|
| 早上 (1-2h) | 理论学习，阅读文档 |
| 中午 (30min) | 复习 flashcards/笔记 |
| 晚上 (2-3h) | 实践操作，动手实验 |
| 周末 (4-6h) | 综合项目，模拟考试 |

---

## ✅ 备考检查清单

### 考前 1 周
- [ ] 完成所有实践任务
- [ ] 完成 3 套模拟考试，正确率 > 80%
- [ ] 复习所有错题
- [ ] 确认考试预约
- [ ] 检查考试环境 (如果是在线考试)

### 考前 1 天
- [ ] 轻松复习，不做新题
- [ ] 准备好证件
- [ ] 保证充足睡眠

---

## 🎓 推荐学习资源

### 官方资源
1. [AWS Certified Generative AI Developer - Official Page](https://aws.amazon.com/certification/certified-generative-ai-developer-professional/)
2. [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
3. [AWS Skill Builder - Generative AI Courses](https://skillbuilder.aws/)
4. [AWS Workshops - Generative AI](https://workshops.aws/)

### 实践资源
1. AWS Free Tier (Bedrock 有免费额度)
2. GitHub AWS Samples
3. AWS re:Invent Generative AI Sessions

### 社区资源
1. AWS Developer Forums
2. Reddit r/aws
3. Discord AWS Community

---

**祝考试顺利！🎉**
