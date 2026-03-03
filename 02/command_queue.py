#!/usr/bin/env python3
"""命令队列 - 防止竞态条件"""
from collections import defaultdict
import threading

# 每个会话一个锁
session_locks = defaultdict(threading.Lock)

# 使用示例：
# async def handle_message(update: Update, context):
#     user_id = str(update.effective_user.id)
#
#     with session_locks[user_id]:
#         messages = load_session(user_id)
#         messages = compact_session(user_id, messages)
#         messages.append({"role": "user", "content": update.message.text})
#
#         response_text, messages = run_agent_turn(messages, SOUL)
#
#         save_session(user_id, messages)
#
#     await update.message.reply_text(response_text)
