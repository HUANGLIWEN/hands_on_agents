import { query } from "@anthropic-ai/claude-agent-sdk";

async function interactiveReview() {
  let sessionId: string | undefined;

  // Initial review
  for await (const message of query({
    prompt: "Review this codebase and identify the top 3 issues",
    options: {
      model: "opus",
      allowedTools: ["Read", "Glob", "Grep"],
      permissionMode: "bypassPermissions",
      maxTurns: 50
    }
  })) {
    if (message.type === "system" && message.subtype === "init") {
      sessionId = message.session_id;
    }
    // ... handle messages
  }

  // Follow-up question using same session
  if (sessionId) {
    for await (const message of query({
      prompt: "Now show me how to fix the most critical issue",
      options: {
        resume: sessionId, // Continue the conversation
        allowedTools: ["Read", "Glob", "Grep"],
        maxTurns: 50
      }
    })) {
      // Claude remembers the previous context
    }
  }
}
