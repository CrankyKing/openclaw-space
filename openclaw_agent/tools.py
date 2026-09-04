"""工具注册与内置工具：定义 Agent 可调用的工具及其注册机制。"""
import ast
import datetime
import json
import operator as op
from typing import Any, Callable, Dict


class Tool:
    """一个可被 Agent 调用的工具。"""

    def __init__(self, name: str, description: str, parameters: Dict[str, Any], func: Callable):
        self.name = name
        self.description = description
        self.parameters = parameters  # JSON Schema 形式
        self.func = func

    def run(self, **kwargs) -> str:
        """执行工具，任何异常都转为可观察的文本，便于模型继续决策。"""
        try:
            result = self.func(**kwargs)
        except Exception as e:  # noqa: BLE001 —— 工具内部错误也返回给模型观察
            return f"工具执行出错: {e}"
        return json.dumps(result, ensure_ascii=False) if not isinstance(result, str) else result

    def to_schema(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


class ToolRegistry:
    """工具注册表：负责注册与按名执行工具。"""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def run(self, name: str, **kwargs) -> str:
        tool = self._tools.get(name)
        if tool is None:
            return f"未知工具: {name}"
        return tool.run(**kwargs)

    @property
    def tools(self) -> Dict[str, Tool]:
        return self._tools

    def describe(self) -> str:
        return "\n".join(f"- {t.name}: {t.description}" for t in self._tools.values())

    @classmethod
    def default(cls) -> "ToolRegistry":
        registry = cls()
        registry.register(
            Tool(
                name="get_current_time",
                description="获取当前日期和时间",
                parameters={"type": "object", "properties": {}},
                func=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %A"),
            )
        )
        registry.register(
            Tool(
                name="calculator",
                description="执行数学表达式计算，支持 + - * / 和括号",
                parameters={
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string", "description": "数学表达式，例如 (1+2)*3.5"}
                    },
                    "required": ["expression"],
                },
                func=safe_calculate,
            )
        )
        return registry


def safe_calculate(expression: str) -> str:
    """安全的表达式计算器：仅允许数字与基本四则运算，防止任意代码执行。"""
    allowed_ops = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Mod: op.mod,
        ast.Pow: op.pow,
        ast.USub: op.neg,
        ast.UAdd: op.pos,
    }

    def _eval(node: ast.AST):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("仅支持数值运算")
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_ops:
            return allowed_ops[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_ops:
            return allowed_ops[type(node.op)](_eval(node.operand))
        raise ValueError(f"不支持的表达式: {type(node).__name__}")

    try:
        tree = ast.parse(expression, mode="eval")
        return str(_eval(tree))
    except Exception as e:  # noqa: BLE001
        return f"计算失败: {e}"
