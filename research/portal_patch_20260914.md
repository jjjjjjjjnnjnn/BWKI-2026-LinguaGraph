# Portal 增量内容补丁（2026-09-14，只新增本文件，不改门户）

> 来源：`research/two_tier_benchmark_20260914.md`、`research/limitations_20260914.md`、`research/human_vs_machine_20260914.md`
> 目标：`cognitive-space/portal/index.html`（源站；`_deploy/portal/index.html` 为构建产物，同步构建时带出）
> 用法：人工复制各片段到指定锚点后本地预览，确认无样式冲突再提交。今日只写补丁，不执行插入。
> 口径：数字只许照抄本文件；向量层与图谱层只比序结构，不比数值。

## 插入总览

| 片段 | 内容 | 插入位置（锚点） | 禁语检查 |
|---|---|---|---|
| A | Two-Tier 对照区 | `section#finding-c` 结束 `</section>` 之后、`<!-- FINDING D -->` 之前（ Finding C 与 Finding D 之间独立小节） | 通过（无"绝对无错/零幻觉/已冻结"） |
| B | Limitations 三段增补卡 | `section#limitations` 内 `.card-grid` 末尾（第 6 张卡之后、`</div></section>` 之前），以独立三张卡追加 | 通过（同上） |
| C | 人文"证伪探针"话术卡 | `section#finding-e` 表格区之后、`section#cognitivespace` 之前（Finding E 末尾追加，或独立小节插在二者之间） | 通过（同上） |

---

## 片段 A — Two-Tier 对照区（HTML，可直接粘贴）

<!-- 插入位置：section#finding-c 之后、Finding D 之前。独立 section，新 id="two-tier"，不改动现有 section。 -->
<!-- 行数见文件末尾统计。禁语检查：通过（无"绝对无错/零幻觉/已冻结"）。措辞上限：只许"未复现序结构"，不许"向量验证/证实了 LDS-K"。 -->

```html
<section id="two-tier" class="fade-in">
  <div class="finding-card" style="border-left:4px solid #0e7490">
    <h3><i class="bi bi-layers" style="color:#0e7490"></i> <span>Textbook Pedagogy vs Latent Model Representations (Two-Tier, 2026-09-14)</span></h3>
    <div class="lead">Open-weight vectors compress three pairs into a 0.48&ndash;0.52 narrow band (spread 0.0445) and do not reproduce the structured split of textbook LDS-K (spread 0.419, zh-de 0.519 &#8810; EN-involved &asymp;0.93). The two tiers measure different things.</div>
    <div class="table-container" style="margin:16px 0;overflow-x:auto">
      <table style="width:100%;border-collapse:collapse;font-size:.85rem">
        <thead>
          <tr style="background:var(--surface2);border-bottom:2px solid #0e7490">
            <th style="padding:8px 12px;text-align:left">Dimension</th>
            <th style="padding:8px 12px;text-align:left">Tier-1 Textbook explicit graph (main evidence)</th>
            <th style="padding:8px 12px;text-align:left">Tier-2 Latent vectors (control baseline, this batch)</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom:1px solid var(--surface2)">
            <td style="padding:8px 12px"><strong>Source</strong></td>
            <td style="padding:8px 12px">Textbook concept/relation tables (68 files, 741 concepts / 665 relations, human + multi-model audit)</td>
            <td style="padding:8px 12px">Open-weight embeddings of the same concept names (nomic-embed-text-v1.5, 768 dims, 934 entries, 434 primary pairs)</td>
          </tr>
          <tr style="border-bottom:1px solid var(--surface2)">
            <td style="padding:8px 12px"><strong>What is measured</strong></td>
            <td style="padding:8px 12px">Curriculum structure: GED similarity + node/edge Jaccard synthesis ("what is taught, how it connects")</td>
            <td style="padding:8px 12px">Distributional paraphrase proximity: cosine distance of synonymous cross-lingual names ("how similar it sounds in pretraining")</td>
          </tr>
          <tr style="border-bottom:1px solid var(--surface2)">
            <td style="padding:8px 12px"><strong>Topology</strong></td>
            <td style="padding:8px 12px">Structured, high variance: spread 0.419; zh-de 0.519 far below EN-involved &asymp;0.93 (0.934 / 0.938)</td>
            <td style="padding:8px 12px">Uniform, low variance: spread 0.0445; overall 0.5029&plusmn;0.1058; zh-de 0.4804 (n=65) / zh-en 0.5249 (n=184) / de-en 0.4888 (n=185)</td>
          </tr>
          <tr style="border-bottom:1px solid var(--surface2)">
            <td style="padding:8px 12px"><strong>Interpretability</strong></td>
            <td style="padding:8px 12px">High: traceable to concepts / edges / dangling refs (51 global unresolved, see blue-team defense)</td>
            <td style="padding:8px 12px">Low: a single value is not traceable to a curriculum fact; distribution-level statements only</td>
          </tr>
          <tr>
            <td style="padding:8px 12px"><strong>Role</strong></td>
            <td style="padding:8px 12px"><strong>Main evidence</strong>: carries the macro language-separability signal (LDS-C, p&lt;0.004)</td>
            <td style="padding:8px 12px"><strong>Control baseline (falsification probe)</strong>: if an effect exists at graph level but vanishes at vector level, it is curriculum structure, not generic semantics. Never a standalone conclusion, never interchangeable.</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p style="margin-top:8px"><strong>Key sentence:</strong> open-weight vector space compresses the three synonymous-pair distances into the 0.48&ndash;0.52 narrow band (spread 0.0445) and does not reproduce the structured split of textbook LDS-K (spread 0.419, zh-de 0.519 &#8810; EN-involved &asymp;0.93) &mdash; the graph is the main evidence for curriculum structure, vectors are the control baseline for distributional proximity; complementary, not interchangeable.</p>
    <p class="honesty">Scale warning: cosine distance and 1 &minus; mean(GED_sim, node/edge Jaccard) are different quantities &mdash; compare rank order only, never raw values. The zh-de closeness (&minus;0.04) is a coincidence of scales; do not report "vectors confirm the zh-de LDS-K value". Reproduce: <span class="mono">python scripts/tools/openweight_embed_audit.py --batch 32</span> (LM Studio online).</p>
    <div class="meta"><span class="tag tag-cyan">Tier-1: LDS-K 0.519 / 0.934 / 0.938</span> <span class="tag tag-blue">Tier-2: 0.4804 / 0.5249 / 0.4888</span> <span class="tag tag-yellow">Source: research/two_tier_benchmark_20260914.md</span></div>
  </div>
</section>
```

---

## 片段 B — Limitations 三段增补卡（HTML，可直接粘贴）

<!-- 插入位置：section#limitations 内 .card-grid 末尾追加三张卡（第 6 张卡之后）。不改现有 6 张卡。 -->
<!-- 行数见文件末尾统计。禁语检查：通过（无"绝对无错/零幻觉/已冻结"）。本片段含 temperature=0 与 500-perm p<0.004 防御话术原文。 -->

```html
<div class="card">
  <h3><i class="bi bi-scissors" style="color:var(--yellow)"></i> <span>Chunking boundaries (section-level granularity)</span></h3>
  <p>Textbook extraction chunks by section (<span class="mono">data/math_extractions/&lt;textbook&gt;_&lt;chapter&gt;_&lt;section&gt;.json</span>); cross-section co-reference is merged only at the alignment table, and edges pointing to concepts established elsewhere count as dangling (244 in-file / 51 unresolved cross-file, see blue-team D3). The bias is one-sided and conservative: node/edge Jaccard can only underestimate cross-lingual overlap and overestimate drift. Conclusions rest on "cross-lingual distance significantly above the null model" (margin floor 0.033 &gt; 0), not on absolute LDS values; chunking applies symmetrically across languages. Future work: chapter-level rerun as sensitivity analysis.</p>
  <div class="meta">Source: research/limitations_20260914.md L1</div>
</div>
<div class="card">
  <h3><i class="bi bi-type" style="color:var(--orange)"></i> <span>Hard-match penalty (normalization + exact alignment)</span></h3>
  <p>Audit and alignment use hard matching (lowercase + strip spaces/hyphens/underscores + &szlig;&rarr;ss + synonym map). Synonymous-but-differently-spelled pairs (e.g. Bayes-Formel vs Satz von Bayes) are penalized by construction; quantified sensitivity is single-digit (unresolved 50 vs 51, cross-file renaming 53 vs 38). The vector audit inherits the same constraint: of 219 alignment groups, 32 are surface-identical in all three languages and zh-de keeps only 65 effective pairs with the widest error bar (mean 0.4804, std 0.1274). Report normalization rules alongside every recall/LDS number; vector level stays distribution-level, no single-pair claims. Soft matching (embedding-threshold alignment) is future work with pre-registered thresholds.</p>
  <div class="meta">Source: research/limitations_20260914.md L2</div>
</div>
<div class="card">
  <h3><i class="bi bi-people" style="color:var(--pink)"></i> <span>Sparse annotation (N=8 pilot + alignment coverage) &middot; temperature=0 &middot; 500-perm p&lt;0.004</span></h3>
  <p>Human side: questionnaire implant is a pilot (N=8, social topics, LDS-C 0.704/0.727/0.751); the powered design is N=30 (86% power) and the human column is a shape placeholder with no significance claim. Alignment side: 219 aligned groups vs 359 unaligned concepts (coverage 37.9%); vector means describe the alignable subset (65/184/185 pairs), not the full curriculum. Reproducibility: judge calls use temperature=0, max_tokens=5 (single 0&ndash;5 digit); embeddings (<span class="mono">text-embedding-nomic-embed-text-v1.5</span>, dim=768 via LM Studio) have no sampling randomness. Defense line (read verbatim): macro separability uses 500 label permutations; p&lt;0.004 is the resolution limit (1/500), not tuning &mdash; ZH-DE 59/59 pass with margin 0.033&ndash;0.424 (floor positive); micro extraction noise and the macro test sit on different nulls, so the macro signal stands under current micro noise; the reverse reading (macro significance proves micro correctness) is explicitly forbidden.</p>
  <div class="meta">Rerun: <span class="mono">python scripts/tools/openweight_embed_audit.py --batch 32</span> &middot; Source: research/limitations_20260914.md L3 + perm defense</div>
</div>
```

---

## 片段 C — 人文"证伪探针"话术卡（HTML，可直接粘贴）

<!-- 插入位置：section#finding-e 末尾（表格区之后）或 section#finding-e 与 section#cognitivespace 之间的独立小节；推荐后者，新 id="falsification-probe"。 -->
<!-- 行数见文件末尾统计。禁语检查：通过（无"绝对无错/零幻觉/已冻结"）。pilot N=8 值仅作基线占位，今日不许报"探针通过/报警"。 -->

```html
<section id="falsification-probe" class="fade-in">
  <div class="finding-card" style="border-left:4px solid var(--purple)">
    <h3><i class="bi bi-eyedropper" style="color:var(--purple)"></i> <span>Humanities "falsification probe" (asymmetric, pre-registered logic)</span></h3>
    <div class="lead">The humanities/social-topic subset of the questionnaire is independent of the math graph and serves one-way falsification only &mdash; it can weaken the "curriculum-specific" claim but can never confirm the math result on its own.</div>
    <p><strong>Pass:</strong> math-domain LDS splits significantly while the humanities subset on the same pair does not (or flips sign) &rarr; supports "effect is math-curriculum-specific", against a generic-language-distance reading. <strong>Alarm:</strong> humanities subset reproduces the same split &rarr; math LDS significance stands (different test objects), but the "curriculum-specific" claim is downgraded to "shared cross-domain split" and the generic factor must be chased. <strong>Never:</strong> the humanities subset alone confirms the math conclusion (different domains, no transfer). Execute at N=30: full-set LDS-C first, then the humanities slice under the same pipeline and alpha with independent Bonferroni correction; report both tables side by side, never only the favorable half. Current state: pilot N=8 social-topic values (0.704/0.727/0.751) are implanted as the probe baseline placeholder &mdash; no pass/alarm call today.</p>
    <div class="table-container" style="margin:16px 0;overflow-x:auto">
      <table style="width:100%;border-collapse:collapse;font-size:.85rem">
        <thead>
          <tr style="background:var(--surface2);border-bottom:2px solid var(--purple)">
            <th style="padding:8px 12px;text-align:left">Reviewer question</th>
            <th style="padding:8px 12px;text-align:left">Standard answer (read verbatim)</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom:1px solid var(--surface2)">
            <td style="padding:8px 12px"><strong>N=8 and you report human conclusions?</strong></td>
            <td style="padding:8px 12px">No. N=8 is a pipeline demo placeholder; the powered design is N=30 (86% power for &Delta;LDS&gt;0). The human column registers shape only, no significance claim.</td>
          </tr>
          <tr style="border-bottom:1px solid var(--surface2)">
            <td style="padding:8px 12px"><strong>Vectors or graphs &mdash; which is right?</strong></td>
            <td style="padding:8px 12px">Not a right/wrong relation but two measurement layers: graphs measure curriculum structure (main evidence), vectors measure distributional proximity (control baseline). Vector uniformity is exactly what shows the graph's structure is not generic semantic noise.</td>
          </tr>
          <tr style="border-bottom:1px solid var(--surface2)">
            <td style="padding:8px 12px"><strong>zh-de 0.48 vs 0.52 &mdash; mutual confirmation?</strong></td>
            <td style="padding:8px 12px">No. Different scales (cosine distance vs GED+Jaccard synthesis); closeness is coincidence. Rank order only, never raw values.</td>
          </tr>
          <tr style="border-bottom:1px solid var(--surface2)">
            <td style="padding:8px 12px"><strong>What if the humanities probe alarms?</strong></td>
            <td style="padding:8px 12px">Downgrade "curriculum-specific" to "shared cross-domain", chase the generic factor; do not retract math LDS significance (different test objects, see blue-team D5 layering).</td>
          </tr>
          <tr style="border-bottom:1px solid var(--surface2)">
            <td style="padding:8px 12px"><strong>Is 500-perm p&lt;0.004 fished?</strong></td>
            <td style="padding:8px 12px">It is the resolution limit at 500 permutations (minimum reportable p); 59/59 pass with margin floor 0.033 &gt; 0; micro noise does not move the macro margin order (see blue_defense_20260914.md &sect;D5).</td>
          </tr>
          <tr>
            <td style="padding:8px 12px"><strong>temperature=0 reproducible?</strong></td>
            <td style="padding:8px 12px">Judge calls use temperature=0, max_tokens=5; embeddings have no sampling randomness (same word, same vector) &mdash; rerun the script for the same table; only an LM Studio model-version change forces re-registration.</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="meta"><span class="tag tag-purple">Probe baseline (pilot, placeholder): 0.704 / 0.727 / 0.751</span> <span class="tag tag-yellow">Source: research/human_vs_machine_20260914.md &sect;3&ndash;4</span></div>
  </div>
</section>
```

---

## 应用步骤（人工执行，不自动改门户）

1. 备份 `cognitive-space/portal/index.html`。
2. 按各片段注释的锚点粘贴（A → `#finding-c` 后；B → `#limitations .card-grid` 末；C → `#finding-e` 后）。
3. 本地打开门户预览三处渲染（表格横向滚动、honesty 条、meta 标签）。
4. 全文搜索禁语 `绝对无错 / 零幻觉 / 已冻结 / 全库已验证 / 探针通过`，命中即打回。
5. 确认数字与三份研究报告一致后，再走正常提交流程。

## 行数统计（片段 HTML 代码行数，以 ```html 块内为准）

- 片段 A（Two-Tier 对照区）：47 行（```html 块内第 24–70 行）
- 片段 B（Limitations 三段）：15 行（```html 块内第 81–95 行）
- 片段 C（证伪探针话术卡）：44 行（```html 块内第 106–149 行）

---

## v3 适用性核验（2026-09-15 追记，不改上文三片段）

- 结论：片段 A/B/C **不受共识 v3 影响，可按原步骤粘贴**。A 只含 Tier-1/Tier-2  frozen 数（LDS-K 0.519/0.934/0.938 vs 向量 0.4804/0.5249/0.4888），v3 改的是集成共识估计（inter 0.5401 等），不在同一层；B 的 L1–L3 与 C 的探针话术均无 v3 数字。
- 澄清（防混淆）：C 片段"temperature=0 reproducible"问答仅指**判官调用**（max_tokens=5 单数字）与**嵌入**（同词同向量），不指教材抽取——抽取在 temp=0 下仍有 ~40% run 间分歧（见 Limitations L4 追记）。粘贴后如评委追问抽取可复现性，照读 L4，不改 C 文案。
- 可选片段 D（L4/L5 两卡，按需粘贴，不强制）：见 `research/limitations_20260914.md` L4–L5 追记；HTML 化时沿用 `.card` 样式 + `Source: research/limitations_20260914.md L4/L5` 落款，禁语规则同 B。
