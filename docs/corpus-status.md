# LinguaGraph 社交媒体语料库 — 状态报告

**日期:** 2026-06-17
**状态:** 初步建成

---

## 已完成

### 1. 语料库结构

```
BWKI/13_social_media_corpus/
├── freedom/           35 files
├── knowledge/         310 files
├── language_thought/  700 files
├── bilingualism/      129 files
├── emotion_culture/   156 files
├── identity/          22 files
├── moral_reasoning/   41 files
├── news_comments/     16 files (DDG scraped)
├── reddit/            0 files (待抓取)
├── zhihu/             0 files (待抓取)
├── german_forums/     0 files (待抓取)
└── youtube/           0 files (待抓取)
```

### 2. 数据统计

| 指标 | 数值 |
|------|------|
| 总扫描文件 | 1744 |
| 成功分类 | 1562 (89.6%) |
| 入库文件 | 1393 |
| 覆盖主题 | 7 |
| 覆盖语言 | 3 (en/zh/de) |

### 3. 按语言分布

| 语言 | 文件数 | 占比 |
|------|--------|------|
| en | 1556 | 99.7% |
| zh | 5 | 0.3% |
| de | 1 | 0.1% |

**问题:** 中文和德语文件极少。需要补充。

### 4. 每条记录包含的元数据

```yaml
type: social_media          # 数据类型
topic: freedom              # 主题分类
language: en                # 语言
platform: academic_paper    # 来源平台
source_domain: 02_linguistics  # 原始目录
source_file: (PDF)....md    # 原始文件名
crawled_at: "2026-06-17..." # 抓取时间
content_hash: "9be3..."     # 内容哈希（去重用）
quality: B                  # 质量评级
status: unverified          # 审核状态
tags: [freedom, en, academic, crawled]
```

---

## 待完成

| 任务 | 优先级 | 说明 |
|------|--------|------|
| 补充中文语料 | 高 | 当前仅 5 篇，需 200+ |
| 补充德语语料 | 高 | 当前仅 1 篇，需 200+ |
| Reddit 抓取 | 中 | 需要 Reddit API 或 Agent-Reach |
| 知乎抓取 | 中 | 需要反爬策略 |
| 德语论坛抓取 | 中 | 需要搜索德语论坛 |

---

## 使用方式

```bash
# 查看语料库
ls C:\Users\rongj\Desktop\本地知识库\知识库内容\BWKI\13_social_media_corpus\

# 按主题查看
ls C:\Users\rongj\Desktop\本地知识库\知识库内容\BWKI\13_social_media_corpus\freedom\

# 搜索特定内容
grep -r "concept" C:\Users\rongj\Desktop\本地知识库\知识库内容\BWKI\13_social_media_corpus\knowledge\
```
