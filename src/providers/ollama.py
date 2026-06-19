"""
Ollama Provider

Calls Ollama via its OpenAI-compatible API endpoint.
Default: http://127.0.0.1:11434/v1
"""

import time
from openai import OpenAI

from src.models import TaskRequest, TaskResponse
from .base import LLMProvider


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider (via OpenAI-compatible endpoint)."""

    def __init__(self, config: dict = None):
        config = config or {}
        self.base_url = config.get("base_url", "http://127.0.0.1:11434/v1")
        self.model = config.get("model", "qwen3:8b")
        self.client = OpenAI(
            base_url=self.base_url,
            api_key="ollama"
        )

    def generate(self, request: TaskRequest) -> TaskResponse:
        start = time.time()

        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        # /no_think disables Qwen3 thinking mode
        messages.append({"role": "user", "content": f"/no_think\n{request.text}"})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            content = response.choices[0].message.content
            # Strip thinking tags (Qwen3 models)
            if "<think>" in content and "</think>" in content:
                content = content.split("</think>")[-1].strip()
            elif content.startswith("<think>"):
                parts = content.split("</think>", 1)
                content = parts[-1].strip() if len(parts) > 1 else ""

            elapsed = (time.time() - start) * 1000

            return TaskResponse(
                task=request.task,
                raw_text=content,
                tokens_in=response.usage.prompt_tokens if response.usage else 0,
                tokens_out=response.usage.completion_tokens if response.usage else 0,
                latency_ms=elapsed,
            )

        except Exception as e:
            elapsed = (time.time() - start) * 1000
            return TaskResponse(
                task=request.task,
                error=str(e),
                latency_ms=elapsed,
            )

    def is_available(self) -> bool:
        try:
            self.client.models.list()
            return True
        except Exception:
            return False

    def __repr__(self):
        return f"OllamaProvider(model={self.model}, url={self.base_url})"
