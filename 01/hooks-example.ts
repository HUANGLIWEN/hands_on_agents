import { query, HookCallback, PreToolUseHookInput } from "@anthropic-ai/claude-agent-sdk";

// Hook callbacks receive three arguments:
// 1. input - details about the event (tool name, arguments, etc.)
// 2. toolUseId - correlates PreToolUse and PostToolUse events for the same call
// 3. context - contains AbortSignal for cancellation
const auditLogger: HookCallback = async (input, toolUseId, { signal }) => {
  if (input.hook_event_name === "PreToolUse") {
    const preInput = input as PreToolUseHookInput;
    console.log(`[AUDIT] ${new Date().toISOString()} - ${preInput.tool_name}`);
  }
  return {}; // Return empty object to allow the operation
};

const blockDangerousCommands: HookCallback = async (input, toolUseId, { signal }) => {
  if (input.hook_event_name === "PreToolUse") {
    const preInput = input as PreToolUseHookInput;
    if (preInput.tool_name === "Bash") {
      const command = (preInput.tool_input as any).command || "";
      if (command.includes("rm -rf") || command.includes("sudo")) {
        return {
          hookSpecificOutput: {
            hookEventName: "PreToolUse",
            permissionDecision: "deny",  // Block the tool from executing
            permissionDecisionReason: "Dangerous command blocked"
          }
        };
      }
    }
  }
  return {};
};

for await (const message of query({
  prompt: "Clean up temporary files",
  options: {
    model: "opus",
    allowedTools: ["Bash", "Glob"],
    maxTurns: 50,
    hooks: {
      // PreToolUse fires before each tool executes
      // Other hooks: PostToolUse, Stop, SessionStart, SessionEnd, etc.
      PreToolUse: [
        // Each entry has an optional matcher (regex) and an array of callbacks
        // No matcher = runs for ALL tool calls
        { hooks: [auditLogger] },

        // matcher: 'Bash' = only runs when tool_name matches 'Bash'
        // Use regex for multiple tools: 'Bash|Write|Edit'
        { matcher: "Bash", hooks: [blockDangerousCommands] }
      ]
    }
  }
})) {
  if (message.type === "assistant") {
    for (const block of message.message.content) {
      if ("text" in block) {
        console.log(block.text);
      }
    }
  }
}
