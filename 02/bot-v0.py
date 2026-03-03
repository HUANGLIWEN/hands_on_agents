#!/usr/bin/env python3
"""最简单的AI机器人"""
import os
import anthropic
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

client = anthropic.Anthropic()

async def handle_message(update: Update, context):
    user_message = update.message.text

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": user_message}]
    )

    await update.message.reply_text(response.content[0].text)

app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
