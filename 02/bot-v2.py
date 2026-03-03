#!/usr/bin/env python3
"""有人格的机器人"""
import json
import os
import anthropic
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

client = anthropic.Anthropic()
SESSIONS_DIR = "./sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

# SOUL.md - 定义Agent的身份、行为和边界
SOUL = """
# 你是谁

**名字：** Jarvis
**角色：** 个人AI助手

## 个性
- 真正有帮助，而不是装模作样有帮助
- 跳过"好问题！"这种套话，直接帮忙
- 可以有观点，允许不同意
- 需要简洁时简洁，需要详细时详细

## 边界
- 私事保持私密
- 有疑问时，先询问再对外行动
- 你不是用户的声音，代人发消息要谨慎

## 记忆
记住对话中的重要细节。
如果重要就写下来。
"""

def get_session_path(user_id):
    return os.path.join(SESSIONS_DIR, f"{user_id}.jsonl")

def load_session(user_id):
    path = get_session_path(user_id)
    messages = []
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line))
    return messages

def append_to_session(user_id, message):
    path = get_session_path(user_id)
    with open(path, "a") as f:
        f.write(json.dumps(message) + "\n")

async def handle_message(update: Update, context):
    user_id = str(update.effective_user.id)
    messages = load_session(user_id)

    user_msg = {"role": "user", "content": update.message.text}
    messages.append(user_msg)
    append_to_session(user_id, user_msg)

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        system=SOUL,  # <-- 在这里注入人格
        messages=messages
    )

    assistant_msg = {"role": "assistant", "content": response.content[0].text}
    append_to_session(user_id, assistant_msg)

    await update.message.reply_text(response.content[0].text)

app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
