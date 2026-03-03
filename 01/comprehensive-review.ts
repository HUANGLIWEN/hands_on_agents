import { query, AgentDefinition } from "@anthropic-ai/claude-agent-sdk";

async function comprehensiveReview(directory: string) {
  for await (const message of query({
    prompt: `Perform a comprehensive code review of ${directory}.
Use the security-reviewer for security issues and test-analyzer for test coverage.`,
    options: {
      model: "opus",
      allowedTools: ["Read", "Glob", "Grep", "Task"], // Task enables subagents
      permissionMode: "bypassPermissions",
      maxTurns: 50,
      agents: {
        "security-reviewer": {
          description: "Security specialist for vulnerability detection",
          prompt: `You are a security expert. Focus on:
- SQL injection, XSS, CSRF vulnerabilities
- Exposed credentials and secrets
- Insecure data handling
- Authentication/authorization issues`,
          tools: ["Read", "Grep", "Glob"],
          model: "sonnet"
        } as AgentDefinition,

        "test-analyzer": {
          description: "Test coverage and quality analyzer",
          prompt: `You are a testing expert. Analyze:
- Test coverage gaps
- Missing edge cases
- Test quality and reliability
- Suggestions for additional tests`,
          tools: ["Read", "Grep", "Glob"],
          model: "haiku" // Use faster model for simpler analysis
        } as AgentDefinition
      }
    }
  })) {
    if (message.type === "assistant") {
      for (const block of message.message.content) {
        if ("text" in block) {
          console.log(block.text);
        } else if ("name" in block && block.name === "Task") {
          console.log(`\n🤖 Delegating to: ${(block.input as any).subagent_type}`);
        }
      }
    }
  }
}

comprehensiveReview(".");
