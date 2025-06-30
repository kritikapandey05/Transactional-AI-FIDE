const axios = require("axios");
const { config } = require("../shared/config");

async function runOrderingAgent(orderDetails) {
  const payload = {
    context: {
      domain: "retail",
      action: "init",
      country: { code: config.countryCode },
      city: { code: config.cityCode },
      timestamp: new Date().toISOString(),
      bap_id: config.bapId,
      bap_uri: config.bapUri
    },
    message: {
      order: {
        provider: { id: orderDetails.providerId },
        items: orderDetails.items
      }
    }
  };

  try {
    const response = await axios.post(`${config.bapUri}/init`, payload);
    console.log("✅ Ordering Agent Response:\n", response.data);
  } catch (error) {
    console.error("❌ Ordering Agent Error:", error.message);
  }
}

// Sample run
runOrderingAgent({
  providerId: "provider-123",
  items: [{ id: "item-001", quantity: { count: 1 } }]
});
