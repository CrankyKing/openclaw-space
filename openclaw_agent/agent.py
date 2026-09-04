"""Agent 核心：基于 ReAct（思考-行动-观察）范式的执行循环。"""
import json
import re
from typing import Dict, Optional

from .config import Config
from .llm import LLMClient
from .memory import Memory
from .tools import ToolRegistry

SYSTEM_PROMPT = """你是一个名为 OpenClaw 的 AI 智能体。
你可以通过调用工具来完成任务。请严格遵循以下格式，每次只输出一个 JSON 对象（不要输出任何其他内容）：

1. 需要调用工具时：
{"action": "tool", "tool": "<工具名>", "arguments": {<参数键值对>}}

2. 已经得到答案、无需再调用工具时：
{"action": "final", "answer": "<最终回答>"}

规则：
- 每一步只能输出一个 JSON 对象。
- 如果工具调用失败或信息不足，可以继续调用其他工具。
- 得到足够信息后，必须用 final 给出最终回答。
"""


class Agent:
    """一个轻量级 ReAct Agent。"""

    def __init__(self, config: Config, registry: Optional[ToolRegistry] = None):
        self.config = config
        self.llm = LLMClient(config)
        self.registry = registry or ToolRegistry.default()
        self.memory = Memory()
        self.memory.add_system(SYSTEM_PROMPT + "\n\n可用工具：\n" + self.registry.describe())

    def run(self, user_input: str) -> str:
        """处理一条用户输入，返回最终回答。"""
        self.memory.add_user(user_input)
        for step in range(1, self.config.max_iterations + 1):
            response = self.llm.chat(self.memory.as_list())
            parsed = self._parse_action(response)

            # 无法解析或模型直接给出最终回答
            if parsed is None or parsed.get("action") == "final":
                answer = parsed.get("answer", response) if parsed else response
                self.memory.add_assistant(answer)
                return answer

            # 调用工具并反馈观察结果
            tool_name = parsed.get("tool", "")
            arguments = parsed.get("arguments", {}) or {}
            observation = self.registry.run(tool_name, **arguments)
            print(f"  [step {step}] 调用工具 {tool_name} -> {observation}")
            self.memory.add_assistant(response)
            self.memory.add_user(f"工具 {tool_name} 的执行结果：{observation}")

        return "已达到最大迭代次数，未能完成任务。"

    @staticmethod
    def _parse_action(text: str) -> Optional[Dict]:
        """从模型输出中解析 JSON 动作：优先取 ```json 代码块，否则取第一个 { ... }。"""
        code_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if code_block:
            raw_text = code_block.group(1)
        else:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            raw_text = match.group(0) if match else None
        if not raw_text:
            return None
        try:
            obj = json.loads(raw_text)
        except json.JSONDecodeError:
            return None
        return obj if isinstance(obj, dict) else None
