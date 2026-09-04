"""简单的滑动窗口对话记忆。"""
from collections import deque
from typing import Deque, List


class Memory:
    """保留最近 N 条消息的对话记忆，避免上下文无限增长。"""

    def __init__(self, max_messages: int = 20):
        self._messages: Deque[dict] = deque(maxlen=max_messages)

    def add_system(self, content: str) -> None:
        self._messages.appendleft({"role": "system", "content": content})

    def add_user(self, content: str) -> None:
        self._messages.append({"role": "user", "content": content})

    def add_assistant(self, content: str) -> None:
        self._messages.append({"role": "assistant", "content": content})

    def as_list(self) -> List[dict]:
        return list(self._messages)

    def clear(self) -> None:
        self._messages.clear()
