# E-Banking Agent with MCP

An interactive banking assistant powered by Mistral AI and the Model Context Protocol (MCP). This project demonstrates how to build an AI agent that can interact with banking APIs through natural language.

> **⚠️ Platform Requirements:** This project is designed to run on **Linux** or **WSL (Windows Subsystem for Linux)**. Windows native environments are not supported.

## Features

- 🏦 Mock Banking API with customer accounts, transactions, and documents
- 🤖 AI-powered chat interface using Mistral AI
- 🔧 MCP (Model Context Protocol) server for tool orchestration
- 🔒 Account-level authentication and authorization
- 💬 Interactive command-line chat interface

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Mistral API key

## Setup

### 1. Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and navigate to the project

```bash
cd /path/to/ebanking-agent
```

### 3. Install dependencies using uv

```bash
# Create a virtual environment and install all dependencies
uv sync
```

This will:
- Create a virtual environment in `.venv`
- Install all dependencies from `pyproject.toml` including:
  - FastAPI for the banking API
  - FastMCP for the MCP server
  - Mistral AI SDK for the AI agent

### 4. Configure environment variables

Create a `.env` file in the project root with your Mistral API key:

```bash
echo "MISTRAL_API_KEY=your_mistral_api_key_here" > .env
```

You can obtain a Mistral API key from [https://console.mistral.ai/](https://console.mistral.ai/)

## Usage

The project consists of three main components that need to be running simultaneously. You'll need three terminal windows.

### Terminal 1: Start the Banking API

The Banking API provides the backend data and operations for accounts, transactions, and documents.

```bash
# Activate the virtual environment
source .venv/bin/activate

# Start the banking API server
uv run banking_api.py
```

The API will start on `http://localhost:8000`
- API documentation available at: `http://localhost:8000/docs`

### Terminal 2: Start the MCP Server

The MCP server acts as a bridge between the AI agent and the Banking API, exposing banking operations as tools.

```bash
# Activate the virtual environment
source .venv/bin/activate

# Start the MCP server
uv run server.py
```

The MCP server will start on `http://localhost:8010`

### Terminal 3: Start the Chat Client

The chat client provides an interactive interface to communicate with the AI banking agent.

```bash
# Activate the virtual environment
source .venv/bin/activate

# Start the interactive chat client
uv run client.py
```

## Interacting with the Banking Agent

Once all three components are running, you can interact with the banking agent through the chat interface:

```
Welcome to the Interactive MCP Chat!
============================================================
Type your questions and press Enter.
Type 'exit', 'quit', or 'q' to end the session.
============================================================

You: 
```

### Example Queries

Try these example queries to interact with the banking system:

- `"Show me all my accounts"`
- `"What's the balance of my checking account?"`
- `"List recent transactions for account ACC001"`
- `"Lock my account ACC001"`
- `"Search for documents about my account statement"`
- `"What's my user profile information?"`

### Notes

- The system uses mock data with pre-configured customers (CUST001, CUST002, CUST003)
- By default, the session will authenticate as a specific user (configured in `server.py`)
- To modify authentication, you can update the `set_user_context()` function in `server.py`
- Type `exit`, `quit`, or `q` to end the chat session

## Project Structure

```
ebanking-agent/
├── banking_api.py          # FastAPI-based mock banking backend
├── server.py               # MCP server with banking tools
├── client.py               # Interactive chat client
├── prompts/
│   └── agent-system-prompt.yaml  # System prompt for the AI agent
├── pyproject.toml          # Project dependencies
├── uv.lock                 # Dependency lock file
└── README.md               # This file
```

## Available MCP Tools

The MCP server exposes the following banking tools:

- `list_accounts()` - List all accounts for the authenticated user
- `get_account_balance(account_id)` - Get balance for a specific account
- `list_transactions(account_id)` - List transactions for an account
- `lock_account(account_id)` - Lock an account
- `search_documents(query)` - Search for customer documents
- `get_user_profile()` - Get the authenticated user's profile

## Development

### Adding New Tools

To add new banking operations:

1. Add the endpoint to `banking_api.py`
2. Create a corresponding MCP tool in `server.py` using the `@mcp.tool()` decorator
3. Ensure proper authentication and authorization checks

### Modifying the AI Behavior

Edit `prompts/agent-system-prompt.yaml` to customize the AI agent's personality and behavior.
