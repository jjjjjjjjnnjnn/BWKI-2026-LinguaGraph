#!/usr/bin/env python3
"""
Fig 6 — Curriculum Coverage Score Comparison

Compares textbook coverage across 4 education systems:
  NRW (Germany) / UK / US / CN

Uses corrected methodology (curriculum concepts → textbook concepts).
Data source: config/expert_graphs/coverage_scores.json

Outputs:
  outputs/figures/fig6_coverage.png (300 DPI)
  outputs/figures/fig6_coverage_data.csv

Usage:
    python scripts/figures/fig6_coverage.py
"""

import csv, json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_LABELS = {"NRW": "NRW\n(Germany)", "UK": "UK", "US": "USA", "China": "China"}
SYSTEM_COLORS = {"NRW": "#2563eb", "UK": "#ea580c", "US": "#16a34a", "China": "#9333ea"}


def load_coverage() -> dict:
    path = PROJECT_ROOT / "config" / "expert_graphs" / "coverage_scores.json"
    if not path.exists():
        print("  [FAIL] coverage_scores.json not found")
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    print("Fig 6: Curriculum Coverage Comparison")
    d = load_coverage()
    if not d:
        return

    curricula = d.get("curricula", {})
    print(f"  Loaded {len(curricula)} curriculum systems")

    systems_data: dict[str, list[float]] = {}
    overall_data: dict[str, float] = {}
    for sys_name, stages in sorted(curricula.items()):
        coverages = []
        for stage_name, stage_data in stages.items():
            if isinstance(stage_data, dict) and "coverage" in stage_data:
                coverages.append(stage_data["coverage"])
        if coverages:
            systems_data[sys_name] = coverages
        ov = stages.get("overall", {})
        if "coverage" in ov:
            overall_data[sys_name] = ov["coverage"]
            print(f"    {sys_name:10s}: overall={ov['coverage']*100:.1f}% ({ov['matched']}/{ov['curriculum_concepts']})")

    if not overall_data:
        print("  [FAIL] No overall coverage scores")
        return

    # Figure 1: Overall coverage bar chart
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    ax = axes[0]
    systems = sorted(overall_data.keys(), key=lambda s: -overall_data[s])
    vals = [overall_data[s] for s in systems]
    colors = [SYSTEM_COLORS.get(s, "#6b7280") for s in systems]
    labels = [SYSTEM_LABELS.get(s, s) for s in systems]

    bars = ax.bar(range(len(systems)), vals, 0.5, color=colors, alpha=0.85)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{val*100:.1f}%", ha="center", va="bottom", fontsize=9)

    ax.set_xticks(range(len(systems)))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Curriculum Concepts Covered by Textbook", fontsize=10)
    ax.set_title("Overall Curriculum Coverage", fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))

    # Add annotation
    ax.text(0.98, 0.97,
            "Higher = curriculum\nconcepts found in\ntextbook knowledge graph\n\n"
            "China: centralized curriculum\nNRW: detailed per-track specs\n"
            "US: broad guidelines, low match",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=6.5, color="#555",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f8f9fa", edgecolor="#ddd"))

    # Figure 2: Per-stage coverage for NRW and UK (which have stage data)
    ax = axes[1]
    stage_systems = [s for s in systems if s in systems_data and len(systems_data[s]) >= 3]
    max_stages = max(len(systems_data[s]) for s in stage_systems) if stage_systems else 0

    if max_stages > 0:
        x = np.arange(max_stages)
        width = 0.8 / max(len(stage_systems), 1)

        for i, sys_name in enumerate(stage_systems):
            vals = list(systems_data[sys_name])
            padded = vals + [0] * (max_stages - len(vals))
            offset = (i - (len(stage_systems) - 1) / 2) * width
            color = SYSTEM_COLORS.get(sys_name, "#6b7280")
            label = SYSTEM_LABELS.get(sys_name, sys_name)
            bars = ax.bar(x + offset, padded, width, label=label, color=color, alpha=0.85)
            for bar, val in zip(bars, padded):
                if val > 0.05:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                            f"{val:.0%}", ha="center", va="bottom", fontsize=5.5, rotation=45)

        # Label stages by generic names
        stage_names = [f"S{i+1}" for i in range(max_stages)]

        ax.set_xticks(x)
        ax.set_xticklabels(stage_names, fontsize=7, rotation=20)
        ax.legend(fontsize=8)

    ax.set_title("Per-Stage Coverage (Detailed)", fontsize=10)
    ax.set_ylabel("Coverage", fontsize=10)
    ax.set_ylim(0, 1.0)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))

    plt.tight_layout()
    path = OUTPUT_DIR / "fig6_coverage.png"
    fig.savefig(path, dpi=300)
    print(f"  [OK] {path}")
    plt.close(fig)

    # CSV
    csv_path = OUTPUT_DIR / "fig6_coverage_data.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["system", "overall_coverage", "matched", "total"])
        for sys_name in sorted(overall_data.keys()):
            ov = curricula[sys_name]["overall"]
            w.writerow([sys_name, round(ov["coverage"], 4), ov["matched"], ov["curriculum_concepts"]])
    print(f"  [OK] {csv_path}")

    print(f"\n  Coverage rank:")
    for sys_name in sorted(overall_data.keys(), key=lambda s: -overall_data[s]):
        print(f"    {sys_name:10s}: {overall_data[sys_name]*100:.1f}%")


if __name__ == "__main__":
    main()
