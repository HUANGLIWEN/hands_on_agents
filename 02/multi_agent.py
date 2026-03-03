#!/usr/bin/env python3
"""多Agent路由"""
# 假设SOUL已经定义
# from bot_v2 import SOUL

AGENTS = {
    "main": {
        "name": "Jarvis",
        "soul": SOUL,  # 我们现有的SOUL
        "session_prefix": "agent:main",
    },
    "researcher": {
        "name": "Scout",
        "soul": """你是Scout，一个研究专家。
你的工作：查找信息并引用来源。每个观点都需要证据。
使用工具收集数据。全面但简洁。
将重要发现保存到记忆中供其他agent参考。""",
        "session_prefix": "agent:researcher",
    },
}

def resolve_agent(message_text):
    """根据前缀命令将消息路由到正确的agent"""
    if message_text.startswith("/research "):
        return "researcher", message_text[len("/research "):]
    return "main", message_text

# 使用示例：
# async def handle_message(update: Update, context):
#     user_id = str(update.effective_user.id)
#     agent_id, message_text = resolve_agent(update.message.text)
#     agent = AGENTS[agent_id]
#     session_key = f"{agent['session_prefix']}:{user_id}"
#
#     with session_locks[session_key]:
#         messages = load_session(session_key)
#         messages = compact_session(session_key, messages)
#         messages.append({"role": "user", "content": message_text})
#
#         response_text, messages = run_agent_turn(messages, agent["soul"])
#
#         save_session(session_key, messages)
#
#     await update.message.reply_text(f"[{agent['name']}] {response_text}")
