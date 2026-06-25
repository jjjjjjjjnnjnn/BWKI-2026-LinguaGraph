# LinguaGraph — 综合审查报告 (2026-06-22)

> **全面企业化、正规化、流程化审查**
> 范围：项目结构 · Python 代码 · Web 可视化 · 合规安全 · 研究可复现性
> 审查代理：5 并行代理（code-reviewer / python-reviewer / web-reviewer / security-reviewer / general-purpose）

---

## 摘要

| 维度 | CRITICAL | HIGH | MEDIUM | LOW | 总数 |
|------|---------|------|--------|-----|------|
| 项目结构 | 2 | 5 | 7 | 5 | 19 |
| Python 代码质量 | 5 | 16 | 9 | 0 | 30 |
| Web 可视化 | 2 | 1 | 3 | 8 | 14 |
| 研究可复现性 | 3 | 3 | 12 | 7 | 25 |
| 合规与安全 | 2 | 6 | 8 | 4 | 20 |
| **总计（去重）** | **11** | **24** | **28** | **18** | **~81** |

---

## 一、🔴 CRITICAL — 必须立即修复

### C1. 双重 SQLite 数据库存在数据漂移风险
- **文件**: `linguaGraph.db` (根目录) vs `survey_pipeline/linguaGraph.db`
- **来源**: 结构审查
- **问题**: 两个独立副本，如果各自写入将导致数据不一致
- **修复**: 删除 `survey_pipeline/linguaGraph.db`，统一使用根目录数据库路径

### C2. `.claude/settings.json` 环境变量路径指向不存在目录
- **文件**: `.claude/settings.json`
- **来源**: 结构审查
- **问题**: `LINGUAGRAPH_DB_PATH` 等变量指向 `02-项目规划/`，但该目录不存在
- **修复**: 更新路径为实际目录

### C3. SQL 注入风险（f-string 拼接）
- **文件**: `survey_pipeline/clean_data.py:65,132`
- **来源**: Python 审查
- **问题**: `f"WHERE quality_flag='{flag}'"` — 变量直接拼入 SQL
- **修复**: 改用参数化查询 `WHERE quality_flag=?`

### C4. 多处 `except: pass` 静默吞噬异常
- **文件**: `src/providers/local.py:117,137,144` · `research/generate_city_data.py:116`
- **来源**: Python 审查
- **问题**: 裸 `except` 捕获包括 `KeyboardInterrupt` 在内的所有异常
- **修复**: 改为 `except Exception:` 并添加日志

### C5. 两处 LDS 公式定义不一致
- **文件**: `docs/methodology.md` vs `docs/cognitive_metrics_framework.md`
- **来源**: 研究可复现性审查
- **问题**: `methodology.md` 定义 3 分量平均 LDS，`cognitive_metrics_framework.md` 定义纯 Jaccard LDS
- **修复**: 统一为 3 分量 LDS（与 `src/scoring.py` 实现一致）

### C6. 全代码库零随机种子设置
- **来源**: 研究可复现性审查
- **问题**: `random.seed` / `np.random.seed` / `torch.manual_seed` 全仓库零出现
- **影响**: 自举置信区间不可复现（`src/scoring.py:237-298`）、LLM 调用不可复现
- **修复**: 每个入口点设置随机种子

### C7. 多重比较校正未实现
- **来源**: 研究可复现性审查
- **问题**: 实验设计文档要求 BH-FDR（q=0.05）或 Bonferroni，但零个分析脚本实现
- **修复**: `scripts/bwki_analysis.py` 中添加 `statsmodels.stats.multitest.multipletests`

### C8. CognitiveSpace 45K 内联数据完全冗余
- **文件**: `cognitive-space/web/index.html:179-45249`
- **来源**: Web 审查
- **问题**: `COGNITIVE_DATA` 内联 JSON 块（574 节点、45K 行）从不会被使用，因为 `data.js` 中的 `COGNITIVE_DATA_EXT` 优先
- **修复**: 删除内联数据块，文件可从 45678→~500 行

### C9. `v1_baseline.html` 无数据源，静默崩溃
- **文件**: `cognitive-space/web/v1_baseline.html`
- **来源**: Web 审查
- **问题**: 未加载 `data.js` 也无内联 `COGNITIVE_DATA`，页面空白但无错误提示
- **修复**: 添加 `<script src="data.js">` 或嵌入最小数据

### C10. 参与者数据在 Git 中被追踪
- **文件**: `participant_data/pilot_v1/` · `pilot_raw/`
- **来源**: 合规审查
- **问题**: 伪匿名化数据（年龄组、语言、自由文本）已被 Git 追踪，可能足以重新识别个人
- **修复**: 加入 `.gitignore`，`git rm --cached`

### C11. 知情同意书占位符未填写
- **文件**: `docs/ethics/consent_{zh,en,de}.md` · `gdpr_package.md`
- **来源**: 合规审查
- **问题**: `[Name]` 和 `[Email]` 占位符在所有三语同意书中未替换
- **修复**: 填写实际数据控制者姓名和联系方式

---

## 二、🟠 HIGH — 应在提交前修复

### H1. 无 `pyproject.toml` / `setup.py`
- **来源**: 结构审查
- **建议**: 添加 `pyproject.toml` 以支持 `pip install -e .` 并统一工具配置

### H2. 无 `.vscode/settings.json`
- **来源**: 结构审查
- **建议**: 添加 IDE 配置（ruff、black、pytest 集成）

### H3. 无 pytest 配置，测试文件使用脆弱的 `sys.path.insert(0,...)`
- **来源**: 结构审查
- **问题**: 所有测试文件手动修改 `sys.path`
- **修复**: 添加 `pyproject.toml` 设置 `pythonpath = ["src"]`，移除所有 `sys.path.insert`

### H4. `output/` 和 `outputs/` 并存
- **来源**: 结构审查
- **问题**: 两个输出目录用途重叠
- **修复**: 合并到 `outputs/`，更新 `config/config.yaml`

### H5. `logs/` 目录不存在但日志配置引用
- **来源**: 结构审查
- **问题**: `config/config.yaml` 指定 `logs/linguagraph.log`，但 `logs/` 不存在
- **修复**: 创建 `logs/.gitkeep` 或改路径为 `outputs/linguagraph.log`

### H6. `src/main.py` 使用平面相对导入
- **来源**: 结构审查
- **问题**: `from extract import ...` 仅在 `src/` 为工作目录时有效
- **修复**: 使用 `from src.extract import ...`

### H7. 多数函数缺少类型标注（17+ 文件）
- **来源**: Python 审查
- **问题**: `src/extract.py`、`scripts/simulate_baseline.py` 等大量函数无类型标注
- **影响**: 降低代码可维护性，IDE 无法提供类型提示

### H8. `sys.path.insert(0, ...)` 散布全仓库
- **来源**: Python 审查
- **问题**: 9+ 个文件各自插入路径
- **修复**: 统一通过 `pip install -e .` 或 `PYTHONPATH` 管理

### H9. 全仓库 676 处 `print()` 替代 `logging`
- **来源**: Python 审查
- **问题**: `scripts/` 和 `survey_pipeline/` 几乎全部使用 `print()`，`logging` 存在但未被使用
- **影响**: 无法按级别过滤日志、无法输出到文件

### H10. `build_graph()` 三重复制
- **来源**: Python 审查
- **文件**: `src/graph.py` · `survey_pipeline/run_lds.py` · `workbench/process.py`
- **修复**: 统一调用 `src/graph.build_graph()`

### H11. 配置散布——硬编码模型参数多处定义
- **来源**: Python 审查
- **问题**: `survey_pipeline/config.py`、`src/providers/*.py`、`scripts/pipeline_v1.py` 各自定义模型 URL/名称
- **修复**: 统一到 `config/config.yaml`

### H12. 实验设计目标不一致（30 vs 60）
- **来源**: 合规审查
- **问题**: `docs/experiment-design.md` 写 "60+ participants"，但 README 和 CLAUDE.md 写 30 人
- **修复**: 统一为 30 人设计

### H13. `MODEL_CARD.md` YAML 元数据损坏
- **来源**: 合规审查
- **问题**: `engression: apache-2.0` 应为 `license: apache-2.0`
- **修复**: 修正 YAML 字段

### H14. `CITATION.cff` ORCID 未填写
- **来源**: 合规审查
- **问题**: `orcid: "https://orcid.org/"` 缺少实际 ID
- **修复**: 填写有效 ORCID 或删除字段

### H15. 两份不同的同意书并存
- **来源**: 合规审查
- **问题**: `data/consent_form.md`（旧版）与 `docs/ethics/`（新版）不一致
- **修复**: 删除 `data/consent_form.md`

### H16. `docs/ethics/consent_zh.md` 命名与内容不匹配
- **来源**: 合规审查
- **问题**: 文件名暗示仅中文同意书，但实际包含完整 GDPR 数据包
- **修复**: 提取独立中文同意书或重命名

### H17. Gold Dataset 仅定义 schema，未物化
- **来源**: 研究可复现性审查
- **问题**: 6 个冻结条件中 0 个完成，标注文件实际不存在
- **修复**: 完成标注或降低声明

### H18. 无预注册
- **来源**: 研究可复现性审查
- **问题**: 无时间戳分析计划或预注册
- **建议**: 在实验设计文档中添加时间戳声明

### H19. 无伦理委员会批号
- **来源**: 研究可复现性审查
- **建议**: 记录 BWKI 机构审查豁免或添加伦理批准号

### H20. 无数据可用性声明
- **来源**: 研究可复现性审查
- **问题**: 无 DOI、Zenodo、OSF 仓库
- **修复**: 在方法论文档中添加声明

### H21. Flask debug 模式开启
- **文件**: `workbench/app.py:118`
- **来源**: Web 审查
- **问题**: `app.run(debug=True)` 启用 Werkzeug 调试器
- **修复**: 改为 `debug=False`

### H22. 例外详情泄露给客户端
- **文件**: `workbench/server.py:62`
- **来源**: Web 审查
- **问题**: `return f"Processing error: {e}", 500` 泄露完整异常信息
- **修复**: 改用 `logger.exception()` + 通用错误消息

### H23. 无预注册
- **来源**: 研究可复现性审查（重复 H18，去重后计为 1 项）

### H24. 无数据可用性声明
- **来源**: 研究可复现性审查（重复 H20，去重后计为 1 项）

---

## 三、🟡 MEDIUM — 考虑修复

> 以下为中等严重性发现的摘要。完整列表见各代理原始输出。

### 项目结构
- `src/main.py` `run_pipeline()` 默认 domain="calculus" 但实际使用 "social_issues"
- `tests/` 中包含非测试分析脚本（`analyze_results.py`、`evaluate_survey.py`）
- `pilot_pipeline.py`（402 行）和 `simulate_baseline.py`（558 行）超行数限制
- 无 `.env.example` 文件
- `cognitive-space/config/expert_graphs/` 与 `config/expert_graphs/` 重复
- `src/archive/` 含死代码但无 `__init__.py`

### Web 可视化
- XSS 风险：`showDetail()` 使用 `innerHTML` 展示节点数据
- 呼吸动画每帧重写 574 节点 val
- 全局变量泄漏 + 未移除事件监听器
- exception 详情泄露给客户端（中等并同时为 H22）

### 合规
- `participant_data/` `.gitignore` 覆盖不全
- `participant_manager.py` delete 遗漏 `graphs` 表级联删除
- 同意书未提及 BWKI 特定数据使用
- `external/CoCo-Ex` 缺少 NOTICE 文件

### 研究可复现性
- LDS 0.3/0.7 阈值无文献支持
- GED 降级到 0.5 未在文档中说明
- 功率分析不完整（未计算 n=10 时的最小可检测效应量）
- 无单命令全管线复现（无 Makefile）
- 依赖版本未锁定（`>=` 而非 `==`）

---

## 四、🟢 LOW — 锦上添花

- `_archive/` 含 `.nojekyll` 等 GitHub Pages 残留
- 认知空间图无 ARIA 标签、字体偏小
- 速度计量条可能超出 100%
- `open.bat` 无注释说明用途
- `consent_en.md` 编号重复
- `RESEARCH_RULES.md` 仅中文
- `src/main.py` 等处使用 emoji 输出
- 无 `.python-version` 文件
- 认知空间仅一个响应式断点
- 字典顺序依赖的关系提取

---

## 五、✅ 通过项

| 检查项 | 结果 |
|--------|------|
| 硬编码密钥/密码 | ✅ 无，全部来自环境变量 |
| eval/exec 使用 | ✅ 未使用 |
| shell=True | ✅ 未使用 |
| .env 文件入版本库 | ✅ 已被 `.gitignore` 排除 |
| 参考文献/引用 | ✅ 88+ 篇论文，CITATION.cff 格式基本正确 |
| GDPR 删除权 | ✅ `participant_manager.py` 实现 Art. 17 |
| 数据保留政策 | ✅ 在 `gdpr_package.md` 中记录 |
| 数据库设计 | ✅ 8 表，外键+唯一约束+索引 |
| Provider 抽象层 | ✅ TaskRequest→Router→Provider 清晰分层 |

---

## 六、修复优先级建议

### 第 1 批 — 立即（BWKI 提交前必须）
```
P0-C1  → 统一 SQLite 数据库路径
P0-C2  → 修复 settings.json 路径
P0-C3  → 修复 SQL 注入（参数化查询）
P0-C4  → 修复裸 except
P0-C5  → 统一 LDS 公式定义文档
P0-C6  → 添加随机种子设置
P0-C7  → 实现多重比较校正
P0-C8  → 删除 45K 冗余内联数据
P0-C9  → 修复 v1_baseline.html 数据源
P0-C10 → 从 Git 移除参与者原始数据
P0-C11 → 填写同意书占位符
```

### 第 2 批 — 高优先级（提交前完成）
```
P1-H1  → 添加 pyproject.toml
P1-H4  → 合并 output → outputs
P1-H12 → 统一实验设计数字（30 vs 60）
P1-H13 → 修复 MODEL_CARD.md YAML
P1-H14 → 填写 ORCID
P1-H15 → 删除旧版 consent_form.md
P1-H21 → 关闭 Flask debug 模式
P1-H22 → 修复异常信息泄露
```

### 第 3 批 — 中等（里程碑 v0.1 前）
```
P2-H7  → 添加类型标注
P2-H9  → print() → logging 迁移
P2-H10 → build_graph 统一
P2-H11 → 配置集中化
P2-H17 → Gold Dataset 物化
P2-H20 → 数据可用性声明
```

---

## 七、代理执行记录

| 代理 | 类型 | 用时 | 文件检查数 | 发现数 |
|------|------|------|-----------|--------|
| 结构审查 | code-reviewer | 217s | 91 | 19 |
| Python 审查 | python-reviewer | 263s | ~50 | 30 |
| Web 审查 | web-reviewer | 262s | 5 | 14 |
| 合规审查 | security-reviewer | 524s | ~60 | 20 |
| 可复现性审查 | general-purpose | 225s | ~30 | 25 |

---

*报告生成：2026-06-22 · LinguaGraph BWKI 2026*
