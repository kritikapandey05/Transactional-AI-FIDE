const { getClaudeIntent } = require("../ai/claudeInterface");
const { runOrderingAgent } = require("./orderingAgent");

async function runOrderingWithAI(prompt) {
  const instruction = `Extract the provider and items to place an order in the following format. Use the format as an example:
{
  "providerId": "provider-123",
  "items": [
    { "id": "item-001", "quantity": { "count": 1 } }
  ]
}`;
  const orderData = await getClaudeIntent(prompt, instruction);
  if (orderData) runOrderingAgent(orderData);
}

//runOrderingWithAI("Place an order for 1 item from provider 123");
