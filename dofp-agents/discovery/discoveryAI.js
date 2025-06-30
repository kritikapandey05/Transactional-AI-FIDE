const { getClaudeIntent } = require("../ai/claudeInterface");
const { runDiscoveryAgent } = require("./discoveryAgent");

async function runDiscoveryWithAI(prompt) {
  const instruction = `You are a helpful assistant. Given a user prompt, extract an object with the following format:
{
  "query": "<what to search for>",
  "location": {
    "city": "std:080",
    "country": "IND"
  }
}`;
  const intent = await getClaudeIntent(prompt, instruction);
  if (intent) runDiscoveryAgent(intent.query, intent.location);
}

// Example
//runDiscoveryWithAI("Find me Adidas shoes under ₹2000");
