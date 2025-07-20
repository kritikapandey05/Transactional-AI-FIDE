from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import requests
from datetime import datetime
import uuid
from typing import List

# Load .env and initialize OpenAI client
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = FastAPI()

class PromptInput(BaseModel):
    user_input: str
    chat_history: List[str] = []

@app.post("/mcp/nlp-to-beckn")
async def generate_beckn_json(data: PromptInput):
    chat_prompt="\n".join(data.chat_history+[f"User: {data.user_input}"])
    # Few-shot prompt
    prompt = f"""
You are a smart assistant that converts natural language into valid Beckn 1.1 protocol-compliant API JSONs for a number of domains.

Use ONLY the structure shown in the following DOFP examples: Discover, Order, Fulfill, and Post-Fulfill.
Always return ONLY the JSON. No text, explanation, or comments.

Discovery Stage
POST search
JSON: 
{{
    "context": {{
        "ttl": "PT10M",
        "action": "search",
        "timestamp": "2025-06-19T16:04:05.236Z",
        "message_id": "cdbd53a8-512a-4d4e-a805-0258306635ac",
        "transaction_id": "862ca4b3-a1f4-49b2-92ad-d81f19dc1a60",
        "domain": "deg:retail",
        "version": "1.1.0",
        "bap_id": "bap-network",
        "bap_uri": "http://bap-network:5002",
        "location": {{
            "country": {{
                "code": "IND"
            }},
            "city": {{
                "code": "std:080"
            }}
        }},
        "bpp_id": "bpp-network",
        "bpp_uri": "http://bpp-network:6002"
    }},
    "message": {{
        "intent": {{
            "item": {{
                "descriptor": {{
                    "name": "Battery"
                }}
            }}
        }}
    }}
}}

Ordering Stage
POST select
JSON:
{{
    "context": {{
        "ttl": "PT10M",
        "action": "select",
        "timestamp": "2025-06-21T07:13:41.888Z",
        "message_id": "df0cb629-fafa-4b52-bf9b-01f1a8b88553",
        "transaction_id": "862ca4b3-a1f4-49b2-92ad-d81f19dc1a60",
        "domain": "deg:retail",
        "version": "1.1.0",
        "bap_id": "bap-network",
        "bap_uri": "http://bap-network:5002",
        "location": {{
            "country": {{
                "code": "IND"
            }},
            "city": {{
                "code": "std:080"
            }}
        }},
        "bpp_id": "bpp-network",
        "bpp_uri": "http://bpp-network:6002"
    }},
    "message": {{
        "order": {{
            "provider": {{
                "id": "19"
            }},
            "items": [
                {{
                    "id": "19",
                    "quantity": {{
                        "selected": {{
                            "count": 2
                        }}
                    }}
                }}
            ],
            "fulfillments": [
                {{
                    "id": "3",
                    "stops": [
                        {{
                            "type": "end",
                            "location": {{
                                "gps": "13.2008459,77.708736",
                                "address": "Your delivery address here"
                            }}
                        }}
                    ]
                }}
            ]
        }}
    }}
}}

POST init
JSON:
{{
  "context": {{
    "domain": "deg:retail",
    "location": {{
      "country": {{
        "code": "IND"
      }},
      "city": {{
        "code": "std:080"
      }}
    }},
    "action": "init",
    "version": "1.1.0",
    "bap_id": "bap-network",
    "bap_uri": "http://bap-network:5002",
    "bpp_id": "bpp-network",
    "bpp_uri": "http://bpp-network:6002",
    "transaction_id": "862ca4b3-a1f4-49b2-92ad-d81f19dc1a60",
    "message_id": "{{{{randomUUID}}}}",
    "timestamp": "2025-06-21T07:35:00.000Z"
  }},
  "message": {{
    "order": {{
      "provider": {{
        "id": "19"
      }},
      "items": [
        {{
          "id": "19",
          "quantity": {{
            "selected": {{
              "count": 2
            }}
          }}
        }}
      ],
      "fulfillments": [
        {{
          "id": "3",
          "type": "Delivery in 5 Days",
          "stops": [
            {{
              "location": {{
                "gps": "13.2008459,77.708736",
                "address": "123, Terminal 1, Kempegowda Int'l Airport Rd, A - Block, Gangamuthanahalli, Karnataka 560300, India",
                "city": {{
                  "name": "Gangamuthanahalli"
                }},
                "state": {{
                  "name": "Karnataka"
                }},
                "country": {{
                  "code": "IND"
                }},
                "area_code": "75001"
              }},
              "contact": {{
                "phone": "919246394908",
                "email": "nc.rehman@gmail.com"
              }}
            }}
          ],
          "customer": {{
            "person": {{
              "name": "Motiur Rehman"
            }},
            "contact": {{
              "phone": "919122343344"
            }}
          }}
        }}
      ],
      "billing": {{
        "name": "Motiur Rehman",
        "phone": "9191223433",
        "email": "nc.rehman@gmail.com",
        "address": "123, Terminal 1, Kempegowda Int'l Airport Rd, A - Block, Gangamuthanahalli, Karnataka 560300, India",
        "city": {{
          "name": "Gangamuthanahalli"
        }},
        "state": {{
          "name": "Karnataka"
        }},
        "country": {{
          "code": "IND"
        }}
      }}
    }}
  }}
}}

POST confirm
JSON:
{{
  "context": {{
    "domain": "deg:retail",
    "location": {{
      "country": {{
        "code": "IND"
      }},
      "city": {{
        "code": "std:080"
      }}
    }},
    "action": "confirm",
    "version": "1.1.0",
    "bap_id": "bap-network",
    "bap_uri": "http://bap-network:5002",
    "bpp_id": "bpp-network",
    "bpp_uri": "http://bpp-network:6002",
    "message_id": "{{{{randomUUID}}}}",
    "transaction_id": "862ca4b3-a1f4-49b2-92ad-d81f19dc1a60",
    "timestamp": "2025-06-21T07:45:00.000Z"
  }},
  "message": {{
    "order": {{
      "provider": {{
        "id": "19"
      }},
      "items": [
        {{
          "id": "19",
          "quantity": {{
            "selected": {{
              "count": 2
            }}
          }}
        }}
      ],
      "fulfillments": [
        {{
          "id": "3",
          "type": "Delivery in 5 Days",
          "stops": [
            {{
              "location": {{
                "gps": "13.2008459,77.708736",
                "address": "123, Terminal 1, Kempegowda Int'l Airport Rd, A - Block, Gangamuthanahalli, Karnataka 560300, India",
                "city": {{
                  "name": "Gangamuthanahalli"
                }},
                "state": {{
                  "name": "Karnataka"
                }},
                "country": {{
                  "code": "IND"
                }},
                "area_code": "75001"
              }},
              "contact": {{
                "phone": "919246394908",
                "email": "nc.rehman@gmail.com"
              }}
            }}
          ],
          "customer": {{
            "person": {{
              "name": "Motiur Rehman"
            }},
            "contact": {{
              "phone": "919122343344"
            }}
          }}
        }}
      ],
      "billing": {{
        "name": "Motiur Rehman",
        "phone": "9191223433",
        "email": "nc.rehman@gmail.com",
        "address": "123, Terminal 1, Kempegowda Int'l Airport Rd, A - Block, Gangamuthanahalli, Karnataka 560300, India",
        "city": {{
          "name": "Gangamuthanahalli"
        }},
        "state": {{
          "name": "Karnataka"
        }},
        "country": {{
          "code": "IND"
        }}
      }},
      "payments": [
        {{
          "collected_by": "BPP",
          "status": "PAID",
          "type": "PRE-ORDER",
          "params": {{
            "price": "101500",
            "currency": "INR"
          }}
        }}
      ]
    }}
  }}
}}

Fulfillment Stage
POST status
JSON:
{{
  "context": {{
    "domain": "deg:retail",
    "location": {{
      "country": {{
        "code": "IND"
      }},
      "city": {{
        "code": "std:080"
      }}
    }},
    "action": "status",
    "version": "1.1.0",
    "bap_id": "bap-network",
    "bap_uri": "http://bap-network:5002",
    "bpp_id": "bpp-network",
    "bpp_uri": "http://bpp-network:6002",
    "message_id": "{{{{randomUUID}}}}",
    "transaction_id": "862ca4b3-a1f4-49b2-92ad-d81f19dc1a60",
    "timestamp": "2025-06-21T07:45:00.000Z",
    "ttl": "PT10M"
  }},
  "message": {{
    "order_id": "3780"
  }}
}}

Now generate the correct JSON for the input: "{data.user_input}"
"""

    try:
        # Step 1: Call OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Beckn JSON generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        raw_output = response.choices[0].message.content.strip()

        # Step 2: Extract pure JSON block
        json_start = raw_output.find('{')
        json_end = raw_output.rfind('}') + 1
        generated_json = json.loads(raw_output[json_start:json_end])

        # Step 3: Update dynamic fields
        ctx = generated_json.get("context", {})
        ctx["version"] = "1.1.0"
        ctx["ttl"] = "PT10M"
        ctx["timestamp"] = datetime.utcnow().isoformat() + "Z"
        ctx["message_id"] = str(uuid.uuid4())
        ctx["transaction_id"] = ctx.get("transaction_id", str(uuid.uuid4()))
        ctx["domain"] = "deg:retail"
        ctx["bap_id"] = "bap-network"
        ctx["bap_uri"] = "http://bap-network:5002"
        ctx["bpp_id"] = "bpp-network"
        ctx["bpp_uri"] = "http://bpp-network:6002"
        ctx["location"] = {
            "country": {"code": "IND"},
            "city": {"code": "std:080"}
        }

        # Remove any stray/invalid context keys
        for key in ["core_version", "country", "city"]:
            ctx.pop(key, None)

        # Step 4: Forward to BAP
        action = ctx.get("action", "search")
        bap_url = f"http://192.168.2.47:5001/{action}"
        bap_response = requests.post(bap_url, json=generated_json)

        return {
            "generated_json": generated_json,
            "bap_endpoint": bap_url,
            "bap_status_code": bap_response.status_code,
            "bap_response": (
                bap_response.json()
                if bap_response.headers.get("Content-Type", "").startswith("application/json")
                else bap_response.text
            )
        }

    except Exception as e:
        return {"error": str(e)}
