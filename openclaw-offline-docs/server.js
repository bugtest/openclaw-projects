const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8766;
const SITE_DIR = __dirname;

const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.md': 'text/markdown',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
    let filePath = path.join(SITE_DIR, req.url === '/' ? 'index.html' : req.url);
    
    // 安全限制：只能在 SITE_DIR 内访问
    const resolvedPath = path.resolve(filePath);
    if (!resolvedPath.startsWith(SITE_DIR)) {
        res.writeHead(403);
        res.end('Forbidden');
        return;
    }
    
    const ext = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes[ext] || 'application/octet-stream';
    
    fs.readFile(filePath, (err, content) => {
        if (err) {
            if (err.code === 'ENOENT') {
                res.writeHead(404);
                res.end('404 Not Found');
            } else {
                res.writeHead(500);
                res.end('500 Internal Server Error');
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content);
        }
    });
});

server.listen(PORT, '0.0.0.0', () => {
    const hostname = require('os').hostname();
    console.log(`
╔══════════════════════════════════════════════════════════╗
║        🦞 OpenClaw 离线文档中心 已启动                   ║
╠══════════════════════════════════════════════════════════╣
║  本地访问：http://localhost:${PORT}                       ║
║  局域网访问：http://${hostname}:8766                   ║
║                                                          ║
║  📁 文档目录：${SITE_DIR}                           ║
║  📊 文档数量：258 篇                                     ║
║                                                          ║
║  按 Ctrl+C 停止服务                                      ║
╚══════════════════════════════════════════════════════════╝
    `);
});
