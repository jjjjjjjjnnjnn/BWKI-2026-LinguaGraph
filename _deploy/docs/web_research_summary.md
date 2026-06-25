# CognitiveSpace Web研究汇总

## 研究日期
2026-06-16

## 研究目标
1. 收集相关论文和方法
2. 找到可用的数据集
3. 了解现有工具和框架
4. 为BWKI竞赛做准备

---

## 一、相关论文（18篇）

### 1. 双语教育与跨语言知识迁移

| 论文 | 作者 | 年份 | 关键发现 |
|------|------|------|----------|
| IndicEval: A Bilingual Indian Educational Evaluation Framework | Bharti et al. | 2026 | CoT提示能提高跨语言推理准确性；多语言退化仍是关键挑战 |
| Are LLMs Ready for Computer Science Education? | Gao et al. | 2026 | GPT-5在英语认证中表现最好，Qwen-Plus在中文中更好；所有模型在复杂认知任务中表现更差 |
| Position: LLMs Can be Good Tutors in English Education | Ye et al. | 2025 | LLMs可作为数据增强器、任务预测器和代理，实现个性化教育 |

### 2. 知识图谱构建

| 论文 | 作者 | 年份 | 关键发现 |
|------|------|------|----------|
| Instructor-Aligned Knowledge Graphs (InstructKG) | AlRabah et al. | 2026 | 自动从课程材料构建知识图谱，提取概念和学习依赖关系 |
| Beyond Static Question Banks | Wang et al. | 2026 | Generative GraphRAG框架：自动构建分层知识图谱+个性化练习生成 |
| Advanced Mathematics Learning Behavior Prediction | Liu & Li | 2026 | 构建分层知识图谱本体，自适应边权重 |
| Hey Chat, Can You Teach Me? | Tio et al. | 2026 | 构建先决条件知识图谱，使用PPO策略进行课程排序 |

### 3. 缺失知识检测

| 论文 | 作者 | 年份 | 关键发现 |
|------|------|------|----------|
| Capture-Calibrate-Coach (3C) | Li et al. | 2026 | 图基框架，85.21% AUC预测潜在感知状态 |
| TLCD: Transfer Learning for Cognitive Diagnosis | Wang et al. | 2025 | 跨学科迁移学习，处理知识系统差异 |
| KG-SoftMAP | Xu & Corter | 2026 | 使用知识图谱先验进行贝叶斯网络结构学习 |

### 4. 认知诊断模型

| 论文 | 作者 | 年份 | 关键发现 |
|------|------|------|----------|
| MERIT: Memory-Enhanced Retrieval | Li et al. | 2026 | 无训练框架，结合LLM推理+结构化记忆 |
| MetaCD: Meta Learning for Cognitive Diagnosis | Wu & Zheng | 2025 | 元学习+持续学习，处理长尾分布 |
| Neural-Symbolic Knowledge Tracing | Hooshyar et al. | 2026 | 集成符号知识，10%训练数据达到0.80 AUC |
| KCQRL: Automated Knowledge Concept Annotation | Ozyurt et al. | 2024 | LLM自动标注知识组件+对比学习 |
| Systematic Review of KT and LLMs | Cho et al. | 2024 | LLM增强KT模型，解决冷启动问题 |

### 5. 额外相关论文

| 论文 | 作者 | 年份 | 关键发现 |
|------|------|------|----------|
| DeepTutor: Agentic Personalized Tutoring | Zhao et al. | 2026 | 开源代理框架，个性化指标提升10.8% |
| AgentSchool: LLM-Powered Multi-Agent Simulation | Ye et al. | 2026 | 建模学习为状态转换，认知可成长的学生代理 |

---

## 二、可用数据集

### 教育知识图谱项目

| 项目 | Stars | URL | 说明 |
|------|-------|-----|------|
| EduData | 301 | github.com/bigdata-ustc/EduData | 综合教育数据集（ASSISTments, Junyi, OLI等） |
| pykt-toolkit | 406 | github.com/pykt-team/pykt-toolkit | 深度学习知识追踪模型基准测试 |
| education_knowledge_graph_app | 138 | github.com/jiangnanboy/education_knowledge_graph_app | K-12教育知识图谱（中文数据集） |
| ourvision-AI-education-kg | 65 | github.com/Goooaaal/ourvision-Artificial-intelligence-education-knowledge-graph | AI教育领域知识图谱（中文） |

### 双语/多语言数据集

| 数据集 | URL | 说明 |
|--------|-----|------|
| WikiEducational | huggingface.co/datasets | 多语言维基百科教育内容 |
| Junyi Academy | junyiacademy.org | 中英数学教育数据 |
| ASSISTments | sites.google.com/site/assistmentsdata/ | 学生回答数据 |
| EdNet | github.com/riiid/ednet | 大规模英语教育数据集（1.31亿交互） |

---

## 三、可用工具

### 认知诊断工具

| 工具 | Stars | URL | 说明 |
|------|-------|-----|------|
| EduStudio | 76 | github.com/HFUT-LEC/EduStudio | 统一学生认知建模库（CD+KT） |
| pyedmine | 80 | github.com/ZhijieXiong/pyedmine | 知识追踪、认知诊断、练习推荐算法 |
| Agent4Edu | 86 | github.com/bigdata-ustc/Agent4Edu | LLM代理生成学习者响应数据 |
| GDINA | 33 | github.com/Wenchao-Ma/GDINA | 广义DINA认知诊断模型（R包） |

### 知识图谱可视化

| 工具 | Stars | URL | 说明 |
|------|-------|-----|------|
| 3d-force-graph | 6100 | github.com/vasturiano/3d-force-graph | **最佳3D力导向图**，ThreeJS/WebGL |
| force-graph | 2000 | github.com/vasturiano/force-graph | 2D力导向图，HTML5 Canvas |
| d3-force | 2000 | github.com/d3/d3-force | D3.js核心力导向布局 |

### 3D知识图谱项目

| 项目 | URL | 说明 |
|------|-----|------|
| NodeScape | github.com/ArjunSNair00/NodeScape | AI驱动的3D知识图谱浏览器 |
| GraphMind | github.com/prutxvi/GraphMind | 3D AI知识图谱（FastAPI + React 19 + Three.js） |
| neural-graph-visualizer | github.com/cdeust/neural-graph-visualizer | 可配置3D知识图谱，bloom效果 |

---

## 四、BWKI竞赛信息

### 关键信息

| 项目 | 内容 |
|------|------|
| 官网 | bundeswettbewerb-ki.de |
| 主办方 | Plattform Lernende Systeme / acatech |
| 面向群体 | 德国9-13年级学生 |
| 频率 | 年度竞赛 |

### 历年获奖项目特点

- **2020**: NLP、计算机视觉、强化学习在教育中的应用
- **2021**: SmartFarm（精准农业CNN）、心理健康聊天机器人
- **2022**: GPT辅导、视障辅助工具
- **2023**: 情感识别、自动驾驶模拟、AI可持续发展

### 常用方法

- 深度学习（CNN、RNN、Transformer）
- NLP（情感分析、文本分类、命名实体识别）
- 计算机视觉（目标检测、图像分割）
- 强化学习
- 知识图谱
- 迁移学习

---

## 五、CognitiveSpace竞争优势分析

### 独特性

1. **跨语言认知断裂研究** - 极少有BWKI项目做这个方向
2. **MCL定义** - Missing Cognitive Links作为可计算表示
3. **加权MCL Score** - 考虑重要性和置信度
4. **双城可视化** - 中文城市vs德语城市
5. **时间维度** - 学习过程追踪

### 技术栈

| 组件 | 选择 | 原因 |
|------|------|------|
| LLM | 本地Qwen + OpenAI API | 成本低、可离线、可对比 |
| 图算法 | NetworkX | 成熟、可复现 |
| 可视化 | 3d-force-graph | 6100 stars、Three.js、易集成 |
| 评价 | 自建框架 | 符合研究需求 |

### 引用的论文

1. IndicEval (Bharti et al., 2026) - 跨语言评估
2. InstructKG (AlRabah et al., 2026) - 知识图谱构建
3. 3C (Li et al., 2026) - 缺失知识检测
4. MERIT (Li et al., 2026) - 认知诊断
5. KCQRL (Ozyurt et al., 2024) - LLM标注

---

## 六、下一步行动

### 立即执行

1. 下载EduData数据集，查看是否有中文数学数据
2. 安装3d-force-graph，测试3D可视化
3. 阅读InstructKG论文，学习知识图谱构建方法
4. 阅读3C论文，学习缺失知识检测方法

### 本周目标

1. 建立Gold Dataset（15人，人工标注）
2. 实现Pipeline v1.0（用真实LLM）
3. 测试3d-force-graph可视化
4. 撰写文献综述初稿

### 关键资源

| 资源 | URL | 用途 |
|------|-----|------|
| 3d-force-graph | npm install 3d-force-graph | 3D可视化 |
| EduData | github.com/bigdata-ustc/EduData | 数据集 |
| EduStudio | github.com/HFUT-LEC/EduStudio | 认知诊断 |
| awesome-student-cognitive-modeling | github.com/HFUT-LEC/awesome-student-cognitive-modeling | 论文列表 |
