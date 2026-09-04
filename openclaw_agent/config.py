"""配置加载：从环境变量读取 OpenAI 兼容 API 配置。"""
import os
from dataclasses import dataclass


@dataclass
class Config:
    api_base: str
    api_key: str
    model: str
    max_iterations: int = 10
    temperature: float = 0.7

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            api_base=os.getenv("OPENCLAW_API_BASE", "https://api.openai.com/v1").rstrip("/"),
            api_key=os.getenv("OPENCLAW_API_KEY", ""),
            model=os.getenv("OPENCLAW_MODEL", "gpt-4o-mini"),
            max_iterations=int(os.getenv("OPENCLAW_MAX_ITERATIONS", "10")),
            temperature=float(os.getenv("OPENCLAW_TEMPERATURE", "0.7")),
        )
