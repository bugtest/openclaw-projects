#!/usr/bin/env node

/**
 * OpenClaw GitHub CI/CD Receiver
 * 接收 GitHub Actions 的 task 请求，转发给 OpenClaw Agent 执行
 * 
 * 用法：node openclaw-receiver.js
 * 默认监听 8765 端口
 */

const http = require('http');
const { exec } = require('child_process');

const PORT = process.env.PORT || 8765;
const WORKSPACE = process.env.WORKSPACE || '/home/wcg/.openclaw/workspace';

const server = http.createServer(async (req, res) => {
  // CORS headers
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Authorization, Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  if (req.method !== 'POST') {
    res.writeHead(405);
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }

  // 验证 API Key (可选)
  const apiKey = req.headers.authorization?.replace('Bearer ', '');
  const expectedKey = process.env.API_KEY;
  if (expectedKey && apiKey !== expectedKey) {
    res.writeHead(401);
    res.end(JSON.stringify({ error: 'Unauthorized' }));
    return;
  }

  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', async () => {
    try {
      const data = JSON.parse(body);
      const { task, context, callback_url } = data;

      console.log(`[GitHub CI/CD] Received task: ${task}`);
      console.log(`[GitHub CI/CD] Context:`, context);

      // 调用 OpenClaw sessions_spawn 来执行任务
      // 这里使用 openclaw CLI 或者 sessions_send 来触发 agent
      const result = await executeAgentTask(task, context);

      // 如果有回调 URL，发送结果回 GitHub
      if (callback_url) {
        await sendCallback(callback_url, result);
      }

      res.writeHead(200);
      res.end(JSON.stringify({
        status: 'accepted',
        task_id: Date.now().toString(),
        result
      }));
    } catch (err) {
      console.error('[GitHub CI/CD] Error:', err);
      res.writeHead(500);
      res.end(JSON.stringify({ error: err.message }));
    }
  });
});

async function executeAgentTask(task, context) {
  return new Promise((resolve, reject) => {
    // 构建完整的 task 描述
    const fullTask = `[GitHub CI/CD Task] ${task}
    
Context:
- Repo: ${context?.repo || 'unknown'}
- Ref: ${context?.ref || 'unknown'}
- SHA: ${context?.sha || 'unknown'}
- Event: ${context?.event || 'unknown'}
- Workspace: ${context?.workspace || WORKSPACE}`;

    // 使用 openclaw sessions_spawn 来执行任务
    // 注意：这里需要根据实际 OpenClaw API 调整
    const cmd = `openclaw sessions_spawn --task "${fullTask.replace(/"/g, '\\"')}" --mode run`;
    
    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        // 如果 openclaw CLI 不可用，记录任务到文件供后续处理
        const fs = require('fs');
        const taskFile = `${WORKSPACE}/github-cicd/pending-tasks.json`;
        const pending = {
          timestamp: Date.now(),
          task: fullTask,
          context
        };
        
        let tasks = [];
        try {
          tasks = JSON.parse(fs.readFileSync(taskFile, 'utf8'));
        } catch {}
        tasks.push(pending);
        fs.writeFileSync(taskFile, JSON.stringify(tasks, null, 2));
        
        resolve({
          status: 'queued',
          message: 'Task queued for agent processing',
          note: 'openclaw CLI not available, task saved to pending-tasks.json'
        });
        return;
      }
      
      resolve({
        status: 'executing',
        message: 'Agent task spawned successfully',
        output: stdout
      });
    });
  });
}

async function sendCallback(callbackUrl, result) {
  // 发送结果回 GitHub Status API (简化版)
  console.log('[GitHub CI/CD] Callback to:', callbackUrl);
  // 实际实现需要根据 GitHub Status API 格式
}

server.listen(PORT, () => {
  console.log(`🚀 OpenClaw GitHub CI/CD Receiver listening on port ${PORT}`);
});
