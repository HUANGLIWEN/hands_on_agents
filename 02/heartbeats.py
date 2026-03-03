#!/usr/bin/env python3
"""定时任务（心跳）- 周期性触发agent"""
import schedule
import time
import threading

# 假设这些已经定义
# from command_queue import session_locks
# from bot_v2 import load_session, run_agent_turn, SOUL, save_session

def setup_heartbeats():
    """配置周期性agent任务"""

    def morning_briefing():
        print("\n⏰ Heartbeat: morning briefing")
        # 使用独立的会话key，这样cron不会污染主聊天
        session_key = "cron:morning-briefing"

        with session_locks[session_key]:
            messages = load_session(session_key)
            messages.append({
                "role": "user",
                "content": "早上好！查看今天的日期并给我一句励志名言。"
            })

            response_text, messages = run_agent_turn(messages, SOUL)
            save_session(session_key, messages)

        print(f"🤖 {response_text}\n")
        # 生产环境中，你还会发送到Telegram/Discord

    schedule.every().day.at("07:30").do(morning_briefing)

    # 在后台线程中运行调度器
    def scheduler_loop():
        while True:
            schedule.run_pending()
            time.sleep(60)

    threading.Thread(target=scheduler_loop, daemon=True).start()

# 调用方式：在启动时、run_polling()之前调用
# setup_heartbeats()
