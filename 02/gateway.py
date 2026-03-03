#!/usr/bin/env python3
"""网关 - 多通道支持

这个示例演示了如何添加HTTP通道。
在实际使用中，需要从bot_v2模块导入相关函数。
"""
from flask import Flask, request, jsonify
import threading

# 在实际使用中，从bot_v2导入这些函数
# from bot_v2 import load_session, run_agent_turn, SOUL, save_session

# 占位符函数，用于演示（实际使用时请导入上面的函数）
def load_session(user_id):
    raise NotImplementedError("请从bot_v2导入load_session函数")

def run_agent_turn(messages, system_prompt):
    raise NotImplementedError("请从bot_v2导入run_agent_turn函数")

def save_session(user_id, messages):
    raise NotImplementedError("请从bot_v2导入save_session函数")

# 示例SOUL（实际使用时应从bot_v2导入）
SOUL = """You are a helpful assistant."""

flask_app = Flask(__name__)

@flask_app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data["user_id"]
    messages = load_session(user_id)
    messages.append({"role": "user", "content": data["message"]})

    response_text, messages = run_agent_turn(messages, SOUL)

    save_session(user_id, messages)
    return jsonify({"response": response_text})

# 在后台线程中运行HTTP API
threading.Thread(target=lambda: flask_app.run(port=5000), daemon=True).start()

# Telegram机器人继续运行
# app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
# app.add_handler(MessageHandler(filters.TEXT, handle_message))
# app.run_polling()
