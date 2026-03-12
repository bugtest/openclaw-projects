const https = require('https');
const fs = require('fs');
const path = require('path');

// 文档分类映射
const categoryMap = {
    'start/': 'get-started',
    'install/': 'install',
    'channels/': 'channels',
    'concepts/agent': 'agents',
    'concepts/session': 'agents',
    'concepts/memory': 'agents',
    'tools/': 'tools',
    'cli/': 'tools',
    'reference/templates/': 'agents',
    'providers/': 'models',
    'platforms/': 'platforms',
    'nodes/': 'platforms',
    'gateway/': 'gateway-ops',
    'automation/': 'gateway-ops',
    'web/': 'gateway-ops',
    'help/': 'reference',
    'reference/': 'reference',
    'plugins/': 'reference',
    'concepts/': 'reference',
};

function getCategory(urlPath) {
    for (const [prefix, category] of Object.entries(categoryMap)) {
        if (urlPath.startsWith(prefix)) {
            return category;
        }
    }
    return 'reference';
}

function fetchUrl(url) {
    return new Promise((resolve, reject) => {
        https.get(url, { timeout: 10000 }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                if (res.statusCode === 200) {
                    resolve(data);
                } else {
                    reject(new Error(`Status ${res.statusCode}`));
                }
            });
        }).on('error', reject);
    });
}

async function main() {
    // 读取 llms.txt 获取所有文档链接
    const llmsTxt = fs.readFileSync('/home/wcg/.openclaw/workspace/openclaw-docs.md', 'utf8');
    
    // 提取所有链接
    const linkRegex = /\[([^\]]+)\]\((https:\/\/docs\.openclaw\.ai\/[^\)]+)\)/g;
    const links = [];
    let match;
    
    while ((match = linkRegex.exec(llmsTxt)) !== null) {
        const title = match[1];
        const url = match[2];
        // 跳过索引页面和 API 文件
        if (!url.includes('/index.md') && !url.includes('openapi.json') && !url.includes('null')) {
            links.push({ title, url });
        }
    }
    
    console.log(`📚 找到 ${links.length} 个文档链接`);
    
    let success = 0;
    let failed = 0;
    const errors = [];
    
    for (let i = 0; i < links.length; i++) {
        const { title, url } = links[i];
        const urlPath = url.replace('https://docs.openclaw.ai/', '');
        const category = getCategory(urlPath);
        
        // 生成文件名
        const fileName = path.basename(urlPath, '.md');
        const outputPath = path.join('/home/wcg/.openclaw/workspace/openclaw-offline-docs', category, `${fileName}.md`);
        
        console.log(`[${i + 1}/${links.length}] 📥 ${title} → ${category}/${fileName}.md`);
        
        try {
            const content = await fetchUrl(url);
            
            // 添加 frontmatter
            const frontmatter = `---
title: ${title}
source: ${url}
category: ${category}
fetched: ${new Date().toISOString().split('T')[0]}
---

`;
            
            fs.writeFileSync(outputPath, frontmatter + content);
            success++;
        } catch (err) {
            failed++;
            errors.push({ title, url, error: err.message });
            console.log(`   ❌ 失败：${err.message}`);
        }
        
        // 避免请求过快
        await new Promise(r => setTimeout(r, 100));
    }
    
    // 生成汇总文件
    const summary = `# OpenClaw 离线文档汇总

抓取时间：${new Date().toISOString()}
文档总数：${links.length}
成功：${success}
失败：${failed}

## 分类统计
${Object.entries(categoryMap).map(([_, cat]) => {
    const count = fs.readdirSync(path.join('/home/wcg/.openclaw/workspace/openclaw-offline-docs', cat)).filter(f => f.endsWith('.md')).length;
    return `- ${cat}: ${count} 篇`;
}).join('\n')}

## 抓取失败的文档
${errors.length > 0 ? errors.map(e => `- ${e.title} (${e.url}): ${e.error}`).join('\n') : '无'}
`;
    
    fs.writeFileSync('/home/wcg/.openclaw/workspace/openclaw-offline-docs/SUMMARY.md', summary);
    
    console.log(`\n✅ 完成！成功：${success}, 失败：${failed}`);
    console.log(`📁 文档保存在：/home/wcg/.openclaw/workspace/openclaw-offline-docs/`);
    
    if (errors.length > 0) {
        console.log('\n❌ 失败的文档:');
        errors.forEach(e => console.log(`   - ${e.title}: ${e.error}`));
    }
}

main().catch(console.error);
