const axios = require("axios");
const { config } = require("../shared/config");

async function runFulfillmentAgent(orderId) {
  const payload = {
    context: {
      domain: "retail",
      action: "status",
      country: { code: config.countryCode },
      city: { code: config.cityCode },
      timestamp: new Date().toISOString(),
      bap_id: config.bapId,
      bap_uri: config.bapUri
    },
    message: {
      order_id: orderId
    }
  };

  try {
    const response = await axios.post(`${config.bapUri}/status`, payload);
    console.log("✅ Fulfillment Agent Response:\n", response.data);
  } catch (error) {
    console.error("❌ Fulfillment Agent Error:", error.message);
  }
}

// Sample run
runFulfillmentAgent("order-xyz-123");
