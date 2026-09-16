# Portal Redesign — Apple-style + inline explorables (2026-09-16)

## 1. 设计系统（全站唯一真源 `portal/tokens.css`）

浅色画布 #fff / 纸灰 #f5f5f7 交替 tile；墨 #1d1d1f；单蓝 #0066cc（indigo #1e3a8a 并入，
约 30 处文本链接一次到位）；17px 正文；56/40 标题负 tracking；pill 主按钮每屏 ≤1；
零阴影；editorial 行（≤980px 居中，发丝线分隔）取代卡片网格。viewer 3D 画布不动，
仅 chrome 换肤；cspace 同 tokens。

## 2. 文内可探索式（Bret Victor 式，三独立页已删）

- m1 A/B-Runs（temperature=0 非确定性）/ m2 Straβe 对齐流水线 / m3 LDS 滑杆（松手回弹
  0.519/0.933/0.938）/ m4 50-perm 直方图（p<0.004/floor 0.033）/ m5 59 绿点 vs 177 条
  （9 n.s.）——全部行内 Vanilla，无测验无进度。
- Finding C 反例抽屉：8 真概念组（#12…#54，id＋三语＋裁决一句）。
- Limitations l1–l6 行内"关掉我"：对应 finding 变暗＋误读警告，280ms 过渡。
- Curriculum 三解释诚实证据条（12.7%→95.4%，无投票）。

## 3. 步骤级溯源（10 个 <details>，默认收起）

每步/每主张：为什么一句＋数字链（输入→真实脚本→输出→SSOT 字段，m1/m2/m5 路径
已核为 scripts/math_graph_pipeline/* 与 scripts/run_dashscope_batch.py）＋GitHub 直链。
Mini-Labore 区保留为锚点索引（#methodology/#findings/#limitations），无独立页。

## 4. 回归（agent 独立复核）

numbers-gate PASS；portal_v2_check PASS（184 i18n/11 区/标签平衡）；
i18n 174 键三语零缺失；JS node --check 全过；banned 0；live 0.934 清零（含 viewer
detail 面板 0.934→0.933）；死链 0（v1 归档/历史文档除外）；行数 792≤900。

## 5. 附带

- B-agent 报告路径缩写问题：已核实落盘链为全路径，GitHub 链有效；虚报已记（以后
  chain 键须附 Glob 截图行）。
- v1.0 仍 block（H1/H3＋6 open 偏离，原判不变）。
