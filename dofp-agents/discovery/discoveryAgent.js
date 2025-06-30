const axios = require("axios");
const { config } = require("../shared/config");

async function runDiscoveryAgent(userQuery) {
  const payload = {
    context: {
      domain: "retail",
      action: "search",
      country: { code: config.countryCode },
      city: { code: config.cityCode },
      timestamp: new Date().toISOString(),
      bap_id: config.bapId,
      bap_uri: config.bapUri
    },
    message: {
      intent: {
        item: {
          descriptor: {
            name: userQuery
          }
        }
      }
    }
  };

  try {
    const response = await axios.post(`${config.bapUri}/search`, payload);
    console.log("✅ Discovery Agent Response:\n", response.data);
  } catch (error) {
    console.error("❌ Discovery Agent Error:", error.message);
  }
}

// Sample run
runDiscoveryAgent("Buy sports shoes");
