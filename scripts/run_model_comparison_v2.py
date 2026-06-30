#!/usr/bin/env python3
"""
run_model_comparison_v2.py — Real LLM model comparison on gold dataset
======================================================================
Calls actual APIs for 4 models: qwen-plus, qwen-max (Bailian), gpt-4o, gpt-4o-mini (OpenRouter)

Usage:
    python scripts/run_model_comparison_v2.py
    python scripts/run_model_comparison_v2.py --models qwen-plus,gpt-4o
"""

import json, os, re, time
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GOLD_PATH = PROJECT_ROOT / "data" / "gold" / "gold_dataset.json"
OUTPUT_DIR = PROJECT_ROOT / "data" / "model_comparison"

# Lazy-loaded extract prompt (avoid module-level file I/O)
_EXTRACT_PROMPT: str | None = None

def _get_extract_prompt() -> str:
    global _EXTRACT_PROMPT
    if _EXTRACT_PROMPT is None:
        _EXTRACT_PROMPT = (PROJECT_ROOT / "config" / "prompts" / "extract.md").read_text(encoding="utf-8")
    return _EXTRACT_PROMPT

# ── API Configuration ──
BAILIAN_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
BAILIAN_KEY = os.environ.get("BAILIAN_API_KEY", "")
# OpenAI-compatible proxy for GPT models
OPENAI_COMPAT_URL = os.environ.get("OPENAI_COMPAT_URL", "https://free.v36.cm/v1")
OPENAI_COMPAT_KEY = os.environ.get("OPENAI_COMPAT_KEY", "")

# ── Model Configs ──
MODELS = {
    "qwen-plus": {
        "api_url": BAILIAN_URL,
        "api_key": BAILIAN_KEY,
        "model_id": "qwen-plus",
        "provider": "bailian",
    },
    "qwen-max": {
        "api_url": BAILIAN_URL,
        "api_key": BAILIAN_KEY,
        "model_id": "qwen-max",
        "provider": "bailian",
    },
    "gpt-4o": {
        "api_url": OPENAI_COMPAT_URL,
        "api_key": OPENAI_COMPAT_KEY,
        "model_id": "gpt-4o",
        "provider": "openai-compat",
    },
    "gpt-4o-mini": {
        "api_url": OPENAI_COMPAT_URL,
        "api_key": OPENAI_COMPAT_KEY,
        "model_id": "gpt-4o-mini",
        "provider": "openai-compat",
    },
}

# ── Encoding fix: emphasize native language output ──
ENCODING_INSTRUCTION = {
    "zh": "\n\nCRITICAL: 输出原始中文概念, 禁止使用 ASCII 编码替代中文字符。直接输出如 '导数' '变化率' 而非拼音或英文翻译。",
    "de": "\n\nCRITICAL: Gib die Konzepte auf Deutsch aus. Verwende Umlaute (ä, ö, ü, ß) korrekt. Keine ASCII-Ersetzungen.",
    "en": "\n\nCRITICAL: Output concepts in English. Use the original English terms directly.",
}


def load_gold():
    with open(GOLD_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def call_llm(text, lang, model_config, max_retries=2):
    """Call LLM API for concept extraction."""
    from openai import OpenAI

    client = OpenAI(
        base_url=model_config["api_url"],
        api_key=model_config["api_key"],
        max_retries=max_retries,
        timeout=60,
    )

    encoding_fix = ENCODING_INSTRUCTION.get(lang, "")
    user_msg = f"Language: {lang}\nText: {text}\n\nExtract concepts as JSON.{encoding_fix}"

    for attempt in range(max_retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model_config["model_id"],
                messages=[
                    {"role": "system", "content": _get_extract_prompt()},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.3,
                max_tokens=512,
            )
            raw = resp.choices[0].message.content.strip()
            # Remove <think>...</think> blocks if present (some models add these)
            cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
            # Extract JSON from response
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if match:
                parsed = json.loads(match.group())
                return parsed.get("concepts", [])
            else:
                # Try to extract concepts from plain text
                lines = [l.strip().strip("-•*").strip() for l in cleaned.split("\n") if l.strip()]
                return [l for l in lines if len(l) > 1][:20]
        except Exception as e:
            if attempt < max_retries:
                print(f"    Retry {attempt+1}: {e}")
                time.sleep(2 ** attempt)
            else:
                print(f"    FAILED after {max_retries+1} attempts: {e}")
                return []


def compute_metrics(gold_set, pred_set):
    """Compute precision, recall, F1."""
    if not gold_set or not pred_set:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    tp = len(gold_set & pred_set)
    p = tp / len(pred_set)
    r = tp / len(gold_set)
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    return {"precision": round(p, 4), "recall": round(r, 4), "f1": round(f1, 4)}


def check_encoding(predicted, lang):
    """Check for encoding issues (mojibake / ASCII replacement)."""
    mojibake_patterns = ["姒傚康", "鏂归潰", "鍏崇郴", "鍥犵堃", "闅跺睘", "瀵圭珛",
                         "鐩稿叧", "鏍稿績", "姒傚", "鍙樺", "鏋", "涓"]
    for p in mojibake_patterns:
        for concept in predicted:
            if p in concept:
                return False
    return True


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=str, default=None,
                        help="Comma-separated model names to run (default: all)")
    args = parser.parse_args()

    target_models = args.models.split(",") if args.models else list(MODELS.keys())

    # Check API keys
    missing = []
    for m in target_models:
        cfg = MODELS.get(m)
        if not cfg:
            print(f"Unknown model: {m}")
            continue
        if not cfg["api_key"]:
            missing.append(m)
    if missing:
        print(f"Missing API keys for: {', '.join(missing)}")
        print("Set BAILIAN_API_KEY and/or OPENROUTER_API_KEY environment variables")
        if not any(MODELS[m]["api_key"] for m in target_models if m in MODELS):
            return

    gold_items = load_gold()
    print(f"Gold items: {len(gold_items)}")
    print(f"Models to run: {target_models}")

    for model_name in target_models:
        cfg = MODELS.get(model_name)
        if not cfg or not cfg["api_key"]:
            print(f"\n=== {model_name} — SKIPPED (no API key) ===")
            continue

        print(f"\n=== {model_name} ({cfg['provider']}) ===")
        results = []
        encoding_errors = 0

        for i, item in enumerate(gold_items):
            text = item.get("text", "")
            lang = item.get("language", "zh")
            gold_concepts = item.get("human_labels", {}).get("concepts", [])
            gold_set = set(c.strip().lower() for c in gold_concepts if c.strip())

            # Call real LLM
            pred_concepts = call_llm(text, lang, cfg)
            pred_set = set(c.strip().lower() for c in pred_concepts if c.strip())

            # Check encoding
            if not check_encoding(pred_concepts, lang):
                encoding_errors += 1
                print(f"  WARNING: Encoding issue in {item.get('sample_id', '')} ({lang})")

            metrics = compute_metrics(gold_set, pred_set)
            results.append({
                "sample_id": item.get("sample_id", ""),
                "language": lang,
                "gold_concepts": gold_concepts,
                "predicted_concepts": pred_concepts,
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1": metrics["f1"],
            })

            # Progress
            if (i + 1) % 5 == 0 or i == len(gold_items) - 1:
                print(f"  [{i+1}/{len(gold_items)}] {item.get('sample_id', '')} F1={metrics['f1']:.4f}")

            # Rate limiting
            time.sleep(0.5)

        # Compute summary
        avg_f1 = sum(r["f1"] for r in results) / len(results) if results else 0
        avg_p = sum(r["precision"] for r in results) / len(results) if results else 0
        avg_r = sum(r["recall"] for r in results) / len(results) if results else 0

        output = {
            "model": model_name,
            "run_at": datetime.now().isoformat(),
            "total_items": len(results),
            "encoding_errors": encoding_errors,
            "summary": {
                "mean_f1": round(avg_f1, 4),
                "mean_precision": round(avg_p, 4),
                "mean_recall": round(avg_r, 4),
            },
            "results": results,
        }

        out_path = OUTPUT_DIR / f"{model_name}_results.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"  F1={avg_f1:.4f} P={avg_p:.4f} R={avg_r:.4f} (n={len(results)})")
        print(f"  Encoding errors: {encoding_errors}")
        print(f"  Saved: {out_path}")

    # Print comparison table
    print(f"\n{'='*60}")
    print("Model Comparison Summary")
    print(f"{'='*60}")
    print(f"  {'Model':<20s} {'F1':>8s} {'P':>8s} {'R':>8s} {'EncErr':>8s}")
    print(f"  {'-'*20} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for model_name in target_models:
        out_path = OUTPUT_DIR / f"{model_name}_results.json"
        if out_path.exists():
            d = json.load(open(out_path, encoding="utf-8"))
            s = d["summary"]
            print(f"  {model_name:<20s} {s['mean_f1']:>8.4f} {s['mean_precision']:>8.4f} {s['mean_recall']:>8.4f} {d.get('encoding_errors', 0):>8d}")


if __name__ == "__main__":
    main()
