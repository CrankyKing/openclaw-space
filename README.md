# OpenClaw Space

基于 Python 实现的轻量级 AI Agent 框架与个人智能体工作空间。

## 项目简介

本项目用 Python 实现了一个简洁、可扩展的 AI Agent 核心：通过 OpenAI 兼容接口接入任意大语言模型，采用 **ReAct（思考 → 行动 → 观察）** 范式循环执行，支持工具注册、对话记忆与命令行交互，可作为学习 Agent 原理或构建个人智能体的起点。

## 功能特性

- 轻量 ReAct Agent：思考 → 调用工具 → 观察结果 → 得出结论
- 模型无关：兼容 OpenAI / DeepSeek / 通义 / 本地 Ollama 等 OpenAI 兼容接口
- 工具注册机制：内置时间查询、安全计算器，可自由扩展自定义工具
- 滑动窗口记忆：保留最近 N 条对话，控制上下文长度
- 命令行交互：开箱即用，输入问题即可对话
- 纯 Python 实现，仅依赖 `requests`

## 项目结构

```text
openclaw-space/
├── main.py                  # 命令行入口
├── requirements.txt         # 依赖清单
├── .env.example             # 环境变量示例
├── openclaw_agent/
│   ├── __init__.py          # 包入口
│   ├── config.py            # 配置加载
│   ├── llm.py               # LLM 客户端（OpenAI 兼容）
│   ├── tools.py             # 工具注册与内置工具
│   ├── memory.py            # 对话记忆
│   └── agent.py             # Agent 核心（ReAct 循环）
└── README.md
```

## 快速开始

### 1. 环境要求

- Python 3.9+
- 任一 OpenAI 兼容的模型服务（OpenAI / DeepSeek / Ollama 等）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
export OPENCLAW_API_KEY=sk-xxx
export OPENCLAW_API_BASE=https://api.openai.com/v1
export OPENCLAW_MODEL=gpt-4o-mini
```

### 4. 启动

```bash
python main.py
```

## 使用示例

```text
你 > 今天星期几？
OpenClaw > 今天是星期五。

你 > 帮我算一下 (12+8)*3.5
OpenClaw > (12+8)*3.5 = 70.0
```

## 扩展自定义工具

在 `openclaw_agent/tools.py` 中注册新工具：

```python
from openclaw_agent.tools import Tool, ToolRegistry

def my_tool(keyword: str) -> str:
    return f"查到的结果是：{keyword}"

registry = ToolRegistry.default()
registry.register(Tool(
    name="my_tool",
    description="自定义工具示例",
    parameters={
        "type": "object",
        "properties": {"keyword": {"type": "string"}},
        "required": ["keyword"],
    },
    func=my_tool,
))
```

## 相关链接

- OpenClaw 官网：https://openclaw.ai

## 许可证

MIT
