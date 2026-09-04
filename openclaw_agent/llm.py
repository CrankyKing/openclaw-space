"""OpenAI 兼容的 LLM 客户端。"""
from typing import List, Optional

import requests

from .config import Config


class LLMError(Exception):
    pass


class LLMClient:
    """封装 chat completions 接口的轻量客户端，兼容 OpenAI / DeepSeek / Ollama 等。"""

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()

    def chat(self, messages: List[dict], temperature: Optional[float] = None) -> str:
        """调用 chat completions 接口，返回助手文本回复。"""
        url = f"{self.config.api_base}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
        }
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.config.temperature,
        }
        try:
            resp = self.session.post(url, headers=headers, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            raise LLMError(f"调用模型失败: {e}") from e

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            raise LLMError(f"模型返回格式异常: {data}") from e
