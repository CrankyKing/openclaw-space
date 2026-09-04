# OpenClaw Space

个人 OpenClaw 智能体工作空间 —— 基于开源 AI Agent 框架 [OpenClaw](https://openclaw.ai) 搭建，用于构建、配置和管理自己的 AI 智能体。

## 项目简介

本项目基于 [OpenClaw](https://openclaw.ai) 打造个人 AI 智能体工作空间。OpenClaw 是一款开源的 AI Agent 平台，通过对接大语言模型与多渠道通信能力，让智能体具备持久记忆、主动执行任务的能力，可自主完成发邮件、查资料、运行代码、管理文件等操作。

> 说明：具体使用场景可在下方补充，例如"用于日常自动化 / 个人助理 / 学习实验"等。

## 功能特性

- 基于 OpenClaw 的智能体配置与管理，支持多智能体并行运行
- 多渠道接入：Telegram、Discord、WhatsApp、微信等 50+ 通信渠道
- 复用 OpenClaw 5,700+ 内置技能，并支持自定义 Skill（Markdown / TypeScript）
- 模型无关：可切换 Claude、GPT、DeepSeek、Gemini、本地 Ollama 等
- 自托管部署，对话数据与 API 密钥完全本地掌控

## 技术栈

- OpenClaw（开源 AI Agent 框架，核心语言 TypeScript）
- Node.js 22+
- LLM：OpenAI / Anthropic / Google / 本地 Ollama 等（按需选择）

## 环境要求

- Node.js 22+
- npm / pnpm / bun（任一包管理器）

## 快速开始

```bash
# 1. 全局安装 OpenClaw
npm install -g openclaw@latest

# 2. 初始化并引导配置（选择模型、接入通信渠道）
openclaw onboard --install-daemon

# 3. 启动 Dashboard 开始使用
openclaw dashboard
```

## 项目结构

```text
openclaw-space/
├── README.md          # 项目说明
└── ...                # 智能体配置 / 自定义 Skills 等（待补充）
```

## 使用说明

【待补充】如何配置、运行和使用这个项目，例如智能体的创建与频道绑定方式。

## 相关链接

- OpenClaw 官网：https://openclaw.ai
- OpenClaw 官方文档：https://documentation.openclaw.ai

## 许可证

MIT
