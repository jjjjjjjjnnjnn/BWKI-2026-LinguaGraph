# Cloudflare Worker 部署指南 — 解决中国用户提交问题

## 问题

Google 服务在中国被屏蔽，中国用户无法通过 Google Apps Script 提交问卷数据。

## 解决方案

用 Cloudflare Workers 做中转代理：国内用户 → Cloudflare Worker（可访问） → Google Apps Script（海外转发）。

## 部署步骤（3 分钟）

### 1. 注册 Cloudflare

1. 打开 https://dash.cloudflare.com/
2. 注册免费账号（用邮箱即可）
3. 验证邮箱后登录

### 2. 创建 Worker

1. 左侧菜单 → **Workers & Pages**
2. 点 **Create Worker**
3. Worker 名字填 `linguagraph-relay`
4. **删除默认代码**，粘贴 `scripts/cloudflare_worker.js` 的全部内容
5. 点 **Save and Deploy**

### 3. 获取 Worker URL

部署完成后，你会看到一个 URL，类似：
```
https://linguagraph-relay.你的子域名.workers.dev
```

复制这个 URL。

### 4. 更新调查问卷

打开 `cognitive-space/survey/index.html`，找到：

```js
const ENDPOINT_URL = 'https://script.google.com/...';
```

改为：

```js
const WORKER_URL = 'https://linguagraph-relay.你的子域名.workers.dev';
const ENDPOINT_URL = 'https://script.google.com/...';  // fallback
```

## 测试

1. 在国内网络环境下打开调查链接
2. 填一份测试回答 → 提交
3. 等 2 分钟 → 刷新 Google Sheets 看数据是否写入

## 原理

```
国内用户 → survey.html → Cloudflare Worker（国内可访问）
                                 ↓
                           Google Apps Script（海外转发）
                                 ↓
                           Google Sheets
```

Cloudflare Workers 免费计划：
- 每天 10 万次请求（足够用）
- 全球节点（国内部分节点可直连）
- 无需服务器、无需备案
