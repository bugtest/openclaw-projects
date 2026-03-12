#!/usr/bin/env python3
"""
OpenClaw Agent Monitor - Prometheus Exporter

采集 OpenClaw sessions 和 subagents 数据，暴露 Prometheus metrics。
"""

import json
import subprocess
import time
import logging
import socket
import os
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# OpenClaw workspace 路径
WORKSPACE = Path.home() / ".openclaw" / "workspace"
OPENCLAW_CMD = "openclaw"

# 机器标识（用于集群模式）
MACHINE_ID = os.getenv('MACHINE_ID', socket.gethostname())
logger.info(f"🖥️  机器标识：{MACHINE_ID}")


class MetricsCollector:
    """采集 OpenClaw metrics"""
    
    def __init__(self):
        self.sessions_cache: Dict[str, Any] = {}
        self.subagents_cache: List[Dict] = []
        self.last_collect_time = 0
        self.collect_interval = 10  # 秒
        
    def run_command(self, cmd: str) -> str:
        """执行 OpenClaw 命令"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout
        except Exception as e:
            logger.error(f"命令执行失败：{cmd} - {e}")
            return ""
    
    def parse_json_output(self, output: str) -> Any:
        """解析 JSON 输出"""
        try:
            # 清理输出，提取 JSON 部分
            lines = output.strip().split('\n')
            json_str = ''
            for line in lines:
                json_str += line
            return json.loads(json_str)
        except Exception as e:
            logger.warning(f"JSON 解析失败：{e}")
            return None
    
    def collect_sessions(self) -> List[Dict]:
        """采集 sessions 数据"""
        output = self.run_command(f"{OPENCLAW_CMD} sessions list --json --limit 50")
        data = self.parse_json_output(output)
        
        if not data:
            return []
        
        # JSON 输出直接是 sessions 数组
        if isinstance(data, list):
            sessions = data
        else:
            sessions = data.get('sessions', [])
        
        logger.info(f"采集到 {len(sessions)} 个 sessions")
        return sessions
    
    def collect_subagents(self) -> List[Dict]:
        """采集 subagents 数据"""
        output = self.run_command(f"{OPENCLAW_CMD} subagents list")
        data = self.parse_json_output(output)
        
        if not data:
            return []
        
        active = data.get('active', [])
        logger.info(f"采集到 {len(active)} 个活跃 subagents")
        return active
    
    def collect(self) -> Dict[str, Any]:
        """执行一次完整采集"""
        now = time.time()
        
        # 限流
        if now - self.last_collect_time < self.collect_interval:
            return {
                'sessions': self.sessions_cache,
                'subagents': self.subagents_cache,
                'timestamp': now
            }
        
        self.last_collect_time = now
        
        # 采集数据
        sessions = self.collect_sessions()
        subagents = self.collect_subagents()
        
        # 更新缓存
        self.sessions_cache = {s.get('key', ''): s for s in sessions}
        self.subagents_cache = subagents
        
        return {
            'sessions': self.sessions_cache,
            'subagents': self.subagents_cache,
            'timestamp': now
        }


class MetricsRegistry:
    """Metrics 注册表"""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            'gauge': {},
            'counter': {},
            'histogram': {}
        }
    
    def gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        """记录 gauge metric"""
        key = self._make_key(name, labels)
        self.metrics['gauge'][key] = {
            'name': name,
            'value': value,
            'labels': labels or {}
        }
    
    def counter(self, name: str, value: float, labels: Dict[str, str] = None):
        """记录 counter metric"""
        key = self._make_key(name, labels)
        if key not in self.metrics['counter']:
            self.metrics['counter'][key] = {
                'name': name,
                'value': 0,
                'labels': labels or {}
            }
        self.metrics['counter'][key]['value'] += value
    
    def histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        """记录 histogram metric（简化版）"""
        key = self._make_key(name, labels)
        if key not in self.metrics['histogram']:
            self.metrics['histogram'][key] = {
                'name': name,
                'count': 0,
                'sum': 0,
                'labels': labels or {}
            }
        self.metrics['histogram'][key]['count'] += 1
        self.metrics['histogram'][key]['sum'] += value
    
    def _make_key(self, name: str, labels: Dict[str, str] = None) -> str:
        """生成 metric key"""
        if not labels:
            return name
        label_str = ','.join(f'{k}="{v}"' for k, v in sorted(labels.items()))
        return f'{name}{{{label_str}}}'
    
    def render_prometheus(self) -> str:
        """渲染为 Prometheus 格式"""
        lines = []
        lines.append("# HELP OpenClaw Agent Metrics")
        lines.append("# TYPE openclaw_scrape_timestamp gauge")
        lines.append(f"openclaw_scrape_timestamp{{instance=\"{MACHINE_ID}\"}} {time.time()}")
        lines.append("")
        
        # Gauge metrics
        for key, data in self.metrics['gauge'].items():
            lines.append(f"# HELP {data['name']} {data['name']}")
            lines.append(f"# TYPE {data['name']} gauge")
            
            # 合并默认标签（instance, machine_id）
            all_labels = {'instance': MACHINE_ID, 'machine_id': MACHINE_ID}
            all_labels.update(data['labels'])
            
            label_str = ','.join(f'{k}="{v}"' for k, v in sorted(all_labels.items()))
            lines.append(f"{data['name']}{{{label_str}}} {data['value']}")
            lines.append("")
        
        # Counter metrics
        for key, data in self.metrics['counter'].items():
            lines.append(f"# HELP {data['name']} {data['name']}")
            lines.append(f"# TYPE {data['name']} counter")
            
            # 合并默认标签（instance, machine_id）
            all_labels = {'instance': MACHINE_ID, 'machine_id': MACHINE_ID}
            all_labels.update(data['labels'])
            
            label_str = ','.join(f'{k}="{v}"' for k, v in sorted(all_labels.items()))
            lines.append(f"{data['name']}{{{label_str}}} {data['value']}")
            lines.append("")
        
        # Histogram metrics (简化为 summary)
        for key, data in self.metrics['histogram'].items():
            lines.append(f"# HELP {data['name']} {data['name']}")
            lines.append(f"# TYPE {data['name']} summary")
            
            # 合并默认标签（instance, machine_id）
            all_labels = {'instance': MACHINE_ID, 'machine_id': MACHINE_ID}
            all_labels.update(data['labels'])
            
            label_str = ','.join(f'{k}="{v}"' for k, v in sorted(all_labels.items()))
            lines.append(f"{data['name']}_count{{{label_str}}} {data['count']}")
            lines.append(f"{data['name']}_sum{{{label_str}}} {data['sum']}")
            lines.append("")
        
        return '\n'.join(lines)


class ExporterHandler(BaseHTTPRequestHandler):
    """HTTP 请求处理器"""
    
    collector = MetricsCollector()
    registry = MetricsRegistry()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        logger.info(f"{self.address_string()} - {format % args}")
    
    def do_GET(self):
        """处理 GET 请求"""
        if self.path == '/metrics':
            self.handle_metrics()
        elif self.path == '/health':
            self.handle_health()
        elif self.path == '/':
            self.handle_index()
        else:
            self.send_error(404, 'Not Found')
    
    def handle_index(self):
        """首页"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = """
        <html>
        <head><title>OpenClaw Agent Monitor</title></head>
        <body>
        <h1>🤖 OpenClaw Agent Monitor</h1>
        <p>Prometheus Exporter</p>
        <ul>
            <li><a href="/metrics">Metrics</a></li>
            <li><a href="/health">Health Check</a></li>
        </ul>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
    
    def handle_health(self):
        """健康检查"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'ok', 'timestamp': time.time()}).encode())
    
    def handle_metrics(self):
        """Metrics 端点"""
        try:
            # 采集数据
            data = self.collector.collect()
            
            # 重置 registry
            self.registry = MetricsRegistry()
            
            # 处理 sessions
            sessions = data.get('sessions', {})
            active_count = len([s for s in sessions.values() if not s.get('aborted_last_run', False)])
            
            self.registry.gauge('openclaw_sessions_active', active_count)
            self.registry.gauge('openclaw_sessions_total', len(sessions))
            
            # 处理 subagents
            subagents = data.get('subagents', [])
            self.registry.gauge('openclaw_subagents_active', len(subagents))
            
            # 处理每个 session 的 metrics
            total_tokens_in = 0
            total_tokens_out = 0
            total_cost = 0.0
            model_usage: Dict[str, int] = {}
            
            # sessions 可能是 dict 或 list
            sessions_list = list(sessions.values()) if isinstance(sessions, dict) else sessions
            
            for session in sessions_list:
                key = session.get('key', 'unknown')
                
                # Token 统计 (优先使用 inputTokens/outputTokens)
                tokens_in = session.get('inputTokens') or session.get('contextTokens', 0) or 0
                tokens_out = session.get('outputTokens') or session.get('totalTokens', 0) or 0
                total_tokens_in += tokens_in
                total_tokens_out += tokens_out
                
                # Model 统计
                model = session.get('model', 'unknown')
                model_usage[model] = model_usage.get(model, 0) + 1
                
                # 提取 channel 信息 (从 key 解析)
                channel = 'unknown'
                if 'feishu' in key:
                    channel = 'feishu'
                elif 'dingtalk' in key:
                    channel = 'dingtalk'
                elif 'openai' in key:
                    channel = 'openai'
                elif 'cron' in key:
                    channel = 'cron'
                
                # 每个 session 的详细信息
                labels = {
                    'session_key': key.split(':')[-1][:12] if ':' in key else key[:12],
                    'channel': channel,
                    'model': model
                }
                self.registry.gauge('openclaw_session_tokens_in', tokens_in, labels)
                self.registry.gauge('openclaw_session_tokens_out', tokens_out, labels)
            
            # 汇总 metrics
            self.registry.counter('openclaw_tokens_in_total', total_tokens_in)
            self.registry.counter('openclaw_tokens_out_total', total_tokens_out)
            
            # Model 使用统计
            for model, count in model_usage.items():
                self.registry.gauge('openclaw_model_usage', count, {'model': model})
            
            # 处理 subagents 详细信息
            for agent in subagents:
                labels = {
                    'task': agent.get('task', 'unknown')[:50],
                    'model': agent.get('model', 'unknown')
                }
                self.registry.gauge('openclaw_subagent_task', 1, labels)
            
            # 渲染输出
            output = self.registry.render_prometheus()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(output.encode('utf-8'))
            
            logger.info(f"Metrics 已生成：{len(sessions)} sessions, {len(subagents)} subagents")
            
        except Exception as e:
            logger.error(f"Metrics 生成失败：{e}")
            self.send_error(500, str(e))


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='OpenClaw Agent Monitor Exporter')
    parser.add_argument('--port', type=int, default=9090, help='监听端口 (默认：9090)')
    parser.add_argument('--machine-id', type=str, default=None, help='机器标识 (默认：hostname)')
    args = parser.parse_args()
    
    # 覆盖机器标识
    global MACHINE_ID
    if args.machine_id:
        MACHINE_ID = args.machine_id
        logger.info(f"🖥️  使用自定义机器标识：{MACHINE_ID}")
    
    port = args.port
    server = HTTPServer(('0.0.0.0', port), ExporterHandler)
    
    logger.info(f"🚀 OpenClaw Agent Monitor 启动")
    logger.info(f"📊 Metrics 端点：http://0.0.0.0:{port}/metrics")
    logger.info(f"❤️  健康检查：http://0.0.0.0:{port}/health")
    logger.info(f"🏠 首页：http://0.0.0.0:{port}/")
    logger.info(f"🖥️  机器标识：{MACHINE_ID}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("👋 收到中断信号，正在关闭...")
        server.shutdown()


if __name__ == '__main__':
    main()
