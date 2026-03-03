#!/usr/bin/env python3
"""工具定义"""
import subprocess

TOOLS = [
    {
        "name": "run_command",
        "description": "在用户电脑上运行shell命令",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "要运行的命令"}
            },
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": "从文件系统读取文件",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "向文件写入内容",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
                "content": {"type": "string", "description": "要写入的内容"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "web_search",
        "description": "在网上搜索信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索查询"}
            },
            "required": ["query"]
        }
    }
]

def execute_tool(name, input):
    """执行工具并返回结果"""
    if name == "run_command":
        result = subprocess.run(
            input["command"], shell=True,
            capture_output=True, text=True, timeout=30
        )
        return result.stdout + result.stderr

    elif name == "read_file":
        with open(input["path"], "r") as f:
            return f.read()

    elif name == "write_file":
        with open(input["path"], "w") as f:
            f.write(input["content"])
        return f"Wrote to {input['path']}"

    elif name == "web_search":
        # 简化版 - 实际使用真实的搜索API
        return f"Search results for: {input['query']}"

    return f"Unknown tool: {name}"
