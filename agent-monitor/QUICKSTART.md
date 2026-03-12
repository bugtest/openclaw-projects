# 🚀 Agent Monitor 快速启动指南

## 一键启动

```bash
cd /home/wcg/.openclaw/workspace/agent-monitor
./start.sh
```

## 访问地址

| 组件 | 地址 | 说明 |
|------|------|------|
| **Grafana** | http://localhost:3000 | 可视化 Dashboard (admin/admin) |
| **Prometheus** | http://localhost:9091 | 时序数据库 |
| **Exporter** | http://localhost:9090/metrics | Metrics 端点 |
| **Exporter** | http://localhost:9090/health | 健康检查 |

## Grafana Dashboard

登录后导入 Dashboard：

1. 访问 http://localhost:3000
2. 登录：admin / admin
3. 点击左侧菜单 **Dashboards** → **Import**
4. 上传 `grafana-dashboard.json` 或输入 ID
5. 选择 Prometheus 数据源
6. 点击 **Import**

## 预置面板

- 📊 **活跃会话数** - 当前活跃的 OpenClaw 会话
- 🤖 **活跃 Subagent** - 正在运行的子代理
- 📥📤 **Token 统计** - 输入/输出 Token 累计
- 📈 **Token 使用速率** - 每分钟 Token 消耗
- 📊 **活跃 Agent 趋势** - 会话数变化趋势
- 🧠 **Model 使用分布** - 各模型使用比例
- 📊 **各 Session Token 使用** - 每个会话的详细用量

## 停止服务

```bash
./stop.sh
```

## 查看日志

```bash
# Exporter 日志
tail -f exporter.log

# Prometheus 日志
docker logs openclaw-prometheus

# Grafana 日志
docker logs openclaw-grafana
```

## Metrics 说明

| Metric | 类型 | 说明 |
|--------|------|------|
| `openclaw_sessions_active` | Gauge | 当前活跃会话数 |
| `openclaw_sessions_total` | Gauge | 总会话数 |
| `openclaw_subagents_active` | Gauge | 活跃 Subagent 数 |
| `openclaw_tokens_in_total` | Counter | 累计输入 Token |
| `openclaw_tokens_out_total` | Counter | 累计输出 Token |
| `openclaw_model_usage` | Gauge | 各 Model 使用次数 |
| `openclaw_session_tokens_in` | Gauge | 各 Session 输入 Token (带 labels) |
| `openclaw_session_tokens_out` | Gauge | 各 Session 输出 Token (带 labels) |

## 自定义配置

### 修改采集间隔

编辑 `prometheus.yml`：

```yaml
global:
  scrape_interval: 10s  # 改为 10 秒
```

重启 Prometheus：

```bash
docker-compose restart prometheus
```

### 修改 Grafana 端口

编辑 `docker-compose.yml`：

```yaml
grafana:
  ports:
    - "8080:3000"  # 改为 8080
```

## 故障排查

### Exporter 无法启动

```bash
# 检查 Python 版本
python3 --version  # 需要 3.8+

# 检查端口占用
lsof -i :9090

# 手动启动测试
python3 exporter.py
```

### Prometheus 无法连接 Exporter

检查 `prometheus.yml` 中的 targets 配置：

```yaml
scrape_configs:
  - job_name: 'openclaw-exporter'
    static_configs:
      - targets: ['host.docker.internal:9090']
```

如果是 Linux，可能需要用实际 IP：

```yaml
- targets: ['172.17.0.1:9090']
```

### Grafana 无法连接 Prometheus

检查数据源配置 `grafana/provisioning/datasources/prometheus.yml`：

```yaml
url: http://prometheus:9091  # Docker 网络内用容器名
```

## 下一步：飞书集成 (方案 2)

完成方案 3 后，可以继续实施方案 2：

1. 创建飞书多维表格
2. 编写定时脚本推送 metrics 到飞书
3. 在飞书中创建仪表盘

---

**有问题？** 查看 README.md 获取完整文档。
