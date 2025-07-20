# Transactional AI with MCP Servers and Beckn Protocol

This project involves building a multi-agent system (MCP) to convert NLP queries into Beckn protocol-compliant JSON, enabling seamless transactions in the retail domain. It is built using the FastAPI framework, OpenAI's GPT models for NLP to JSON conversion, and Streamlit for the frontend UI.

NOTE: Setting up beckn onix in a pre requisite for using this agent. 
      THe agent needs to be network configured with the right ip to ensure dockerized containers can connect it with non-dockerized ones.
_____________________________________________________________________

## Project Structure

The project is divided into the following main components:

1. **MCP Server 1 (NLP to Beckn JSON)**
   - Receives natural language queries from the user.
   - Converts the user input to a valid Beckn protocol-compliant JSON using OpenAI's API.

2. **MCP Server 2 (Beckn JSON to NLP)**
   - Receives a Beckn JSON response from the Beckn ONIX system.
   - Converts the JSON response into natural language for the user.

3. **Frontend (Streamlit UI)**
   - A user interface that allows the user to input their queries (e.g., "I want to buy a battery").
   - Displays the Beckn JSON generated in response.
   - Handles interactions between the user and the backend servers.
_____________________________________________________________________

## Requirements

The project requires the following Python packages:

- FastAPI: A modern web framework for building APIs with Python 3.6+ based on standard Python type hints.
- Uvicorn: ASGI server for running FastAPI applications.
- OpenAI: Python library to interface with OpenAI's models.
- Requests: A simple HTTP library for Python.
- Pydantic: Data validation library used by FastAPI for request body validation.
- Streamlit: A tool to create beautiful, interactive web apps.
- LangChain: A framework to build applications with large language models (optional, depending on use case).

You can install the required packages with:

bash
pip install -r requirements.txt
_____________________________________________________________________

Setup Instructions

Step 1: Clone the repository

Step 2: Set up a virtual environment

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate  # For Linux/MacOS
.\venv\Scripts\activate  # For Windows

Step 3: Install dependencies

pip install -r requirements.txt

Step 4: Set up environment variables

Create a .env file in the root directory with your OpenAI API key and any other necessary environment variables:

OPENAI_API_KEY=your_openai_api_key

Step 5: Run the servers
MCP Server 1 (NLP to Beckn JSON)

Start the FastAPI server for MCP Server 1:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

MCP Server 2 (Beckn JSON to NLP)

Start the FastAPI server for MCP Server 2:

uvicorn app.mcp2:app --reload --host 0.0.0.0 --port 8001

Streamlit Frontend

Run the Streamlit UI:

streamlit run app/frontend.py

This will open up the UI in your browser. You can now input NLP queries and see the corresponding responses from the MCP servers.
Step 6: Test the system

Once the servers are running:

    Open the Streamlit app in your browser (http://localhost:8501).

    Type in your queries (e.g., "I want to buy a battery") and see the generated Beckn JSON and its natural language response.

Troubleshooting

If you encounter any issues with the mcp servers, ensure that:

    All servers are running (check the logs for any errors).

    The network is correctly set up for Docker containers (if applicable).

    The OpenAI API key is correctly set in the .env file.
_____________________________________________________________________

Contributing

Feel free to contribute by opening issues or pull requests. Make sure to follow the repository's code of conduct and contribute guidelines.
_____________________________________________________________________

License

This project is licensed under the MIT License.
_____________________________________________________________________
