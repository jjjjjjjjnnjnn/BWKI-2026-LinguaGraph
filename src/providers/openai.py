"""
OpenAI Provider — calls OpenAI API (or any OpenAI-compatible endpoint).

Supports:
- OpenAI API (GPT-4.1-mini, etc.)
- Any OpenAI-compatible local server (via base_url)
"""

import os
import time
from openai import OpenAI

from src.models import TaskRequest, TaskResponse
from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI / OpenAI-compatible provider."""

    def __init__(self, config: dict = None):
        config = config or {}
        self.model = config.get("model", "gpt-4.1-mini")
        self.api_key = config.get("api_key") or os.environ.get("OPENAI_API_KEY")
        self.base_url = config.get("base_url")

        client_kwargs = {"api_key": self.api_key or "no-key"}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url

        self.client = OpenAI(**client_kwargs)

    def generate(self, request: TaskRequest) -> TaskResponse:
        start = time.time()

        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.text})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            choice = response.choices[0]
            content = choice.message.content or ""
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
        return f"OpenAIProvider(model={self.model})"
