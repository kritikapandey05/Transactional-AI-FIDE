import streamlit as st
import requests
import json

# Initialize Streamlit UI
st.title("Beckn Protocol Chatbot")
st.subheader("Ask me anything related to product search, order, or fulfillment")

# Define the chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Display the chat history
for message in st.session_state['messages']:
    if message["role"] == "user":
        st.markdown(f"**You**: {message['content']}")
    elif message["role"] == "bot":
        st.markdown(f"**Bot**: {message['content']}")

# Chat input form
user_input = st.text_input("Type your message:", key="user_input")

def send_message(user_input):
    # Add the user's message to the chat history
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    # Send user input to the MCP1 to generate the Beckn JSON
    try:
        response = requests.post(
            "http://localhost:8000/mcp/nlp-to-beckn",  # MCP1 API endpoint
            json={"user_input": user_input}
        )
        
        response.raise_for_status()  # Will raise HTTPError for bad responses (4xx or 5xx)
        
        if response.status_code == 200:
            data = response.json()
            if "beckn_request" in data:
                # Add the generated Beckn JSON to the chat history as a bot message
                st.session_state['messages'].append({"role": "bot", "content": "Processing Beckn JSON..."})
                
                # Send the generated Beckn JSON to MCP2 for conversion to NLP
                nlp_response = requests.post(
                    "http://localhost:8001/mcp/beckn-to-nlp",  # MCP2 API endpoint
                    json={"beckn_json": json.loads(data["beckn_request"])}
                )
                
                nlp_response.raise_for_status()  # Will raise HTTPError for bad responses (4xx or 5xx)
                
                if nlp_response.status_code == 200:
                    nlp_data = nlp_response.json()
                    if "natural_language_response" in nlp_data:
                        # Add the NLP response from MCP2 to the chat history
                        st.session_state['messages'].append({"role": "bot", "content": nlp_data["natural_language_response"]})
                    else:
                        st.error(f"Error: {nlp_data.get('error', 'Unknown error')}")
                else:
                    st.error(f"Error from MCP2: Received {nlp_response.status_code}")
            else:
                st.error(f"Error from MCP1: Received {response.status_code}")
        else:
            st.error(f"Error from MCP1: Received {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {str(e)}")

# Send the message if button is clicked
if st.button("Send"):
    if user_input.strip():
        send_message(user_input)
    else:
        st.warning("Please enter a message to send.")
