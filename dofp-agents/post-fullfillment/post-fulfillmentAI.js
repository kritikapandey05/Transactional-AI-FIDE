const { getClaudeIntent } = require("../ai/claudeInterface");
const { runPostFulfillmentAgent } = require("./postFulfillmentAgent");

async function runPostFulfillmentWithAI(prompt) {
  const instruction = `Extract order feedback and rating. Use following format as an example:
{
  "id": "order-xyz-123",
  "value": 4.5,
  "feedback": "It arrived quickly!"
}`;
  const feedback = await getClaudeIntent(prompt, instruction);
  if (feedback) runPostFulfillmentAgent(feedback);
}

//runPostFulfillmentWithAI("I'd give 4.5 stars. It arrived quickly!");
