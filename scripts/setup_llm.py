"""
LinguaGraph — Model & Runtime Setup

Downloads the lightweight GGUF model and llama-cli binary for
zero-config local inference.

Usage:
    python scripts/setup_llm.py            # Interactive (check + download)
    python scripts/setup_llm.py --force     # Force re-download

This script makes the project fully self-contained — no API keys,
no OpenAI, no Ollama, no LM Studio.
"""

import os
import platform
import sys
import zipfile
from pathlib import Path

# --- Project paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
LLAMA_DIR = PROJECT_ROOT / "llama"

# --- Model configuration ---
# Qwen2.5-0.5B Q4_K_M — 463 MB, runs on phone
# Non-instruct version (matches existing project-local model file)
MODEL_URL = (
    "https://huggingface.co/Qwen/Qwen2.5-0.5B-GGUF/resolve/main/"
    "qwen2.5-0.5b-q4_k_m.gguf"
)
MODEL_FILENAME = "qwen2.5-0.5b-q4_k_m.gguf"
MODEL_EXPECTED_MB = 463

# llama.cpp pre-built binary (lightweight, no GPU needed)
LLAMA_VERSION = "b4663"
SYSTEM = platform.system().lower()

if SYSTEM == "windows":
    LLAMA_URL = (
        f"https://github.com/ggml-org/llama.cpp/releases/download/b{LLAMA_VERSION}/"
        f"llama-b{LLAMA_VERSION}-bin-win-cuda-cu12.4.0-x64.zip"
    )
    LLAMA_CLI_NAME = "llama-cli.exe"
elif SYSTEM == "linux":
    LLAMA_URL = (
        f"https://github.com/ggml-org/llama.cpp/releases/download/b{LLAMA_VERSION}/"
        f"llama-b{LLAMA_VERSION}-bin-ubuntu-x64.zip"
    )
    LLAMA_CLI_NAME = "llama-cli"
elif SYSTEM == "darwin":
    LLAMA_URL = (
        f"https://github.com/ggml-org/llama.cpp/releases/download/b{LLAMA_VERSION}/"
        f"llama-b{LLAMA_VERSION}-bin-macos-x64.zip"
    )
    LLAMA_CLI_NAME = "llama-cli"
else:
    LLAMA_URL = None
    LLAMA_CLI_NAME = "llama-cli"


def log(msg: str, ok: bool = True) -> None:
    icon = "✅" if ok else "❌"
    print(f"  {icon} {msg}")


def check_model() -> bool:
    """Check if the GGUF model file exists and has expected size."""
    model_path = MODELS_DIR / MODEL_FILENAME
    if not model_path.exists():
        log(f"Model not found: {MODEL_FILENAME}", ok=False)
        return False
    size_mb = model_path.stat().st_size / (1024 * 1024)
    if size_mb < MODEL_EXPECTED_MB * 0.8:
        log(f"Model too small: {size_mb:.0f} MB (expected ~{MODEL_EXPECTED_MB} MB)", ok=False)
        return False
    log(f"Model found: {MODEL_FILENAME} ({size_mb:.0f} MB)")
    return True


def check_llama_cli() -> bool:
    """Check if llama-cli binary exists and is executable."""
    cli_path = LLAMA_DIR / LLAMA_CLI_NAME
    if not cli_path.exists():
        log(f"llama-cli not found: {LLAMA_CLI_NAME}", ok=False)
        return False
    log(f"llama-cli found: {LLAMA_CLI_NAME}")
    return True


def download_model(force: bool = False) -> bool:
    """Download the GGUF model from Hugging Face."""
    model_path = MODELS_DIR / MODEL_FILENAME
    if model_path.exists() and not force:
        log("Model already exists (use --force to re-download)")
        return True

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n  Downloading {MODEL_FILENAME} (~{MODEL_EXPECTED_MB} MB)...")
    print(f"  From: {MODEL_URL}")
    print("  This may take a few minutes on slow connections.\n")

    try:
        import urllib.request

        def progress(count, block_size, total_size):
            percent = min(count * block_size * 100 // max(total_size, 1), 100)
            bar = "█" * (percent // 5) + "░" * (20 - percent // 5)
            sys.stdout.write(f"\r  [{bar}] {percent}%")
            sys.stdout.flush()

        urllib.request.urlretrieve(MODEL_URL, model_path, progress)
        print()
        size_mb = model_path.stat().st_size / (1024 * 1024)
        log(f"Download complete: {size_mb:.0f} MB")
        return True
    except Exception as e:
        log(f"Download failed: {e}", ok=False)
        if model_path.exists():
            model_path.unlink()
        return False


def download_llama_cli(force: bool = False) -> bool:
    """Download and extract llama-cli binary."""
    cli_path = LLAMA_DIR / LLAMA_CLI_NAME
    if cli_path.exists() and not force:
        log("llama-cli already exists (use --force to re-download)")
        return True

    if not LLAMA_URL:
        log(f"Auto-download not available for {SYSTEM}.", ok=False)
        log("Install llama.cpp manually: https://github.com/ggml-org/llama.cpp", ok=True)
        return False

    LLAMA_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = LLAMA_DIR / "llama.zip"

    print(f"\n  Downloading llama.cpp ({SYSTEM})...")
    try:
        import urllib.request
        urllib.request.urlretrieve(LLAMA_URL, zip_path)
    except Exception as e:
        log(f"Download failed: {e}", ok=False)
        return False

    # Extract llama-cli from zip
    try:
        with zipfile.ZipFile(zip_path) as zf:
            for name in zf.namelist():
                if name.endswith(LLAMA_CLI_NAME) or name.endswith(f"/{LLAMA_CLI_NAME}"):
                    target = LLAMA_DIR / LLAMA_CLI_NAME
                    with zf.open(name) as src, open(target, "wb") as dst:
                        dst.write(src.read())
                    target.chmod(0o755)
                    break

        zip_path.unlink()
        log(f"llama-cli extracted to: {LLAMA_DIR}")
        return True
    except Exception as e:
        log(f"Extraction failed: {e}", ok=False)
        return False


def self_check() -> dict:
    """Run a full system check and return status."""
    print("\n" + "=" * 50)
    print(" LinguaGraph — Self-Check")
    print("=" * 50)

    results = {}

    # Python version
    py_ok = sys.version_info >= (3, 10)
    print(f"\n  Python: {sys.version}")
    log(f"Python 3.10+ (got {sys.version_info.major}.{sys.version_info.minor})", ok=py_ok)
    results["python"] = py_ok

    # Dependencies
    deps_ok = True
    print("\n  Dependencies:")
    for dep in ["networkx", "yaml", "json", "pathlib"]:
        try:
            __import__(dep.replace("-", "_"))
            log(f"{dep}")
        except ImportError:
            log(f"{dep} — NOT INSTALLED", ok=False)
            deps_ok = False
    results["dependencies"] = deps_ok

    # Model
    model_ok = check_model()
    results["model"] = model_ok

    # llama-cli
    cli_ok = check_llama_cli()
    results["llama_cli"] = cli_ok

    # Config
    config_ok = (PROJECT_ROOT / "config" / "config.yaml").exists()
    print()
    log("config/config.yaml", ok=config_ok)
    results["config"] = config_ok

    # Summary
    print("\n" + "-" * 50)
    all_ok = all(results.values())
    if all_ok:
        print(" ✅ ALL CHECKS PASSED — LinguaGraph is ready to use!")
    else:
        print(" ⚠️  Some checks failed. Run with --download to fix.")
        for k, v in results.items():
            if not v:
                print(f"    - {k}: FAILED")
    print("=" * 50 + "\n")

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph LLM Setup")
    parser.add_argument("--check", action="store_true", help="Run self-check only")
    parser.add_argument("--download", action="store_true", help="Download model + llama-cli")
    parser.add_argument("--force", action="store_true", help="Force re-download")
    parser.add_argument("--model-only", action="store_true", help="Download model only")
    parser.add_argument("--llama-only", action="store_true", help="Download llama-cli only")
    args = parser.parse_args()

    if args.check or not (args.download or args.force or args.model_only or args.llama_only):
        results = self_check()
        if not all(results.values()) and not args.check:
            print("\n  💡 Run with --download to download missing files:")
            print("     python scripts/setup_llm.py --download")
        return

    # Download mode
    if not args.llama_only:
        download_model(force=args.force)
    if not args.model_only:
        download_llama_cli(force=args.force)

    # Final check
    self_check()


if __name__ == "__main__":
    main()
