// 1. Define tools with their schemas
const tools = [{
  name: "get_weather",
  description: "Get current weather for a city",
  input_schema: {
    type: "object",
    properties: {
      city: { type: "string", description: "City name" }
    },
    required: ["city"]
  }
}];

// 2. Write an executor for each tool
function executeTool(name: string, input: any): string {
  if (name === "get_weather") {
    return fetchWeatherAPI(input.city);
  }
  throw new Error(`Unknown tool: ${name}`);
}

// 3. Run the agent loop
const messages = [{ role: "user", content: "What's the weather in Tokyo?" }];

let response = await client.messages.create({
  model: "claude-opus-4-5-20251101",
  tools,
  messages
});

while (response.stop_reason === "tool_use") {
  messages.push({ role: "assistant", content: response.content });

  const toolResults = response.content
    .filter(block => block.type === "tool_use")
    .map(toolUse => ({
      type: "tool_result",
      tool_use_id: toolUse.id,
      content: executeTool(toolUse.name, toolUse.input)
    }));

  messages.push({ role: "user", content: toolResults });
  response = await client.messages.create({ model, tools, messages });
}

const textBlock = response.content.find(block => block.type === "text");
if (textBlock && textBlock.type === "text") {
  console.log("Final response:", textBlock.text);
}
