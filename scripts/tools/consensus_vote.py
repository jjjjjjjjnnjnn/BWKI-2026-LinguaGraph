#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三源多数表决：mimo vs spark vs bailian（概念/关系）。

只读输入：
  data/math_extractions/<base>.json                      (mimo: extracted_concepts/extracted_relations)
  research/mimo_spark_audit/<base>.audit.json            (spark_concepts/spark_relations)
  research/bailian_audit/<base>.bailian.json             (parsed.extracted_concepts/parsed.extracted_relations)
只写输出（research/ 下）：
  research/consensus_20260914.json
  research/consensus_20260914.md
不改 data/，不写其他目录。

规则（按任务要求）：
  归一化：小写 + 去全部空白（re.sub(r'\\s+', '', s.lower())），概念按归一化名比对；
  概念多数表决：>=2 源认可 = 收录(accepted)；
  关系分级：有序端点对(归一化 source, 归一化 target)一致，>=2 源 = Solid，1 源 = Hypothetical（忽略 type 差异）；
  mimo 独有且他源无（sources=={mimo}）= 候选删/审(mimo_only)。

对象：12 个在 mimo_spark_audit 有 .audit.json 且在 mimo 存在顶层 json 的 basename
（其中 11 个另有 bailian 三源，1 个 zh_选修2-2_ch1_sec1.1 为 mimo+spark 两源）。

用法: python scripts/tools/consensus_vote.py [--out-json research/consensus_20260914.json --out-md research/consensus_20260914.md]
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

DATE_TAG = "20260914"
OUT_JSON_DEFAULT = f"research/consensus_{DATE_TAG}.json"
OUT_MD_DEFAULT = f"research/consensus_{DATE_TAG}.md"


def norm(s) -> str:
    return re.sub(r"\s+", "", str(s if s is not None else "").lower())


def concept_name(item) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        for k in ("name", "concept", "entity", "label", "text"):
            v = item.get(k)
            if isinstance(v, str) and v.strip():
                return v
        return ""
    return str(item)


def endpoint_name(v) -> str:
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        for k in ("name", "concept", "entity", "label", "text"):
            x = v.get(k)
            if isinstance(x, str) and x.strip():
                return x
        return ""
    return str(v) if v is not None else ""


def load_mimo(fp: Path):
    d = json.loads(fp.read_text(encoding="utf-8"))
    concepts = d.get("extracted_concepts", []) or []
    relations = d.get("extracted_relations", []) or []
    return concepts, relations


def load_spark_audit(fp: Path):
    d = json.loads(fp.read_text(encoding="utf-8"))
    concepts = d.get("spark_concepts", []) or []
    relations = d.get("spark_relations", []) or []
    return concepts, relations


def load_bailian(fp: Path):
    d = json.loads(fp.read_text(encoding="utf-8"))
    parsed = d.get("parsed", d) if isinstance(d, dict) else {}
    if not isinstance(parsed, dict):
        parsed = {}
    concepts = parsed.get("extracted_concepts", []) or []
    relations = parsed.get("extracted_relations", []) or []
    # 兼容变体键
    if not concepts:
        for k in ("concepts", "concepts_list"):
            if isinstance(parsed.get(k), list):
                concepts = parsed[k]
                break
    if not relations:
        for k in ("relations", "relations_list"):
            if isinstance(parsed.get(k), list):
                relations = parsed[k]
                break
    return concepts, relations


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-json", default=OUT_JSON_DEFAULT)
    ap.add_argument("--out-md", default=OUT_MD_DEFAULT)
    a = ap.parse_args()

    root = Path(__file__).resolve().parent.parent.parent
    mimo_dir = root / "data" / "math_extractions"
    spark_dir = root / "research" / "mimo_spark_audit"
    bailian_dir = root / "research" / "bailian_audit"

    out_json = (root / a.out_json).resolve()
    out_md = (root / a.out_md).resolve()
    for p in (out_json, out_md):
        if root / "research" not in p.parents and p.parent != root / "research":
            raise SystemExit(f"refuse to write outside research/: {p}")

    # 发现 12 个 basename：spark audit ∩ mimo 顶层
    spark_bases = sorted(p.name[:-len(".audit.json")] for p in spark_dir.glob("*.audit.json"))
    bases = [b for b in spark_bases if (mimo_dir / f"{b}.json").is_file()]
    if len(bases) != 12:
        print(f"WARN: expected 12 basenames, got {len(bases)}: {bases}")

    files_out = []
    tot_accepted = tot_solid = tot_hypo = tot_mimo_only = 0

    for base in bases:
        mimo_c_raw, mimo_r_raw = load_mimo(mimo_dir / f"{base}.json")
        spark_c_raw, spark_r_raw = load_spark_audit(spark_dir / f"{base}.audit.json")
        bpath = bailian_dir / f"{base}.bailian.json"
        has_bailian = bpath.is_file()
        if has_bailian:
            bai_c_raw, bai_r_raw = load_bailian(bpath)
        else:
            bai_c_raw, bai_r_raw = [], []

        # ---- 概念 ----
        cmap: dict = {}  # norm -> {"display": str, "sources": set, "raw": {src: original}}
        src_lists = [("mimo", mimo_c_raw), ("spark", spark_c_raw)]
        if has_bailian:
            src_lists.append(("bailian", bai_c_raw))
        per_src_concept_n = {}
        for src, raw_list in src_lists:
            seen = set()
            for item in raw_list:
                name = concept_name(item)
                n = norm(name)
                if not n:
                    continue
                seen.add(n)
                e = cmap.setdefault(n, {"display": name.strip(), "sources": set(), "raw": {}})
                if src not in e["raw"]:
                    e["raw"][src] = name.strip()
                e["sources"].add(src)
            per_src_concept_n[src] = len(seen)

        accepted = sorted([n for n, e in cmap.items() if len(e["sources"]) >= 2])
        mimo_only = sorted([n for n, e in cmap.items() if e["sources"] == {"mimo"}])

        # ---- 关系（有序端点对，忽略 type）----
        rmap: dict = {}  # (ns, nt) -> {"src": display, "tgt": display, "sources": set}
        rel_src_lists = [("mimo", mimo_r_raw), ("spark", spark_r_raw)]
        if has_bailian:
            rel_src_lists.append(("bailian", bai_r_raw))
        per_src_rel_n = {}
        for src, raw_list in rel_src_lists:
            seen_pairs = set()
            for r in raw_list:
                if not isinstance(r, dict):
                    continue
                s_raw = endpoint_name(r.get("source", ""))
                t_raw = endpoint_name(r.get("target", ""))
                ns, nt = norm(s_raw), norm(t_raw)
                if not ns or not nt:
                    continue
                seen_pairs.add((ns, nt))
                e = rmap.setdefault((ns, nt), {"src": s_raw.strip(), "tgt": t_raw.strip(),
                                               "sources": set(), "types": set()})
                e["sources"].add(src)
                tp = str(r.get("type", "") or "")
                if tp:
                    e["types"].add(tp)
            per_src_rel_n[src] = len(seen_pairs)

        solid = sorted([list(k) for k, e in rmap.items() if len(e["sources"]) >= 2])
        hypo = sorted([list(k) for k, e in rmap.items() if len(e["sources"]) == 1])

        tot_accepted += len(accepted)
        tot_mimo_only += len(mimo_only)
        tot_solid += len(solid)
        tot_hypo += len(hypo)

        files_out.append({
            "basename": base,
            "n_sources": 3 if has_bailian else 2,
            "has_bailian": has_bailian,
            "counts": {
                "mimo_concepts": per_src_concept_n.get("mimo", 0),
                "spark_concepts": per_src_concept_n.get("spark", 0),
                "bailian_concepts": per_src_concept_n.get("bailian", 0) if has_bailian else 0,
                "accepted_concepts_ge2": len(accepted),
                "mimo_only_review": len(mimo_only),
                "mimo_relations": per_src_rel_n.get("mimo", 0),
                "spark_relations": per_src_rel_n.get("spark", 0),
                "bailian_relations": per_src_rel_n.get("bailian", 0) if has_bailian else 0,
                "solid_ge2": len(solid),
                "hypothetical_1src": len(hypo),
            },
            "accepted_concepts": [
                {"norm": n, "display": cmap[n]["display"], "sources": sorted(cmap[n]["sources"])}
                for n in accepted
            ],
            "mimo_only_review": [
                {"norm": n, "display": cmap[n]["display"]} for n in mimo_only
            ],
            "solid_relations": [
                {"source_norm": p[0], "target_norm": p[1],
                 "source_display": rmap[(p[0], p[1])]["src"],
                 "target_display": rmap[(p[0], p[1])]["tgt"],
                 "sources": sorted(rmap[(p[0], p[1])]["sources"])}
                for p in solid
            ],
            "hypothetical_relations": [
                {"source_norm": p[0], "target_norm": p[1],
                 "source_display": rmap[(p[0], p[1])]["src"],
                 "target_display": rmap[(p[0], p[1])]["tgt"],
                 "sources": sorted(rmap[(p[0], p[1])]["sources"])}
                for p in hypo
            ],
        })

    payload = {
        "meta": {
            "date": DATE_TAG,
            "method": "概念归一化=小写+去全部空白；概念>=2源=收录；关系有序端点对(归一化source,归一化target)一致>=2源=Solid，1源=Hypothetical（忽略type）；mimo独有(sources=={mimo})=候选删/审",
            "inputs": ["data/math_extractions/<base>.json",
                       "research/mimo_spark_audit/<base>.audit.json",
                       "research/bailian_audit/<base>.bailian.json"],
            "n_files": len(files_out),
            "basenames": [f["basename"] for f in files_out],
        },
        "totals": {
            "accepted_concepts_ge2": tot_accepted,
            "solid_relations": tot_solid,
            "hypothetical_relations": tot_hypo,
            "mimo_only_review": tot_mimo_only,
        },
        "files": files_out,
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- MD ----
    lines = [f"# 三源多数表决共识 {DATE_TAG}", "",
             "方法：概念归一化=小写+去全部空白；概念≥2源=收录；关系有序端点对一致≥2源=Solid，1源=Hypothetical（忽略 type）；mimo 独有且他源无=候选删/审。",
             f"输入：`data/math_extractions/`（mimo）、`research/mimo_spark_audit/*.audit.json`（spark）、`research/bailian_audit/*.bailian.json`（parsed）；对象=12 个有三源（或两源）的 basename（11×三源 + 1×两源 `zh_选修2-2_ch1_sec1.1`）。", "",
             "## 三类总数", "",
             f"- 收录概念（≥2源）：**{tot_accepted}**",
             f"- Solid 关系（≥2源）：**{tot_solid}**",
             f"- Hypothetical 关系（1源）：**{tot_hypo}**",
             f"- 候选删/审（mimo 独有）：**{tot_mimo_only}**", "",
             "## 分文件表", "",
             "| basename | 源数 | mimo概念 | spark概念 | bailian概念 | 收录概念≥2 | 候选删mimo独有 | mimo关系 | spark关系 | bailian关系 | Solid≥2 | Hypothetical=1 |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for f in files_out:
        c = f["counts"]
        lines.append(f"| {f['basename']} | {f['n_sources']} | {c['mimo_concepts']} | {c['spark_concepts']} | "
                     f"{c['bailian_concepts']} | {c['accepted_concepts_ge2']} | {c['mimo_only_review']} | "
                     f"{c['mimo_relations']} | {c['spark_relations']} | {c['bailian_relations']} | "
                     f"{c['solid_ge2']} | {c['hypothetical_1src']} |")
    lines += ["", f"合计：收录概念 {tot_accepted} / Solid {tot_solid} / Hypothetical {tot_hypo} / 候选删 {tot_mimo_only}。", "",
              f"明细见 `{OUT_JSON_DEFAULT}`（每文件含 accepted/mimo_only/solid/hypothetical 列表）。", ""]
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"files={len(files_out)} accepted={tot_accepted} solid={tot_solid} hypo={tot_hypo} mimo_only={tot_mimo_only}")
    print(f"wrote {out_json.name} + {out_md.name}")


if __name__ == "__main__":
    main()
