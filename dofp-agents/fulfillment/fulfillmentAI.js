const { getClaudeIntent } = require("../ai/claudeInterface");
const { runFulfillmentAgent } = require("./fulfillmentAgent");

async function runFulfillmentWithAI(prompt) {
  const instruction = `Extract the order ID to check order status. Returnin the following format for example:
"order-xyz-123"`;
  const orderId = await getClaudeIntent(prompt, instruction);
  if (orderId) runFulfillmentAgent(orderId);
}

//runFulfillmentWithAI("Track the status of my last order");
