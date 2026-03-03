#!/usr/bin/env python3
"""上下文压缩 - 当对话太长时总结旧消息"""
import json

def estimate_tokens(messages):
    """粗略估算token数：约4个字符一个token"""
    return sum(len(json.dumps(m)) for m in messages) // 4

def compact_session(client, user_id, messages):
    """当上下文太长时总结旧消息"""
    if estimate_tokens(messages) < 100_000:  # 约128k窗口的80%
        return messages  # 不需要压缩

    split = len(messages) // 2
    old, recent = messages[:split], messages[split:]

    print("  Compacting session history...")

    summary = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": (
                "简洁地总结这段对话。保留：\n"
                "- 关于用户的关键事实（名字、偏好）\n"
                "- 做出的重要决定\n"
                "- 未完成的任务或待办事项\n\n"
                f"{json.dumps(old, indent=2)}"
            )
        }]
    )

    compacted = [{
        "role": "user",
        "content": f"[之前的对话摘要]\n{summary.content[0].text}"
    }] + recent

    save_session(user_id, compacted)
    return compacted
