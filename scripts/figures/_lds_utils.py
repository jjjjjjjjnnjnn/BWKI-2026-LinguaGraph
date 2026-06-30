"""Shared utilities for LDS computation used by all figure scripts."""
import json
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RANDOM_SEED = 42


def lds_jaccard(
    nodes_a: list, nodes_b: list, edges_a: list, edges_b: list
) -> dict:
    """Compute LDS using Jaccard similarity (no GED dependency)."""
    set_a, set_b = set(nodes_a), set(nodes_b)
    node_jac = len(set_a & set_b) / max(len(set_a | set_b), 1)
    set_ea, set_eb = set(edges_a), set(edges_b)
    edge_jac = len(set_ea & set_eb) / max(len(set_ea | set_eb), 1)
    return {
        "lds_score": round(1.0 - (node_jac + edge_jac) / 2, 4),
        "jaccard_node": round(node_jac, 4),
        "jaccard_edge": round(edge_jac, 4),
    }


def lds_pair(
    nodes_a: list, nodes_b: list, edges_a: list, edges_b: list
) -> float:
    """Return LDS as a single float (convenience wrapper)."""
    return lds_jaccard(nodes_a, nodes_b, edges_a, edges_b)["lds_score"]


def load_aligned(path: Path | None = None) -> dict:
    """Load aligned concept data."""
    if path is None:
        path = (
            PROJECT_ROOT
            / "data"
            / "math_extractions"
            / "merged"
            / "aligned_data.json"
        )
    return json.loads(Path(path).read_text(encoding="utf-8"))


def get_lang_graphs(
    aligned: dict,
) -> tuple[dict[str, list[str]], dict[str, set[tuple[str, str]]]]:
    """Return (lang -> [node_labels], lang -> set_of_edges)."""
    groups = aligned.get("aligned_groups", [])
    gid_to_labels: dict[str, dict] = {
        g["id"]: g.get("labels", {}) for g in groups
    }
    lang_nodes: dict[str, list[str]] = {"zh": [], "en": [], "de": []}
    for g in groups:
        labels = g.get("labels", {})
        for lang in ["zh", "en", "de"]:
            if labels.get(lang):
                lang_nodes[lang].append(labels[lang])
    lang_edges: dict[str, set[tuple[str, str]]] = {
        "zh": set(),
        "en": set(),
        "de": set(),
    }
    for r in aligned.get("relations", []):
        sg = r.get("source_group") or r.get("source", "")
        tg = r.get("target_group") or r.get("target", "")
        if sg in gid_to_labels and tg in gid_to_labels:
            for lang in ["zh", "en", "de"]:
                s_label = gid_to_labels[sg].get(lang)
                t_label = gid_to_labels[tg].get(lang)
                if s_label and t_label:
                    lang_edges[lang].add((s_label, t_label))
    return lang_nodes, lang_edges


def degree_preserving_rewire(
    edges: list[tuple], n_swaps: int = 1000
) -> list[tuple]:
    """Double-edge swap: preserves degree sequence."""
    if len(edges) < 2:
        return edges
    edge_list = list(edges)
    random.seed(RANDOM_SEED)
    for _ in range(n_swaps):
        i, j = (
            random.randrange(len(edge_list)),
            random.randrange(len(edge_list)),
        )
        if i == j:
            continue
        a, b = edge_list[i]
        c, d = edge_list[j]
        if len({a, b, c, d}) < 4:
            continue
        if a == d or b == c:
            continue
        if (a, d) in edge_list or (c, b) in edge_list:
            continue
        edge_list[i] = (a, d)
        edge_list[j] = (c, b)
    return edge_list
