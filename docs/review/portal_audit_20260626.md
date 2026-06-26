# LinguaGraph Portal & CognitiveSpace — 全量技术审计报告

**日期**: 2026-06-26  
**审计范围**: `cognitive-space/portal/index.html`, `cognitive-space/web/index.html`, `cognitive-space/web/v1_baseline.html`, `cognitive-space/web/i18n.js`, `_deploy/` 部署结构

---

## 问题汇总

| # | 严重程度 | 类别 | 描述 | 影响 |
|---|---------|------|------|------|
| 1 | 🔴 ERROR | CSP | `frame-src 'self' https:` 缺少 `data:` 导致 Mermaid sandbox iframe 加载被阻止 | Mermaid 管线图不渲染 |
| 2 | 🟡 WARN | Mermaid | `unreachable code after return statement` — Mermaid v11 `securityLevel:'sandbox'` 已知 bug | 控制台噪音，不影响功能 |
| 3 | 🔴 ERROR | 路径 | `cognitive-space/portal/index.html` 中 `<iframe src="../index.html">` 指向不存在的 `cognitive-space/index.html`（本地开发环境 404） | 3D 查看器在本地不加载 |
| 4 | 🔴 ERROR | 路径 | `cognitive-space/portal/index.html` 中图表引用 `../figures/` 指向不存在的 `cognitive-space/figures/`（本地开发环境 404） | 图片在本地不加载 |
| 5 | 🟡 WARN | JS | TRANSLATIONS 对象中存在 trailing commas（行尾逗号），在严格模式下可能导致错误 | 旧浏览器兼容性风险 |
| 6 | 🟡 WARN | 数据量 | `data.js` 为 1.4MB 的单一文件，3D 查看器加载时可能导致长时间白屏 | 性能问题 |

---

## 详细分析

### Issue 1: CSP frame-src 阻止 Mermaid sandbox
- **文件**: `cognitive-space/portal/index.html:6`
- **当前**: `frame-src 'self' https:`  
- **应改为**: `frame-src 'self' https: data:`
- **原因**: Mermaid v11 `securityLevel:'sandbox'` 通过 `data:text/html;base64,...` 创建 iframe 来隔离渲染。缺少 `data:` 白名单导致浏览器阻止加载。

### Issue 2: Mermaid unreachable code
- **文件**: `mermaid.min.js` (第三方 CDN)
- **原因**: Mermaid 11 的 sandbox 模式生成 iframe 时产生不可达代码路径。这是上游 bug，无法修复。Issue 1 修复后此警告可能消失或减少。

### Issue 3: iframe src 路径断裂
- **文件**: `cognitive-space/portal/index.html:501`
- **当前**: `<iframe src="../index.html">`
- **本地解析**: `cognitive-space/portal/../index.html` = `cognitive-space/index.html` — 不存在
- **部署解析**: `_deploy/portal/../index.html` = `_deploy/index.html` — 正常
- **修复**: 部署路径不变，本地创建 `cognitive-space/index.html` 重定向到 `web/index.html`

### Issue 4: 图表路径断裂
- **文件**: `cognitive-space/portal/index.html` (4处图片引用)
- **图片**: fig3_cds_by_level.png, fig7_three_subject_cds.png, fig5_hds_distribution.png, fig4_lds_heatmap.png
- **本地路径**: `../figures/` → `cognitive-space/figures/` — 不存在（实际在 `cognitive-space/web/figures/`）
- **部署路径**: `../figures/` → `_deploy/figures/` — 正常
- **修复**: 部署路径不变，本地创建 `cognitive-space/figures/` symlink 或复制

### Issue 5: Trailing commas
- **文件**: `cognitive-space/portal/index.html` TRANSLATIONS 对象
- **位置**: 多个键值对末尾（如 `},` → 前一个键以 `,` 结尾）
- **风险**: 低。现代浏览器 (Chrome/Firefox/Safari/Edge) 均支持 trailing commas in JS objects

### Issue 6: data.js 大小
- **文件**: `cognitive-space/web/data.js` (~1.4MB)
- **影响**: 3D 查看器首次加载需传输+解析 1.4MB 数据
- **缓解**: 已有 loading spinner。可考虑后续 gzip 压缩或分块加载

---

## 部署结构检查

| 环境 | 路径 | 状态 |
|------|------|------|
| 本地 Portal | `cognitive-space/portal/index.html` | iframe src 和 figures 路径断裂 |
| 本地 3D Viewer | `cognitive-space/web/index.html` | 正常 |
| 本地 Baseline | `cognitive-space/web/v1_baseline.html` | 正常 |
| 本地 i18n | `cognitive-space/web/i18n.js` | 正常 |
| 部署 Portal | `_deploy/portal/index.html` | 正常 (已有 TRANSLATIONS 修复) |
| 部署 3D Viewer | `_deploy/index.html` | 正常 |
| 部署 Figures | `_deploy/figures/*.png` | 正常 |

---

## 修复措施

1. **CSP**: 添加 `data:` → `frame-src 'self' https: data:`
2. **本地 dev**: 创建 `cognitive-space/index.html` 重定向文件（指向 `web/index.html`）
3. **本地 dev**: 复制 figures 到 `cognitive-space/figures/`
4. **TRANSLATIONS trailing commas**: 移除（可选，低风险）
5. **部署同步**: `_deploy/portal/index.html` 同步更新

## 待用户确认
- trailing commas 是否需要修复（影响极小）
- 是否需要 gzip data.js 以改善加载速度
