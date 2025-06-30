const { getClaudeIntent } = require("../ai/claudeInterface");
const { OrchestrationAgent } = require("./orchestrationAgent"); // assuming you export it properly

async function runOrchestrationWithAI(prompt) {
  const instruction = `You are an AI agent that extracts e-commerce intents for transactional AI. 
Given a user prompt, return a JSON object with the following format:

{
  "query": "<product to search for>",
  "location": {
    "city": "std:080",
    "country": "IND"
  }
}

Only include the item name as 'query' — no filters, prices, or brands.`;

  const intent = await getClaudeIntent(prompt, instruction);

  if (!intent || !intent.query) {
    console.error("❌ Could not extract intent from prompt.");
    return;
  }

  console.log(`🧠 Claude extracted query: "${intent.query}"`);
  const orchestrator = new OrchestrationAgent();
  orchestrator.run(intent.query); // just pass the query for now
}

// Example
// runOrchestrationWithAI("Order Nike running shoes for Bangalore");
