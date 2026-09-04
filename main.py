"""OpenClaw Agent 命令行入口。"""
import sys

from openclaw_agent import Agent, Config


def main() -> None:
    config = Config.from_env()
    if not config.api_key:
        print("错误：未设置 OPENCLAW_API_KEY。")
        print("请先配置环境变量，例如：")
        print("  export OPENCLAW_API_KEY=sk-xxx")
        print("  export OPENCLAW_API_BASE=https://api.openai.com/v1")
        print("  export OPENCLAW_MODEL=gpt-4o-mini")
        print("更多配置见 .env.example")
        sys.exit(1)

    agent = Agent(config)
    print("OpenClaw Agent 已启动，输入问题开始对话，输入 exit 退出。\n")
    while True:
        try:
            user_input = input("你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "退出"):
            print("再见！")
            break
        try:
            answer = agent.run(user_input)
        except Exception as e:  # noqa: BLE001 —— 单次对话失败不中断程序
            print(f"[错误] {e}")
            continue
        print(f"OpenClaw > {answer}\n")


if __name__ == "__main__":
    main()
