#!/usr/bin/env python3
"""带持久会话的机器人"""
import json
import os
import anthropic
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

client = anthropic.Anthropic()
SESSIONS_DIR = "./sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

def get_session_path(user_id):
    return os.path.join(SESSIONS_DIR, f"{user_id}.jsonl")

def load_session(user_id):
    """从磁盘加载会话历史"""
    path = get_session_path(user_id)
    messages = []
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line))
    return messages

def append_to_session(user_id, message):
    """向会话文件追加单条消息"""
    path = get_session_path(user_id)
    with open(path, "a") as f:
        f.write(json.dumps(message) + "\n")

def save_session(user_id, messages):
    """用完整的消息列表覆盖会话文件"""
    path = get_session_path(user_id)
    with open(path, "w") as f:
        for message in messages:
            f.write(json.dumps(message) + "\n")

async def handle_message(update: Update, context):
    user_id = str(update.effective_user.id)
    user_message = update.message.text

    # 加载已有对话
    messages = load_session(user_id)

    # 添加新用户消息
    user_msg = {"role": "user", "content": user_message}
    messages.append(user_msg)
    append_to_session(user_id, user_msg)

    # 带着完整历史调用AI
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        messages=messages
    )

    # 保存助手回复
    assistant_msg = {"role": "assistant", "content": response.content[0].text}
    append_to_session(user_id, assistant_msg)

    await update.message.reply_text(response.content[0].text)

app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
