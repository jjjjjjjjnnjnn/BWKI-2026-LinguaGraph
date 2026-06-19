"""
Local GGUF Provider — runs GGUF models via llama.cpp subprocess.

No HTTP server, no Ollama, no intermediate layer.
Direct C++ inference via llama-cli binary.

Self-contained: discovers model and llama-cli relative to project root.
No external dependencies, no PATH configuration needed.
"""

import os
import subprocess
import tempfile
import time
from pathlib import Path

from src.models import TaskRequest, TaskResponse
from .base import LLMProvider


# Project-local paths (auto-discovered, no external dependencies)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # src/../.. = project root
_FALLBACK_PATHS = [
    # 1. Project-local model (self-contained)
    _PROJECT_ROOT / "models" / "qwen2.5-0.5b-q4_k_m.gguf",
    # 2. Project-local llama-cli
    _PROJECT_ROOT / "llama" / "llama-cli.exe",
    # 3. Platform-generic: model in current dir / models/
    _PROJECT_ROOT / "models" / "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
    _PROJECT_ROOT / "models" / "model.gguf",
]


def _find_first_existing(*paths: Path) -> Path | None:
    """Return the first existing file path."""
    for p in paths:
        if p.exists():
            return p.resolve()
    return None


class LocalProvider(LLMProvider):
    """Local GGUF model via llama.cpp CLI subprocess.

    Auto-discovers model and binary from:
    1. Project-local models/ and llama/ directories
    2. Shared MML Runtime directory
    3. Game project's ai-runtime directory

    No configuration needed for standard setup.
    """

    def __init__(self, config: dict = None):
        config = config or {}

        # Resolve model path
        self.model_path = config.get("model_path", "")
        if not self.model_path or not Path(self.model_path).exists():
            found = _find_first_existing(
                _FALLBACK_PATHS[0], _FALLBACK_PATHS[2], _FALLBACK_PATHS[3]
            )
            self.model_path = str(found) if found else ""

        # Resolve llama-cli path
        self.llama_cli = config.get("llama_cli_path", "")
        if not self.llama_cli or not Path(self.llama_cli).exists():
            found = _find_first_existing(
                _FALLBACK_PATHS[1]
            )
            self.llama_cli = str(found) if found else ""

        self.n_threads = config.get("n_threads", 4)
        self.n_ctx = config.get("n_ctx", 2048)

    def generate(self, request: TaskRequest) -> TaskResponse:
        start = time.time()

        # Write prompt to temp file (llama-cli -p enters interactive mode; -f avoids it)
        prompt = self._build_prompt(request)
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(prompt)
            prompt_file = f.name

        cmd = [
            self.llama_cli,
            "-m", self.model_path,
            "-f", prompt_file,
            "-n", str(request.max_tokens),
            "--temp", str(request.temperature),
            "--threads", str(self.n_threads),
            "--ctx-size", str(self.n_ctx),
            "--no-display-prompt",
        ]

        try:
            cli_dir = str(Path(self.llama_cli).parent)

            result = subprocess.run(
                cmd, capture_output=True, timeout=120, cwd=cli_dir,
                stdin=subprocess.DEVNULL,  # Prevent interactive mode hang
            )
            elapsed = (time.time() - start) * 1000

            # Decode output with error tolerance (llama-cli banner may contain non-UTF-8 bytes)
            stdout = result.stdout.decode("utf-8", errors="replace")
            stderr = result.stderr.decode("utf-8", errors="replace")

            # Cleanup temp file
            try: os.unlink(prompt_file)
            except: pass

            if result.returncode != 0:
                return TaskResponse(
                    task=request.task,
                    error=f"llama-cli exit {result.returncode}: {stderr[:200]}",
                    latency_ms=elapsed,
                )

            output = self._parse_output(stdout)
            return TaskResponse(
                task=request.task,
                raw_text=output,
                latency_ms=elapsed,
                metadata={"speed": self._extract_speed(stderr)},
            )

        except subprocess.TimeoutExpired:
            elapsed = (time.time() - start) * 1000
            try: os.unlink(prompt_file)
            except: pass
            return TaskResponse(
                task=request.task, error="模型推理超时 (>30s)", latency_ms=elapsed,
            )
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            try: os.unlink(prompt_file)
            except: pass
            return TaskResponse(
                task=request.task, error=str(e), latency_ms=elapsed,
            )

    def _build_prompt(self, request: TaskRequest) -> str:
        """Qwen2.5 ChatML format."""
        system = request.system_prompt or "You are a helpful assistant."
        return f"<|system|>\n{system}\n<|user|>\n{request.text}\n<|assistant|>\n"

    def _parse_output(self, raw: str) -> str:
        """Extract response from llama-cli output."""
        lines = raw.split("\n")
        result = []
        in_response = False
        for line in lines:
            if "<|assistant|>" in line:
                in_response = True
                continue
            if not in_response:
                continue
            if "t/s" in line or line.strip().startswith("["):
                continue
            result.append(line)
        return "\n".join(result).strip()

    def _extract_speed(self, stderr: str) -> str:
        for line in stderr.split("\n"):
            if "t/s" in line or "tokens/s" in line:
                return line.strip()
        return ""

    def is_available(self) -> bool:
        return bool(self.model_path) and Path(self.model_path).exists()

    def __repr__(self):
        name = Path(self.model_path).name if self.model_path else "(no model)"
        return f"LocalProvider({name})"
