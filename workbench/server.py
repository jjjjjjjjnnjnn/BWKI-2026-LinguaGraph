"""
LinguaGraph Workbench — Web Server

Provides a web interface for the text → analysis → 3D visualization pipeline.

Usage:
    python workbench/server.py
    Open http://localhost:5000
"""

import sys, os, json
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

# Ensure project root is on path
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from workbench.process import process_text

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = PROJECT_DIR / "workbench" / "output"

# Ensure output directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/")
def index():
    """Input form."""
    return render_template("input.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """Process text and show results."""
    text = request.form.get("text", "").strip()
    language = request.form.get("language", "zh")

    if not text:
        return redirect(url_for("index"))

    # Create a unique job ID
    import time
    job_id = f"job_{int(time.time())}"
    output_dir = app.config["UPLOAD_FOLDER"] / job_id

    try:
        # Run the pipeline
        result = process_text(text, language, output_dir)

        # Build relative path to visualization
        viz_url = f"/viz/{job_id}/index.html"

        return render_template("result.html",
            stats=result["stats"],
            viz_url=viz_url,
            text_preview=text[:200] + ("..." if len(text) > 200 else ""),
            job_id=job_id
        )
    except Exception as e:
        return f"Processing error: {e}", 500


@app.route("/viz/<job_id>/<path:filename>")
def serve_viz(job_id, filename):
    """Serve generated visualization files."""
    viz_dir = app.config["UPLOAD_FOLDER"] / job_id
    return send_from_directory(str(viz_dir), filename)


@app.route("/demo")
def demo():
    """Load the pre-computed CognitiveSpace with 574 concepts."""
    return redirect("/cognitive-space/web/index.html")


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║  LinguaGraph Processing Workbench            ║")
    print("║  Open: http://localhost:5000                 ║")
    print("║                                                ║")
    print("║  /        — Text input                        ║")
    print("║  /analyze — Process text (POST)               ║")
    print("║  /viz/   — Generated visualizations           ║")
    print("╚══════════════════════════════════════════════╝")
    app.run(debug=False, port=5000)
