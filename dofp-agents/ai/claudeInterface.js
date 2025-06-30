const axios = require("axios");
require("dotenv").config();

const CLAUDE_API_KEY = process.env.CLAUDE_API_KEY;

async function getClaudeIntent(promptText, systemInstruction) {
  const headers = {
    "x-api-key": CLAUDE_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
  };

  const payload = {
    model: "claude-3-sonnet-20240229",
    max_tokens: 300,
    system: systemInstruction,
    messages: [
      { role: "user", content: promptText }
    ]
  };

  try {
    const res = await axios.post("https://api.anthropic.com/v1/messages", payload, { headers });
    const raw = res.data.content[0].text;
    return JSON.parse(raw); // Assuming Claude returns JSON
  } catch (err) {
    console.error("❌ Claude API Error:", err.response?.data || err.message);
    return null;
  }
}

module.exports = { getClaudeIntent };
