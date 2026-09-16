#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rule-based prune candidates for data/math_extractions/* (DAG validation).

只读 data（data/math_extractions/ 顶层 68 个 json，不含 merged/ 子目录），
只写 research/prune_candidates_20260914.json。不改数据、不碰禁区。

规则（全确定性，按归一化名 = strip + lower 生效）：
  R1 self_loop   : 归一化后 source == target                         -> 删边
  R2 bad_length  : 概念实体字符数 <2 或 >20                           -> 人工定
  R3 dangling    : 关系端点不在全库概念名并集中（51 个端点出现次数）  ->
                   (a) 字符数<2或>20 -> 删边（噪声标签）
                   (b) 全局出现频次>=2 -> 补概念（系统性缺概念）
                   (c) 别名/模糊可解 -> 纠目标（detail 给 suggest）
                   (d) 其余 -> 人工定
  R4 dup_relation : 同一文件内归一化 (source, target) 重复            -> 删边（去冗余）

另用 networkx 有向图做环检测（节点=概念名并集+端点，边=relations），
环结果只打印到 stdout（供 dag_validation 报告引用），不另写文件。

用法: python scripts/tools/rule_prune_candidates.py [--out research/prune_candidates_20260914.json]
"""
import argparse
import difflib
import json
from collections import Counter, defaultdict
from pathlib import Path

OUT_DEFAULT = "research/prune_candidates_20260914.json"
DATE_TAG = "20260914"


def norm(s) -> str:
    return str(s if s is not None else "").strip().lower()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT_DEFAULT)
    a = ap.parse_args()

    root = Path(__file__).resolve().parent.parent.parent
    data_dir = root / "data" / "math_extractions"
    out_path = (root / a.out).resolve()
    # 安全护栏：只允许写到 research/ 下，绝不写 data/
    if root / "research" not in out_path.parents and out_path.parent != root / "research":
        raise SystemExit(f"refuse to write outside research/: {out_path}")
    if "data" in out_path.parts[len(root.parts):]:
        raise SystemExit(f"refuse to write into data/: {out_path}")

    files = sorted(data_dir.glob("*.json"))  # 仅顶层，自动排除 merged/ 子目录
    concepts: set = set()          # 归一化概念名并集
    concept_files = defaultdict(set)  # norm name -> set(files)
    alias2canon: dict = {}         # 归一化别名 -> 归一化标准名
    edges = []                     # (src_norm, tgt_norm, file, rel_type, src_raw, tgt_raw, edge_idx)

    for fp in files:
        d = json.loads(fp.read_text(encoding="utf-8"))
        for c in d.get("extracted_concepts", []) or []:
            n = norm(c.get("name", ""))
            if not n:
                continue
            concepts.add(n)
            concept_files[n].add(fp.name)
            for al in c.get("aliases", []) or []:
                an = norm(al)
                if an and an not in alias2canon:
                    alias2canon[an] = n
        for i, r in enumerate(d.get("extracted_relations", []) or []):
            s_raw, t_raw = r.get("source", ""), r.get("target", "")
            s, t = norm(s_raw), norm(t_raw)
            if not s or not t:
                continue
            edges.append((s, t, fp.name, str(r.get("type", "")), str(s_raw), str(t_raw), i))

    cands = []

    # R1 自环
    for s, t, fn, typ, s_raw, t_raw, idx in edges:
        if s == t:
            cands.append({
                "file": fn,
                "kind": "self_loop",
                "detail": {"endpoint": s_raw, "endpoint_norm": s,
                           "rel_type": typ, "edge_index": idx},
                "action": "删边",
            })

    # R2 长度异常实体（针对概念并集）
    for n in sorted(concepts):
        if len(n) < 2 or len(n) > 20:
            cands.append({
                "file": sorted(concept_files[n])[0],
                "kind": "bad_length",
                "detail": {"entity": n, "chars": len(n),
                           "reason": "单字符" if len(n) < 2 else "超长短语",
                           "all_files": sorted(concept_files[n])},
                "action": "人工定",
            })

    # R3 全局悬空端点（逐条边、逐端点计数 => 51）
    dang_norms = []
    for s, t, fn, typ, s_raw, t_raw, idx in edges:
        if s not in concepts:
            dang_norms.append(s)
        if t not in concepts:
            dang_norms.append(t)
    freq = Counter(dang_norms)
    union_list = sorted(concepts)
    for s, t, fn, typ, s_raw, t_raw, idx in edges:
        for side, raw, nn in (("source", s_raw, s), ("target", t_raw, t)):
            if nn in concepts:
                continue
            if len(nn) < 2 or len(nn) > 20:
                act, sugg, why = "删边", None, "噪声标签：字符数<2或>20"
            elif freq[nn] >= 2:
                act, why = "补概念", f"系统性缺概念：全局出现{freq[nn]}次"
                sugg = alias2canon.get(nn)
            else:
                sugg = alias2canon.get(nn)
                if sugg is None:
                    fb = difflib.get_close_matches(nn, union_list, n=1, cutoff=0.85)
                    sugg = fb[0] if fb else None
                if sugg is not None:
                    act, why = "纠目标", "别名/近似可解"
                else:
                    act, why = "人工定", "无别名、无近似、单次出现"
            cands.append({
                "file": fn,
                "kind": "dangling",
                "detail": {"endpoint": raw, "endpoint_norm": nn, "side": side,
                           "rel_type": typ, "edge_index": idx,
                           "freq_global": freq[nn], "suggest": sugg, "reason": why},
                "action": act,
            })

    # R4 文件内重复关系对（归一化 (source, target)，忽略 type 差异但记录）
    by_key = defaultdict(list)
    for s, t, fn, typ, s_raw, t_raw, idx in edges:
        by_key[(fn, s, t)].append((typ, idx))
    for (fn, s, t), occ in sorted(by_key.items()):
        if len(occ) > 1:
            cands.append({
                "file": fn,
                "kind": "dup_relation",
                "detail": {"source_norm": s, "target_norm": t,
                           "occurrences": len(occ),
                           "rel_types": sorted({x[0] for x in occ}),
                           "edge_indices": sorted(x[1] for x in occ)},
                "action": "删边",
            })

    # 环检测（networkx 有向图），结果仅 stdout
    import networkx as nx
    G = nx.DiGraph()
    G.add_nodes_from(concepts)
    for s, t, *_ in edges:
        G.add_edge(s, t)
    raw_cycles = list(nx.simple_cycles(G))
    seen, uniq = set(), []
    for c in raw_cycles:
        key = frozenset(c)
        if key not in seen:
            seen.add(key)
            uniq.append(sorted(c))
    uniq.sort(key=lambda c: (len(c), c))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(cands, ensure_ascii=False, indent=2), encoding="utf-8")

    dang = [c for c in cands if c["kind"] == "dangling"]
    disp = Counter(c["action"] for c in dang)
    print(f"files={len(files)} concepts={len(concepts)} edges={len(edges)}")
    print(f"cycles_dedup={len(uniq)}")
    for c in uniq:
        print("cycle: " + " | ".join(c))
    print(f"cands_total={len(cands)} "
          f"self_loop={sum(1 for c in cands if c['kind']=='self_loop')} "
          f"bad_length={sum(1 for c in cands if c['kind']=='bad_length')} "
          f"dangling={len(dang)} "
          f"dup_relation={sum(1 for c in cands if c['kind']=='dup_relation')}")
    print("dangling_disp 补={} 纠={} 删={} 归档={}".format(
        disp.get("补概念", 0), disp.get("纠目标", 0),
        disp.get("删边", 0), disp.get("人工定", 0)))
    print(f"wrote {out_path.name}")


if __name__ == "__main__":
    main()
