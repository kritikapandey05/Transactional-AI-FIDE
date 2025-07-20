from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import requests

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# FastAPI app
app = FastAPI()

class BecknResponse(BaseModel):
    beckn_json: dict

@app.post("/mcp/beckn-to-nlp")
async def beckn_to_nlp(payload: BecknResponse):

    prompt = f"""
You are a helpful assistant that reads JSON responses from the Beckn 1.1 protocol and explains them in clear, concise natural language for the end user.

Always refer to the field `context.action` to understand what the response represents, and summarize accordingly.

Instructions:

1. If `context.action` is `"on_search"`:
   - List all available products.
   - For each product, mention:
     - **Item name**
     - **Brand or provider**
     - **Price** (if available)
     - Any extra attribute like **battery capacity**, **delivery time**, etc.

2. If `context.action` is `"on_select"`, `"on_init"`, or `"on_confirm"`:
   - Clearly explain what the user selected:
     - Item name
     - Quantity
     - Provider
     - Price
     - Delivery address
     - Billing details (if available)
   - Format it like a short purchase summary.

3. If `context.action` is `"on_cancel"` or `"on_status"`:
   - Clearly state:
     - Current status of the order
     - If it's a cancellation, mention whether it succeeded or failed
     - Show order ID and provider if present

Rules:
- DO NOT show technical fields like `bap_uri`, `message_id`, `transaction_id`, etc.
- Do NOT output any JSON or code.
- Make your tone friendly and conversational.
- Focus only on what a human user would care about.

---

Here is the Beckn response JSON:

{json.dumps(payload.beckn_json, indent=2)}

Now respond with a natural language summary:
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        reply = response.choices[0].message.content.strip()
        return {"natural_language_response": reply}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
