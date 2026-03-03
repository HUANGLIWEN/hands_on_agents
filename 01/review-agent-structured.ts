import { query } from "@anthropic-ai/claude-agent-sdk";

const reviewSchema = {
  type: "object",
  properties: {
    issues: {
      type: "array",
      items: {
        type: "object",
        properties: {
          severity: { type: "string", enum: ["low", "medium", "high", "critical"] },
          category: { type: "string", enum: ["bug", "security", "performance", "style"] },
          file: { type: "string" },
          line: { type: "number" },
          description: { type: "string" },
          suggestion: { type: "string" }
        },
        required: ["severity", "category", "file", "description"]
      }
    },
    summary: { type: "string" },
    overallScore: { type: "number" }
  },
  required: ["issues", "summary", "overallScore"]
};

async function reviewCodeStructured(directory: string) {
  for await (const message of query({
    prompt: `Review the code in ${directory}. Identify all issues.`,
    options: {
      model: "opus",
      allowedTools: ["Read", "Glob", "Grep"],
      permissionMode: "bypassPermissions",
      maxTurns: 50,
      outputFormat: {
        type: "json_schema",
        schema: reviewSchema
      }
    }
  })) {
    if (message.type === "result" && message.subtype === "success") {
      const review = message.structured_output as {
        issues: Array<{
          severity: string;
          category: string;
          file: string;
          line?: number;
          description: string;
          suggestion?: string;
        }>;
        summary: string;
        overallScore: number;
      };

      console.log(`\n📊 Code Review Results\n`);
      console.log(`Score: ${review.overallScore}/100`);
      console.log(`Summary: ${review.summary}\n`);

      for (const issue of review.issues) {
        const icon = issue.severity === "critical" ? "🔴" :
                     issue.severity === "high" ? "🟠" :
                     issue.severity === "medium" ? "🟡" : "🟢";
        console.log(`${icon} [${issue.category.toUpperCase()}] ${issue.file}${issue.line ? `:${issue.line}` : ""}`);
        console.log(`   ${issue.description}`);
        if (issue.suggestion) {
          console.log(`   💡 ${issue.suggestion}`);
        }
        console.log();
      }
    }
  }
}

reviewCodeStructured(".");
