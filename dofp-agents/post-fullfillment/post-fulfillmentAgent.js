const axios = require("axios");
const { config } = require("../shared/config");

async function runPostFulfillmentAgent(feedbackPayload) {
  const payload = {
    context: {
      domain: "retail",
      action: "rating",
      country: { code: config.countryCode },
      city: { code: config.cityCode },
      timestamp: new Date().toISOString(),
      bap_id: config.bapId,
      bap_uri: config.bapUri
    },
    message: {
      rating: feedbackPayload
    }
  };

  try {
    const response = await axios.post(`${config.bapUri}/rating`, payload);
    console.log("✅ Post-fulfillment Agent Response:\n", response.data);
  } catch (error) {
    console.error("❌ Post-fulfillment Agent Error:", error.message);
  }
}

// Sample run
runPostFulfillmentAgent({
  id: "order-xyz-123",
  value: 4.5,
  feedback: "Quick delivery!"
});
