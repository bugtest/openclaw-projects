# Agent Monitor - OpenClaw 实时监控体系

基于 Prometheus + Grafana 的 OpenClaw agent 观测平台。

## 🚀 快速启动

### 方式一：一键启动（推荐）

```bash
cd /home/wcg/.openclaw/workspace/agent-monitor

# 一键启动所有组件
./start.sh

# 访问 Grafana
# http://localhost:3000 (admin/admin)

# 停止
./stop.sh
```

### 方式二：分步启动

```bash
# 1. 启动 exporter (后台运行)
nohup python3 exporter.py > exporter.log 2>&1 &

# 2. 启动 Prometheus + Grafana
docker-compose up -d

# 3. 访问 Grafana
# http://localhost:3000 (admin/admin)
```

## 组件说明

| 组件 | 端口 | 说明 |
|------|------|------|
| exporter | 9090 | 采集 OpenClaw 数据，暴露 metrics |
| Prometheus | 9091 | 时序数据库 |
| Grafana | 3000 | 可视化 dashboard |

## Metrics 列表

| Metric | 类型 | 说明 |
|--------|------|------|
| `openclaw_sessions_active` | Gauge | 当前活跃会话数 |
| `openclaw_subagents_active` | Gauge | 当前活跃 subagent 数 |
| `openclaw_tokens_in_total` | Counter | 累计输入 token 数 |
| `openclaw_tokens_out_total` | Counter | 累计输出 token 数 |
| `openclaw_cost_usd_total` | Counter | 累计成本 (USD) |
| `openclaw_model_usage_total` | Counter | 各 model 使用次数 |
| `openclaw_session_duration_seconds` | Histogram | 会话耗时分布 |
| `openclaw_task_duration_seconds` | Histogram | 任务耗时分布 |

## Dashboard

导入 `grafana-dashboard.json` 到 Grafana 即可。
