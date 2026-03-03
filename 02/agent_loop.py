#!/usr/bin/env python3
"""Agent循环 - 让AI可以决定何时使用工具"""
import json

def serialize_content(content):
    """将API响应内容块转换为JSON可序列化的字典"""
    serialized = []
    for block in content:
        if hasattr(block, "text"):
            serialized.append({"type": "text", "text": block.text})
        elif block.type == "tool_use":
            serialized.append({
                "type": "tool_use",
                "id": block.id,
                "name": block.name,
                "input": block.input
            })
    return serialized

def run_agent_turn(client, messages, system_prompt, tools):
    """运行一个完整的agent回合（可能涉及多次工具调用）"""
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            messages=messages
        )

        content = serialize_content(response.content)

        # 如果AI完成了（没有工具调用），返回文本
        if response.stop_reason == "end_turn":
            text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    text += block.text
            messages.append({"role": "assistant", "content": content})
            return text, messages

        # 处理工具调用
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  Tool: {block.name}({json.dumps(block.input)})")
                    from tools import execute_tool
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })

            messages.append({"role": "user", "content": tool_results})
