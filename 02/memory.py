#!/usr/bin/env python3
"""长期记忆系统"""
import os

MEMORY_DIR = "./memory"

# 长期记忆工具定义
MEMORY_TOOLS = [
    {
        "name": "save_memory",
        "description": "将重要信息保存到长期记忆中。用于用户偏好、关键事实和值得跨会话记住的任何内容。",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "短标签，例如 'user-preferences', 'project-notes'"
                },
                "content": {
                    "type": "string",
                    "description": "要记住的信息"
                }
            },
            "required": ["key", "content"]
        }
    },
    {
        "name": "memory_search",
        "description": "在长期记忆中搜索相关信息。在对话开始时使用以回忆之前会话的上下文。",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "要搜索的内容"
                }
            },
            "required": ["query"]
        }
    }
]

def execute_memory_tool(name, input):
    """执行记忆工具"""
    if name == "save_memory":
        os.makedirs(MEMORY_DIR, exist_ok=True)
        filepath = os.path.join(MEMORY_DIR, f"{input['key']}.md")
        with open(filepath, "w") as f:
            f.write(input["content"])
        return f"Saved to memory: {input['key']}"

    elif name == "memory_search":
        query = input["query"].lower()
        results = []
        if os.path.exists(MEMORY_DIR):
            for fname in os.listdir(MEMORY_DIR):
                if fname.endswith(".md"):
                    with open(os.path.join(MEMORY_DIR, fname), "r") as f:
                        content = f.read()
                    if any(word in content.lower() for word in query.split()):
                        results.append(f"--- {fname} ---\n{content}")
        return "\n\n".join(results) if results else "No matching memories found."

    return f"Unknown tool: {name}"
