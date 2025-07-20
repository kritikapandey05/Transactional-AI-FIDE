import requests

MCP_ENDPOINT = "http://127.0.0.1:8000/mcp/nlp-to-beckn"  # Adjust if hosted elsewhere

def send_user_input_to_mcp(user_input: str) -> dict:
    """
    Send the user input (natural language) to the MCP Server and get the Beckn-compliant JSON.
    """
    try:
        response = requests.post(MCP_ENDPOINT, json={"user_input": user_input})
        response.raise_for_status()
        return response.json()  # Should return {"beckn_request": {...}} or {"error": "..."}
    except requests.RequestException as e:
        return {"error": str(e)}
