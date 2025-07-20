import requests

def send_to_user(nlp_response: str):
    try:
        requests.post("http://localhost:8501/receive", json={"message": nlp_response})
    except Exception as e:
        print(f"Failed to send to client agent: {e}")
