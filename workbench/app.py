"""
LinguaGraph Research Workbench — Flask Application

A minimal research workbench serving the CognitiveSpace knowledge graph.
All data is pre-computed from the existing pipeline. No new research code.

Usage:
    python workbench/app.py
    Open http://localhost:5000
"""

import json, os, math, flask
from pathlib import Path
from flask import Flask, render_template, request, jsonify

PROJECT_DIR = Path(__file__).resolve().parent.parent

app = Flask(__name__)

# Serve CognitiveSpace static files
COGNITIVE_SPACE_DIR = PROJECT_DIR / "cognitive-space" / "web"
if COGNITIVE_SPACE_DIR.exists():
    @app.route("/cognitive-space/web/<path:filename>")
    def serve_cognitivespace(filename):
        return flask.send_from_directory(str(COGNITIVE_SPACE_DIR), filename)

# ── Load pre-computed data ─────────────────────────────────────────────

# Load the CognitiveSpace graph data
data_path = PROJECT_DIR / "cognitive-space" / "web" / "data.js"
GRAPH_DATA = None
if data_path.exists():
    raw = data_path.read_text("utf-8")
    json_str = raw.split("const COGNITIVE_DATA = ")[1].rsplit(";", 1)[0]
    GRAPH_DATA = json.loads(json_str)

# ── Compute statistics from graph data ─────────────────────────────────
def compute_stats(data):
    if not data:
        return {}
    nodes = data["nodes"]
    links = data["links"]

    # Level distribution
    levels = {}
    for n in nodes:
        lv = n.get("level", "unknown")
        levels[lv] = levels.get(lv, 0) + 1

    # Language coverage
    lang_coverage = {"zh": 0, "en": 0, "de": 0}
    trilingual = 0
    for n in nodes:
        labels = n.get("labels", {})
        if labels.get("zh"): lang_coverage["zh"] += 1
        if labels.get("en"): lang_coverage["en"] += 1
        if labels.get("de"): lang_coverage["de"] += 1
        if labels.get("zh") and labels.get("en") and labels.get("de"):
            trilingual += 1

    # Groups (domains)
    groups = {}
    for n in nodes:
        g = n.get("group", "general")
        groups[g] = groups.get(g, 0) + 1

    return {
        "total_nodes": len(nodes),
        "total_links": len(links),
        "known_links": sum(1 for l in links if not l.get("inferred", False)),
        "inferred_links": sum(1 for l in links if l.get("inferred", False)),
        "levels": levels,
        "level_names": {"elementary": "小学", "middle": "初中", "high": "高中", "college": "大学"},
        "lang_coverage": lang_coverage,
        "trilingual": trilingual,
        "groups": groups,
    }

STATS = compute_stats(GRAPH_DATA)

# ── Routes ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Landing page: overview + upload prompt."""
    return render_template("index.html", stats=STATS)


@app.route("/results")
def results():
    """Graph statistics + LDS comparison."""
    return render_template("results.html", stats=STATS)


@app.route("/cognitivespace")
def cognitivespace():
    """Embedded CognitiveSpace 3D visualization."""
    return render_template("cognitivespace.html")


@app.route("/report")
def report():
    """Auto-generated analysis report."""
    return render_template("report.html", stats=STATS)


@app.route("/api/stats")
def api_stats():
    """JSON endpoint for dynamic data loading."""
    return jsonify(STATS)


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║  LinguaGraph Research Workbench              ║")
    print("║  http://localhost:5000                       ║")
    print("╚══════════════════════════════════════════════╝")
    app.run(debug=True, port=5000)
