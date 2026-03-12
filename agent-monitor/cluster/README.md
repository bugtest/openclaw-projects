# Agent Monitor - 集群版

多机器 OpenClaw 集中式监控方案。

## 架构

```
机器 A → Exporter:9090 ─┐
机器 B → Exporter:9090 ─┼→ 中央 Prometheus → Grafana
机器 C → Exporter:9090 ─┘
```

## 部署步骤

### 1. 每台机器部署 Exporter

```bash
# 在每台运行 OpenClaw 的机器上
cd /path/to/agent-monitor

# 设置机器标识（可选，默认用 hostname）
export MACHINE_ID="server-01"

# 启动 Exporter
nohup python3 exporter.py > exporter.log 2>&1 &
```

### 2. 中央服务器部署 Prometheus + Grafana

在**其中一台机器**（或独立监控服务器）上：

```bash
cd /path/to/agent-monitor/cluster

# 编辑 targets.json，添加所有机器 IP
vim targets.json

# 启动 Prometheus + Grafana
docker-compose up -d
```

### 3. 访问 Grafana

```
http://中央服务器 IP:3000
账号：admin
密码：admin
```

---

## 配置说明

### targets.json - 目标机器列表

```json
[
  {
    "targets": ["192.168.1.10:9090", "192.168.1.11:9090"],
    "labels": {
      "env": "prod",
      "region": "beijing",
      "group": "cluster-a"
    }
  }
]
```

### prometheus.yml - Prometheus 配置

- 每 15 秒抓取一次所有 exporter
- 数据保留 30 天
- 支持动态刷新目标列表

### grafana-dashboard.json - 仪表盘

- 支持按机器筛选
- 支持按环境/区域筛选
- 总览 + 单机详情

---

## 扩容

新增机器时：

1. 在新机器上启动 exporter
2. 在中央服务器的 `targets.json` 中添加新机器 IP
3. Prometheus 会自动发现（30 秒内）

无需重启！

---

## 网络要求

- 中央 Prometheus 需要能访问所有 exporter 的 9090 端口
- 如果跨网络，可能需要：
  - 开放防火墙规则
  - 使用 VPN/内网穿透
  - 通过 SSH 隧道转发

---

## 安全加固（可选）

### 1. Exporter 加认证

```bash
# 启动时加认证
python3 exporter.py --auth-token "your-secret-token"
```

### 2. Prometheus 加 Basic Auth

编辑 `docker-compose.yml`：
```yaml
command:
  - '--web.read-user=admin'
  - '--web.read-password=/etc/prometheus/password'
```

### 3. Grafana 改密码

首次登录后立即修改 admin 密码！

---

## 故障排查

### Exporter 无法访问

```bash
# 检查 exporter 是否运行
curl http://localhost:9090/metrics

# 检查防火墙
telnet 192.168.1.10 9090

# 检查 exporter 日志
tail exporter.log
```

### Prometheus 无法抓取

检查 Prometheus targets 状态：
```
http://中央服务器:9091/targets
```

查看哪些目标是 DOWN 状态。

---

**下一步：** 集成飞书多维表格，实现跨机器数据汇总报告（方案 2）
