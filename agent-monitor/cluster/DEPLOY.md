# 集群版部署指南

## 📋 部署清单

假设有 3 台机器：

| 机器 | IP | 角色 | 运行组件 |
|------|-----|------|----------|
| server-01 | 192.168.1.10 | OpenClaw + Exporter | exporter:9090 |
| server-02 | 192.168.1.11 | OpenClaw + Exporter | exporter:9090 |
| server-03 | 192.168.1.12 | OpenClaw + Exporter + 监控中心 | exporter:9090 + Prometheus + Grafana |

---

## 🚀 部署步骤

### 步骤 1：所有机器部署 Exporter

在 **每台机器** (server-01/02/03) 上执行：

```bash
# 1. 复制 agent-monitor 目录到每台机器
scp -r /home/wcg/.openclaw/workspace/agent-monitor user@192.168.1.10:/opt/
scp -r /home/wcg/.openclaw/workspace/agent-monitor user@192.168.1.11:/opt/
scp -r /home/wcg/.openclaw/workspace/agent-monitor user@192.168.1.12:/opt/

# 2. 在每台机器上启动 Exporter（带机器标识）
cd /opt/agent-monitor

# 方式 A：使用环境变量
export MACHINE_ID="server-01"  # 每台机器不同
nohup python3 exporter.py > exporter.log 2>&1 &

# 方式 B：使用命令行参数
python3 exporter.py --machine-id "server-01" --port 9090 &

# 3. 验证
curl http://localhost:9090/metrics | head -20
```

---

### 步骤 2：监控中心部署 Prometheus + Grafana

在 **server-03** (监控中心) 上执行：

```bash
cd /opt/agent-monitor/cluster

# 1. 编辑 targets.json，添加所有机器 IP
vim targets.json
```

**targets.json 内容：**

```json
[
  {
    "targets": ["192.168.1.10:9090", "192.168.1.11:9090", "192.168.1.12:9090"],
    "labels": {
      "env": "prod",
      "region": "beijing",
      "group": "cluster-a"
    }
  }
]
```

```bash
# 2. 启动 Prometheus + Grafana
docker-compose up -d

# 3. 验证
docker-compose ps
curl http://localhost:9091/-/healthy  # Prometheus
curl http://localhost:3000/api/health  # Grafana
```

---

### 步骤 3：访问 Grafana

浏览器访问：`http://192.168.1.12:3000`

- 账号：`admin`
- 密码：`admin`

**导入 Dashboard：**

1. 点击左侧菜单 **Dashboards** → **Import**
2. 上传 `grafana-dashboard-cluster.json`
3. 选择 Prometheus 数据源
4. 点击 **Import**

---

## 🔧 配置说明

### 机器标识 (MACHINE_ID)

每台机器的 exporter 必须有唯一标识：

```bash
# 推荐：使用 hostname 或自定义名称
export MACHINE_ID="server-01"
export MACHINE_ID="beijing-prod-01"
export MACHINE_ID="openclaw-worker-03"
```

### 目标配置 (targets.json)

支持多组目标，每组可以有不同标签：

```json
[
  {
    "targets": ["192.168.1.10:9090", "192.168.1.11:9090"],
    "labels": {
      "env": "prod",
      "region": "beijing"
    }
  },
  {
    "targets": ["192.168.2.10:9090"],
    "labels": {
      "env": "prod",
      "region": "shanghai"
    }
  },
  {
    "targets": ["192.168.3.10:9090"],
    "labels": {
      "env": "dev",
      "region": "beijing"
    }
  }
]
```

### Prometheus 配置

- **采集间隔**: 15 秒
- **数据保留**: 30 天
- **目标刷新**: 30 秒（自动发现新目标）

---

## 📊 Grafana Dashboard 功能

### 顶部筛选器

- **机器** - 选择查看特定机器或全部
- **环境** - 按 env 标签筛选 (prod/dev)
- **区域** - 按 region 标签筛选 (beijing/shanghai)

### 面板说明

| 面板 | 说明 |
|------|------|
| 集群活跃会话总数 | 所有机器会话数总和 |
| 集群活跃 Subagent 总数 | 所有机器 Subagent 总和 |
| 集群累计输入/输出 Token | 全集群 Token 统计 |
| 各机器 Token 使用速率 | 按机器分组的 Token 消耗曲线 |
| 各机器活跃会话数 | 按机器分组的会话数趋势 |
| 集群 Model 使用分布 | 全集群模型使用饼图 |
| 机器 Token 使用排行 | Top 10 机器排行 |
| 各机器 Session 详情 | 详细表格（机器/渠道/模型/Token 数） |

---

## 🔐 网络要求

### 防火墙规则

监控中心 (server-03) 需要能访问所有 exporter 的 9090 端口：

```bash
# 在所有机器上开放 9090 端口（内网）
sudo ufw allow from 192.168.1.0/24 to any port 9090
```

### 跨网络访问

如果机器不在同一网络：

**方案 A：SSH 隧道**

```bash
# 在监控中心建立隧道
ssh -L 9090:localhost:9090 user@192.168.1.10
```

**方案 B：VPN**

建立内网 VPN，所有机器在同一虚拟网络。

**方案 C：反向代理**

用 Nginx 做反向代理，统一暴露端口。

---

## 📈 扩容

### 新增机器

1. 在新机器上启动 exporter：
   ```bash
   export MACHINE_ID="server-04"
   python3 exporter.py &
   ```

2. 在监控中心更新 `targets.json`：
   ```json
   {
     "targets": ["192.168.1.10:9090", "192.168.1.11:9090", "192.168.1.12:9090", "192.168.1.13:9090"]
   }
   ```

3. Prometheus 自动发现（30 秒内），无需重启！

### 扩容监控中心

如果单机 Prometheus 扛不住：

- **方案 A**: 增加保留时间，降低采集频率
- **方案 B**: 用 Thanos/Cortex 做长期存储
- **方案 C**: 分片（按区域/环境拆分多个 Prometheus）

---

## 🛠️ 运维

### 查看状态

```bash
# Prometheus targets 状态
http://监控中心 IP:9091/targets

# Exporter 健康检查
curl http://各机器 IP:9090/health
```

### 日志查看

```bash
# Exporter 日志
tail -f /opt/agent-monitor/exporter.log

# Prometheus 日志
docker logs openclaw-prometheus-cluster

# Grafana 日志
docker logs openclaw-grafana-cluster
```

### 重启服务

```bash
# 重启 Exporter
pkill -f exporter.py
python3 exporter.py &

# 重启 Prometheus + Grafana
cd /opt/agent-monitor/cluster
docker-compose restart
```

---

## ⚠️ 注意事项

1. **时间同步** - 所有机器时间必须同步（用 NTP）
2. **主机名唯一** - MACHINE_ID 必须全局唯一
3. **网络延迟** - Prometheus 到 exporter 延迟 < 500ms
4. **磁盘空间** - Prometheus 数据目录可能较大（30 天数据）
5. **安全** - Grafana 首次登录后立即改密码！

---

## 📝 下一步

集群监控搭建完成后，可以继续：

1. **方案 2** - 飞书多维表格集成，推送日报/周报
2. **告警** - 配置 Prometheus Alertmanager，异常时通知
3. **长期存储** - 接入 Thanos，数据保留更久

---

**有问题？** 查看 README.md 或联系 小 A 🤖
