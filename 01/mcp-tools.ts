import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

// Create your custom MCP server
const customServer = createSdkMcpServer({
  name: "code-metrics",
  version: "1.0.0",
  tools: [
    // Define a custom tool using the `tool` helper
    // Arguments: name, description, input schema, handler function
    tool(
      "analyze_complexity",
      "Calculate cyclomatic complexity for a file",
      {
        // Zod schema defines what inputs the tool accepts
        filePath: z.string().describe("Path to the file to analyze")
      },
      // Handler function - runs when Claude calls the tool
      async (args) => {
        // In real implementation, calculate actual complexity
        const complexity = Math.floor(Math.random() * 20) + 1;

        // Return format required by MCP - array of content blocks
        return {
          content: [{
            type: "text",
            text: `Cyclomatic complexity for ${args.filePath}: ${complexity}`
          }]
        };
      }
    )
  ]
});

async function analyzeCode(filePath: string) {
  for await (const message of query({
    prompt: `Analyze the complexity of ${filePath}`,
    options: {
      model: "opus",

      // Register the custom MCP server
      // The key ("code-metrics") becomes part of the tool name
      mcpServers: {
        "code-metrics": customServer
      },

      // Specify which tools Claude can use
      // MCP tools follow the pattern: mcp__<server-name>__<tool-name>
      allowedTools: ["Read", "mcp__code-metrics__analyze_complexity"],

      // Maximum number of back-and-forth turns before stopping
      maxTurns: 50
    }
  })) {
    // Handle assistant messages (Claude's responses and tool calls)
    if (message.type === "assistant") {
      for (const block of message.message.content) {
        // Text blocks contain Claude's written responses
        if ("text" in block) {
          console.log(block.text);
        }
      }
    }

    // Handle the final result when the agent loop completes
    if (message.type === "result") {
      console.log("Done:", message.subtype); // "success" or an error type
    }
  }
}

analyzeCode("main.ts");
