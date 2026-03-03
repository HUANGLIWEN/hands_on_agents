import { query } from "@anthropic-ai/claude-agent-sdk";

async function reviewCode(directory: string) {
  console.log(`\n🔍 Starting code review for: ${directory}\n`);

  for await (const message of query({
    prompt: `Review the code in ${directory} for:
1. Bugs and potential crashes
2. Security vulnerabilities
3. Performance issues
4. Code quality improvements

Be specific about file names and line numbers.`,
    options: {
      model: "opus",
      allowedTools: ["Read", "Glob", "Grep"],
      permissionMode: "bypassPermissions", // Auto-approve read operations
      maxTurns: 50
    }
  })) {
    // Show Claude's analysis as it happens
    if (message.type === "assistant") {
      for (const block of message.message.content) {
        if ("text" in block) {
          console.log(block.text);
        } else if ("name" in block) {
          console.log(`\n📁 Using ${block.name}...`);
        }
      }
    }

    // Show completion status
    if (message.type === "result") {
      if (message.subtype === "success") {
        console.log(`\n✅ Review complete! Cost: $${message.total_cost_usd.toFixed(4)}`);
      } else {
        console.log(`\n❌ Review failed: ${message.subtype}`);
      }
    }
  }
}

// Review the current directory
reviewCode(".");
