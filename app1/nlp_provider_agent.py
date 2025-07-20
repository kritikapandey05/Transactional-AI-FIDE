import requests

def send_to_provider_agent(instructions: str):
    try:
        requests.post("http://localhost:8600/provider", json={"message": instructions})
    except Exception as e:
        print(f"Failed to send to provider agent: {e}")
