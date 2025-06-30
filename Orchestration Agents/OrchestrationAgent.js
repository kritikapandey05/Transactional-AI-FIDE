const axios = require("axios");
const { config } = require("../shared/config");

class OrchestrationAgent {
  constructor() {
    this.context = {
      domain: "retail",
      country: { code: config.countryCode },
      city: { code: config.cityCode },
      bap_id: config.bapId,
      bap_uri: config.bapUri,
      timestamp: new Date().toISOString()
    };
  }

  async run(userQuery) {
    console.log(`\n🚀 Starting transaction for: "${userQuery}"\n`);

    const catalog = await this.search(userQuery);
    if (!catalog) return;

    const selectedItem = this.selectItem(catalog);
    if (!selectedItem) return;

    const quote = await this.getQuote(selectedItem);
    if (!quote) return;

    const order = await this.initOrder(quote);
    if (!order) return;

    const confirmed = await this.confirmOrder(order);
    if (!confirmed) return;

    await this.checkFulfillment(confirmed);

    console.log(`🎉 Transaction completed for query: "${userQuery}"`);
  }

  buildContext(action) {
    return {
      ...this.context,
      action,
      transaction_id: this.transactionId || this.generateTransactionId(),
      message_id: this.generateMessageId(),
      timestamp: new Date().toISOString()
    };
  }

  generateTransactionId() {
    this.transactionId = `txn-${Date.now()}`;
    return this.transactionId;
  }

  generateMessageId() {
    return `msg-${Date.now()}`;
  }

  async search(userQuery) {
    const payload = {
      context: this.buildContext("search"),
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
      const res = await axios.post(`${config.bapUri}/search`, payload);
      console.log("🔍 Search successful.");
      return res.data.message.catalog;
    } catch (err) {
      console.error("❌ Search failed:", err.message);
      return null;
    }
  }

  selectItem(catalog) {
    const provider = catalog.providers?.[0];
    const item = provider?.items?.[0];

    if (!item || !provider) {
      console.error("❌ No valid provider/item found.");
      return null;
    }

    console.log(`✅ Selected item "${item.descriptor.name}" from provider "${provider.descriptor.name}".`);
    return { provider, item };
  }

  async getQuote({ provider, item }) {
    const payload = {
      context: this.buildContext("select"),
      message: {
        order: {
          items: [item],
          provider: {
            id: provider.id
          }
        }
      }
    };

    try {
      const res = await axios.post(`${config.bapUri}/select`, payload);
      console.log("💰 Quote received.");
      return res.data.message.order;
    } catch (err) {
      console.error("❌ Quote request failed:", err.message);
      return null;
    }
  }

  async initOrder(order) {
    const payload = {
      context: this.buildContext("init"),
      message: { order }
    };

    try {
      const res = await axios.post(`${config.bapUri}/init`, payload);
      console.log("🛒 Order initialized.");
      return res.data.message.order;
    } catch (err) {
      console.error("❌ Order init failed:", err.message);
      return null;
    }
  }

  async confirmOrder(order) {
    const payload = {
      context: this.buildContext("confirm"),
      message: { order }
    };

    try {
      const res = await axios.post(`${config.bapUri}/confirm`, payload);
      console.log("✅ Order confirmed. Transaction ID:", this.transactionId);
      return res.data.message.order;
    } catch (err) {
      console.error("❌ Order confirmation failed:", err.message);
      return null;
    }
  }

  async checkFulfillment(order) {
    const fulfillmentStatus = order?.fulfillments?.[0]?.state?.descriptor?.code;
    console.log(`📦 Fulfillment status: ${fulfillmentStatus || "Unknown"}`);
  }
}

// Sample run
const orchestrator = new OrchestrationAgent();
orchestrator.run("Buy sports shoes");
