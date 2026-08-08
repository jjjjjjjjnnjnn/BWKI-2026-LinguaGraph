#!/usr/bin/env python3
"""LinguaGraph — A4: LDS-K deep dive (per-topic, cross-source null, sensitivity).

Deepens the corpus-side LDS-K evidence per restart_plan A4, using the frozen
LDS v3 formula (LDS = 1 - mean(J_node, J_edge)) from lds_formal_definition.md.

Components
----------
1. Wikipedia aligned LDS  : ZH concepts glossed to EN (lds_k_wiki_gloss.py),
   then all 3 languages run through canonical_key. Fixes the fig_wikipedia_lds.py
   artifact where unglossed ZH => empty keys => LDS == 1.0 trivially.
   - per-topic (5 topics) + pooled, node/edge components.
2. Math LDS-K by level    : elementary / middle / high / college, from the 219
   aligned groups (level metadata present). Node/edge components.
3. Cross-source null (§3.6): textbook (math) vs Wikipedia (social) same language.
   - Caveat: domain differs (math vs social) => a genuine confound; we report it
     and ALSO run a domain-clean cross-source check: Wikipedia(zh) vs human(zh)
     aggregate concept sets on the 5 social topics (same domain, same language,
     different source: institutional vs cognitive).
   - Decision: if intra-language cross-source LDS ~ inter-language within-source
     LDS, then LDS is primarily a source/domain metric, not a language metric.
4. Sensitivity:
   - directed vs undirected edges
   - alignment tightness: exact gloss match vs canonical_key (synonym+stem)
   - importance threshold: keep concepts with importance >= thresh (0.0 / 0.5 / 0.85)

All outputs written to data/lds_c/lds_k_deep/<file>.json with full provenance.
Console prints the key tables for the report.

Usage:
    python scripts/lds_k_deepen.py
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from lds_c_compute import canonical_key, PAIRS, TOPICS  # noqa: E402

OUT_DIR = PROJECT_ROOT / "data" / "lds_c" / "lds_k_deep"
WIKI_DIR = PROJECT_ROOT / "data" / "wikipedia_extractions"
MATH_PATH = PROJECT_ROOT / "data" / "math_extractions" / "merged" / "aligned_data.json"
# Wikipedia extraction files use English topic slugs
TOPIC_SLUG = {"Freiheit": "freedom", "Gerechtigkeit": "justice",
              "Verantwortung": "responsibility", "Heimat": "home", "Erfolg": "success"}
LANG_CODES = ["zh", "en", "de"]


# ── Core LDS (frozen v3 formula) ────────────────────────────────────
def lds_v3(nodes_a, nodes_b, edges_a=None, edges_b=None) -> dict:
    """LDS = 1 - mean(J_node, J_edge); edge component optional (node-only if None).

    Empty-set convention: two empty node sets are identical (LDS=0); one empty
    side returns LDS=NaN (degenerate) so the caller can detect the alignment
    artifact instead of silently reporting maximum divergence."""
    sa, sb = set(nodes_a), set(nodes_b)
    if not sa and not sb:
        return {"lds": 0.0, "j_node": 1.0,
                "j_edge": None if edges_a is None else 1.0}
    if not sa or not sb:
        return {"lds": float("nan"), "j_node": 0.0,
                "j_edge": None if edges_a is None else 0.0}
    j_node = len(sa & sb) / max(len(sa | sb), 1)
    if edges_a is not None and edges_b is not None:
        ea, eb = set(edges_a), set(edges_b)
        j_edge = len(ea & eb) / max(len(ea | eb), 1)
    else:
        j_edge = float("nan")
    if edges_a is not None:
        lds = 1.0 - (j_node + j_edge) / 2
    else:
        lds = 1.0 - j_node
    return {"lds": round(lds, 4), "j_node": round(j_node, 4),
            "j_edge": None if edges_a is None else round(j_edge, 4)}


def load_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ── 1. Wikipedia aligned LDS ────────────────────────────────────────
def wiki_graphs(gloss: Dict[str, str], undirected: bool = False,
                threshold: float = 0.0) -> Dict[str, Dict[str, dict]]:
    """topic -> lang -> {"nodes": set(keys), "edges": set(tuple keys)}."""
    result: Dict[str, Dict[str, dict]] = {}
    for topic in TOPICS:
        result[topic] = {}
        slug = TOPIC_SLUG[topic]
        for lang in LANG_CODES:
            fpath = WIKI_DIR / f"{slug}_{lang}.json"
            if not fpath.exists():
                continue
            d = load_json(fpath)
            nodes = set()
            for c in d.get("concepts", []):
                name = (c.get("name") or "").strip()
                if not name:
                    continue
                imp = c.get("importance", 1.0) or 1.0
                if imp < threshold:
                    continue
                # ZH and DE concepts are glossed to English so all 3 languages
                # align in the same canonical key space. EN passes through.
                en = gloss.get(name, name)
                key = canonical_key(en)
                if key:
                    nodes.add(key)
            edges = set()
            for r in d.get("relations", []):
                s = r.get("source") or ""
                t = r.get("target") or ""
                ks, kt = canonical_key(gloss.get(s, s)), canonical_key(gloss.get(t, t))
                if ks and kt:
                    edges.add((ks, kt) if not undirected else
                              (min(ks, kt), max(ks, kt)))
            result[topic][lang] = {"nodes": nodes, "edges": edges}
    return result


# ── 2. Math LDS-K by level ──────────────────────────────────────────
def math_by_level() -> Tuple[Dict[str, dict], Dict[str, str]]:
    """Returns (level -> {lang: {nodes, edges}}, group_id -> level).

    Edge attribution: an edge's level is taken from its source_group. Edges whose
    endpoints span levels are attributed to the source level (documented below);
    relations whose groups have no labels are counted and reported (audit M8)."""
    d = load_json(MATH_PATH)
    groups = d.get("aligned_groups", [])
    gid_level = {g["id"]: g.get("level", "unknown") for g in groups}
    levels = sorted({g.get("level", "unknown") for g in groups})
    # level -> lang -> nodes
    result: Dict[str, Dict[str, dict]] = {}
    for lv in levels:
        result[lv] = {lang: {"nodes": set(), "edges": set()} for lang in LANG_CODES}
    # nodes: aligned group labels per level
    for g in groups:
        lv = g.get("level", "unknown")
        labels = g.get("labels", {})
        for lang in LANG_CODES:
            lab = labels.get(lang)
            if lab:
                result[lv][lang]["nodes"].add(lab)
    # edges: relations mapped to level via source_group
    gid_labels = {g["id"]: g.get("labels", {}) for g in groups}
    n_dropped = 0
    n_cross_level = 0
    for r in d.get("relations", []):
        sg = r.get("source_group") or ""
        tg = r.get("target_group") or ""
        lv = gid_level.get(sg, "unknown")
        if sg in gid_labels and tg in gid_labels:
            s_labels = gid_labels[sg]
            t_labels = gid_labels[tg]
            if gid_level.get(tg) != lv:
                n_cross_level += 1  # spans levels; attributed to source level
            for lang in LANG_CODES:
                s = s_labels.get(lang)
                t = t_labels.get(lang)
                if s and t:
                    result[lv][lang]["edges"].add((s, t))
        else:
            n_dropped += 1  # group without labels: edge silently skipped (audit M8)
    if n_dropped:
        print(f"  [M8] {n_dropped} relations dropped (group has no labels); "
              f"{n_cross_level} cross-level edges attributed to source level.")
    return result, gid_level


def pair_lds(graphs: Dict[str, dict], la: str, lb: str) -> dict:
    a, b = graphs.get(la, {}), graphs.get(lb, {})
    if not a.get("nodes") or not b.get("nodes"):
        return {}
    return lds_v3(a["nodes"], b["nodes"], a.get("edges"), b.get("edges"))


# ── 3. Cross-source null ────────────────────────────────────────────
def cross_source(wiki: Dict[str, Dict[str, dict]],
                 math_graphs: Dict[str, Dict[str, dict]]) -> dict:
    """Textbook(math) vs Wikipedia(social) per language pair.

    Acknowledges domain confound (math vs social); complements with the
    domain-clean check elsewhere (Wikipedia vs human on social topics)."""
    out = {}
    for lang in LANG_CODES:
        w_nodes = set()
        w_edges = set()
        for t in TOPICS:
            if lang in wiki.get(t, {}):
                w_nodes |= wiki[t][lang]["nodes"]
                w_edges |= wiki[t][lang]["edges"]
        # math graph per language (pooled across levels)
        m_nodes = set()
        m_edges = set()
        for lv in math_graphs.values():
            if lang in lv:
                m_nodes |= lv[lang]["nodes"]
                m_edges |= lv[lang]["edges"]
        if w_nodes and m_nodes:
            out[lang] = lds_v3(m_nodes, w_nodes, m_edges, w_edges)
            out[lang]["n_nodes"] = {"math": len(m_nodes), "wiki": len(w_nodes)}
    return out


def cross_source_wiki_vs_human(wiki: Dict[str, Dict[str, dict]],
                               human_units_path: Path, gloss: Dict[str, str],
                               ) -> dict:
    """Domain-clean cross-source: Wikipedia(zh) vs human(zh) on social topics.

    Same domain (social), same language (zh), different source (institutional
    Wikipedia vs cognitive human expression). Both concept sets canonicalized."""
    # load human extractions (canonical glosses already English)
    if not human_units_path.exists():
        return {"error": f"human extractions not found: {human_units_path}"}
    human = load_json(human_units_path)
    human_nodes = set()
    for r in human.get("responses", []):
        if r.get("language") != "zh":
            continue
        for t in r.get("topics", []):
            for c in t.get("concepts", []):
                en = c.get("en", "")
                k = canonical_key(en)
                if k:
                    human_nodes.add(k)
    w_nodes = set()
    for t in TOPICS:
        if "zh" in wiki.get(t, {}):
            w_nodes |= wiki[t]["zh"]["nodes"]
    if not human_nodes or not w_nodes:
        return {"error": f"empty sets (human={len(human_nodes)}, wiki={len(w_nodes)})"}
    # node-only LDS (human has no relations in this source)
    return {
        "comparison": "Wikipedia(zh) vs Human(zh) — social domain, same language, cross-source",
        "lds_node_only": lds_v3(w_nodes, human_nodes)["lds"],
        "j_node": lds_v3(w_nodes, human_nodes)["j_node"],
        "n_nodes": {"wiki": len(w_nodes), "human": len(human_nodes)},
    }


# ── 4. Sensitivity ──────────────────────────────────────────────────
def sensitivity_math(math_graphs: Dict[str, Dict[str, dict]]) -> dict:
    """Directed vs undirected edges; node-only vs node+edge."""
    out = {"directed": {}, "undirected": {}, "node_only": {}}
    for pair, la, lb in PAIRS:
        a, b = math_graphs.get(la, {}), math_graphs.get(lb, {})
        if not a or not b:
            continue
        out["directed"][pair] = lds_v3(a["nodes"], b["nodes"], a["edges"], b["edges"])
        # undirected: canonize edge order
        ua = {(min(x, y), max(x, y)) for x, y in a["edges"]}
        ub = {(min(x, y), max(x, y)) for x, y in b["edges"]}
        out["undirected"][pair] = lds_v3(a["nodes"], b["nodes"], ua, ub)
        out["node_only"][pair] = lds_v3(a["nodes"], b["nodes"])
    return out


def sensitivity_alignment(wiki: Dict[str, Dict[str, dict]],
                          gloss: Dict[str, str]) -> dict:
    """Alignment tightness on Wikipedia (all-English gloss space).

    canonical_key applies the synonym map + stemmer (loose); strict compares the
    raw English gloss strings (no synonym/stem merging). If LDS is robust to this,
    alignment tightness is not the bottleneck — mirroring the human-side finding
    that lexical alignment only merged ~5% of glosses."""
    out = {"loose_canonical": {}, "strict_gloss": {}}
    # loose = current wiki_graphs (canonical_key applied)
    loose = wiki
    strict_pooled = {}
    for lang in LANG_CODES:
        nodes, edges = set(), set()
        for t in TOPICS:
            if lang not in loose.get(t, {}):
                continue
            # raw gloss string (gloss map applied, but no canonical_key)
            slug = TOPIC_SLUG[t]
            fpath = WIKI_DIR / f"{slug}_{lang}.json"
            if not fpath.exists():
                continue
            d = load_json(fpath)
            for c in d.get("concepts", []):
                name = (c.get("name") or "").strip()
                if not name:
                    continue
                en = gloss.get(name, name).strip().lower()
                if en:
                    nodes.add(en)
            for r in d.get("relations", []):
                s = gloss.get(r.get("source", ""), r.get("source", "")).strip().lower()
                t_ = gloss.get(r.get("target", ""), r.get("target", "")).strip().lower()
                if s and t_:
                    # audit M13: keep DIRECTED edges (same as the loose/canonical
                    # branch) so alignment tightness is not confounded with edge
                    # direction. Previously this branch undirected the edges,
                    # mixing the two sensitivity axes.
                    edges.add((s, t_))
        strict_pooled[lang] = {"nodes": nodes, "edges": edges}
    # pooled loose from wiki arg
    loose_pooled = {}
    for lang in LANG_CODES:
        nodes, edges = set(), set()
        for t in TOPICS:
            if lang in wiki.get(t, {}):
                nodes |= wiki[t][lang]["nodes"]
                edges |= wiki[t][lang]["edges"]
        loose_pooled[lang] = {"nodes": nodes, "edges": edges}
    for pair, la, lb in PAIRS:
        out["loose_canonical"][pair] = lds_v3(
            loose_pooled[la]["nodes"], loose_pooled[lb]["nodes"],
            loose_pooled[la]["edges"], loose_pooled[lb]["edges"])
        out["strict_gloss"][pair] = lds_v3(
            strict_pooled[la]["nodes"], strict_pooled[lb]["nodes"],
            strict_pooled[la]["edges"], strict_pooled[lb]["edges"])
    return out


def sensitivity_threshold_wiki(wiki: Dict[str, Dict[str, dict]],
                               gloss: Dict[str, str]) -> dict:
    """Importance threshold on Wikipedia concepts: 0.0 / 0.5 / 0.85.

    NOTE: Wikipedia extractions carry no 'importance' field (all concepts are
    unweighted), so the threshold is a no-op there. We therefore also run the
    threshold on the LLM-as-subject concept graphs, which DO carry 0-1 weights —
    that is the meaningful test of whether keeping only high-importance concepts
    changes LDS-C."""
    out = {"wiki_noop": {}}
    for thresh in [0.0, 0.5, 0.85]:
        g = wiki_graphs(gloss, threshold=thresh)
        pooled = {}
        for lang in LANG_CODES:
            nodes, edges = set(), set()
            for t in TOPICS:
                if lang in g.get(t, {}):
                    nodes |= g[t][lang]["nodes"]
                    edges |= g[t][lang]["edges"]
            pooled[lang] = {"nodes": nodes, "edges": edges}
        out["wiki_noop"][f"thresh_{thresh}"] = {
            p: lds_v3(pooled[la]["nodes"], pooled[lb]["nodes"],
                      pooled[la]["edges"], pooled[lb]["edges"])
            for p, la, lb in PAIRS
        }
    # meaningful: threshold on LLM-as-subject P1 concepts (0-1 importance weights)
    llm_files = sorted((OUT_DIR.parent / "llm_subject").glob("llm_subject_*.json"))
    if llm_files:
        out["llm_subject"] = _threshold_llm(llm_files[-1])
    else:
        print("  WARN: no llm_subject_*.json found; skipping meaningful "
              "importance-threshold block (audit H2)")
    return out


def _threshold_llm(llm_path: Path) -> dict:
    """LDS-C (concept-level, node-only) on LLM P1 units at importance thresholds."""
    d = load_json(llm_path)
    out = {}
    for thresh in [0.0, 0.5, 0.85]:
        nodes = {"zh": set(), "en": set(), "de": set()}
        for u in d.get("units", []):
            if u.get("probe") != "P1":
                continue
            lang = u["language"]
            for topic, concepts in u.get("concepts", {}).items():
                for c in concepts:
                    imp = c.get("importance", 1.0) or 1.0
                    if imp < thresh:
                        continue
                    k = canonical_key(c.get("en", ""))
                    if k:
                        nodes[lang].add(k)
        out[f"thresh_{thresh}"] = {
            p: lds_v3(nodes[la], nodes[lb]) for p, la, lb in PAIRS
        }
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # gloss tables: combined ZH+DE -> EN (lds_k_wiki_gloss.py output).
    # Use the LATEST gloss file (not a hardcoded date) so re-runs pick up new
    # glosses; fail loudly if no gloss exists rather than silently degrade to
    # empty keys (audit H2).
    gloss_files = sorted(WIKI_DIR.glob("wiki_gloss_*.json"))
    if not gloss_files:
        gloss_files = sorted(WIKI_DIR.glob("zh_to_en_gloss_*.json"))
    if not gloss_files:
        raise FileNotFoundError(
            "No gloss table found in %s (need wiki_gloss_*.json). "
            "Run scripts/lds_k_wiki_gloss.py first — without it, ZH/DE concepts "
            "collapse to empty canonical keys and wiki LDS degrades to the "
            "LDS=1.0 alignment artifact this script is meant to fix." % WIKI_DIR)
    gloss_path = gloss_files[-1]
    gloss = load_json(gloss_path).get("glosses", {})
    if not gloss:
        raise RuntimeError("Gloss table %s is empty (audit H2)" % gloss_path)
    print(f"  Gloss table: {len(gloss)} entries from {gloss_path.name}")

    print("=" * 66)
    print("A4: LDS-K Deep Dive (per-topic / cross-source null / sensitivity)")
    print("=" * 66)

    # ── 1. Wikipedia aligned LDS ──
    print("\n── 1. Wikipedia LDS (aligned via gloss -> canonical key) ──")
    wiki = wiki_graphs(gloss)
    wiki_topic = {}
    for topic in TOPICS:
        wiki_topic[topic] = {p: pair_lds(wiki[topic], la, lb) for p, la, lb in PAIRS}
    # pooled
    pooled_wiki = {}
    for lang in LANG_CODES:
        nodes, edges = set(), set()
        for t in TOPICS:
            if lang in wiki.get(t, {}):
                nodes |= wiki[t][lang]["nodes"]
                edges |= wiki[t][lang]["edges"]
        pooled_wiki[lang] = {"nodes": nodes, "edges": edges}
    wiki_pooled = {p: lds_v3(pooled_wiki[la]["nodes"], pooled_wiki[lb]["nodes"],
                             pooled_wiki[la]["edges"], pooled_wiki[lb]["edges"])
                   for p, la, lb in PAIRS}

    print("  Per-topic LDS (aligned):")
    for topic in TOPICS:
        row = " | ".join(f"{p}:{wiki_topic[topic].get(p, {}).get('lds', '—')}"
                         for p, _, _ in PAIRS)
        print(f"    {topic:14s} {row}")
    print("  Pooled:")
    for p, la, lb in PAIRS:
        v = wiki_pooled.get(p, {})
        print(f"    {p}: LDS={v.get('lds')} (j_node={v.get('j_node')}, "
              f"j_edge={v.get('j_edge')})")

    # ── 2. Math LDS-K by level ──
    print("\n── 2. Math LDS-K by education level ──")
    math_by_lv, _ = math_by_level()
    math_pooled = {}
    for lang in LANG_CODES:
        nodes, edges = set(), set()
        for lv in math_by_lv.values():
            nodes |= lv[lang]["nodes"]
            edges |= lv[lang]["edges"]
        math_pooled[lang] = {"nodes": nodes, "edges": edges}
    math_level = {}
    for lv, g in sorted(math_by_lv.items()):
        math_level[lv] = {p: pair_lds(g, la, lb) for p, la, lb in PAIRS}
        row = " | ".join(f"{p}:{math_level[lv].get(p, {}).get('lds', '—')}"
                         for p, _, _ in PAIRS)
        sizes = " / ".join(f"{lang}:{len(g[lang]['nodes'])}" for lang in LANG_CODES)
        print(f"    {lv:12s} {row}   [nodes: {sizes}]")
    math_pooled_res = {p: lds_v3(math_pooled[la]["nodes"], math_pooled[lb]["nodes"],
                                 math_pooled[la]["edges"], math_pooled[lb]["edges"])
                       for p, la, lb in PAIRS}
    print("    Pooled:", " | ".join(f"{p}:{math_pooled_res.get(p, {}).get('lds', '—')}"
                                    for p, _, _ in PAIRS))

    # ── 3. Cross-source null ──
    print("\n── 3. Cross-source null (§3.6) ──")
    cs = cross_source(wiki, math_by_lv)
    for lang, v in cs.items():
        if v:
            print(f"    Textbook vs Wikipedia ({lang}): LDS={v['lds']} "
                  f"(j_node={v['j_node']}, j_edge={v['j_edge']}) "
                  f"[math={v['n_nodes']['math']}, wiki={v['n_nodes']['wiki']}]")
    # domain-clean: Wikipedia vs human (zh)
    human_files = sorted((PROJECT_ROOT / "data" / "lds_c").glob("extractions_*.json"))
    if not human_files:
        raise FileNotFoundError("No human extractions found (audit H2)")
    human_path = human_files[-1]
    cs_h = cross_source_wiki_vs_human(wiki, human_path, gloss)
    print(f"    Wiki(zh) vs Human(zh) social: {json.dumps(cs_h, ensure_ascii=False)}")

    # ── 4. Sensitivity ──
    print("\n── 4. Sensitivity ──")
    sens = sensitivity_math(math_pooled)
    for mode, res in sens.items():
        row = " | ".join(f"{p}:{res.get(p, {}).get('lds', '—')}" for p, _, _ in PAIRS)
        print(f"    math/{mode:12s} {row}")

    sens_align = sensitivity_alignment(wiki, gloss)
    for mode, res in sens_align.items():
        row = " | ".join(f"{p}:{res.get(p, {}).get('lds', '—')}" for p, _, _ in PAIRS)
        print(f"    align/{mode:12s} {row}")

    print("    wiki/threshold (importance 0.0 / 0.5 / 0.85):")
    sens_thresh = sensitivity_threshold_wiki(wiki, gloss)
    for block, res in sens_thresh.items():
        if block == "wiki_noop":
            for mode, val in res.items():
                row = " | ".join(f"{p}:{val.get(p, {}).get('lds', '—')}" for p, _, _ in PAIRS)
                print(f"      {block}/{mode:14s} {row}  (wiki: no importance field -> no-op)")
        else:
            print(f"      {block} (LLM-as-subject P1, concept-level node-only):")
            for mode, val in res.items():
                row = " | ".join(f"{p}:{val.get(p, {}).get('lds', '—')}" for p, _, _ in PAIRS)
                print(f"        {mode:14s} {row}")

    # ── save ──
    result = {
        "generated_at": datetime.now().isoformat(),
        "lds_formula": "LDS = 1 - mean(J_node, J_edge) [frozen v3]",
        "alignment": "gloss->canonical_key (synonym+stem); ZH wiki glossed to EN",
        "wiki_gloss_path": str(gloss_path),
        "wiki_topic_lds": wiki_topic,
        "wiki_pooled_lds": wiki_pooled,
        "math_level_lds": math_level,
        "math_pooled_lds": math_pooled_res,
        "cross_source_textbook_vs_wiki": cs,
        "cross_source_wiki_vs_human": cs_h,
        "sensitivity": sens,
        "sensitivity_alignment": sens_align,
        "sensitivity_threshold_wiki": sens_thresh,
    }
    out_path = OUT_DIR / f"lds_k_deepen_{datetime.now().strftime('%Y%m%d')}.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()
