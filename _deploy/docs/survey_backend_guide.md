# Survey Backend — Deployment Guide

> **目的**: 自动收集问卷回复到 Google Sheets，无需手动发送邮件。

---

## 步骤一：部署 Google Apps Script (2分钟)

1. 打开 https://sheets.google.com 创建新表格，取名 `LinguaGraph Survey Responses`
2. 点菜单「Extensions → Apps Script」
3. 删除默认代码，复制粘贴 `scripts/survey_backend.gs` 的内容
4. 按 `Ctrl+S` 保存，项目名取 `LinguaGraph Backend`
5. 点「Deploy → New deployment」
6. 类型选 **Web app**
7. 设置：
   - **Execute as**: Me
   - **Who has access**: Anyone
8. 点 Deploy
9. **复制 Web App URL**（以 `https://script.google.com/.../exec` 开头）

## 步骤二：配置调查问卷 (30秒)

1. 打开 `cognitive-space/survey/index.html`
2. 找到第 267 行：
   ```js
   const ENDPOINT_URL = '';
   ```
3. 把 Google Apps Script URL 粘贴进去：
   ```js
   const ENDPOINT_URL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec';
   ```

## 步骤三：测试

1. 在浏览器打开 `cognitive-space/survey/index.html`
2. 填一份测试回答并提交
3. 打开你的 Google Sheets 刷新——应该看到新行

## 工作原理

```
用户提交 → survey.html → fetch() → Google Apps Script
                                         ↓
                                  Google Sheets (自动写入)
```

- 完全免费（Google 配额每天 20,000 次请求）
- 不需要服务器
- 不需要数据库
- 数据实时进入表格
