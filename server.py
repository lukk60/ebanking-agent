from fastmcp import FastMCP
from fastapi import FastAPI, HTTPException
from typing import List, Optional, Dict, Any
from banking_api import Account, Transaction, Document
import requests
import os
from functools import wraps

mcp = FastMCP(name="Banking MCP Server")

banking_api_url = "http://127.0.0.1:8000"

# User context management
class UserContext:
    def __init__(self, user_id: str, customer_id: str):
        self.user_id = user_id
        self.customer_id = customer_id

# Global user context (in production, this would come from authentication)
current_user = UserContext(user_id="CUST001", customer_id="CUST001")

def set_user_context(user_id: str, customer_id: str):
    """Set the current user context"""
    global current_user
    current_user = UserContext(user_id, customer_id)

def require_authentication(func):
    """Decorator to ensure user is authenticated"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user is None:
            raise HTTPException(status_code=401, detail="User not authenticated")
        return func(*args, **kwargs)
    return wrapper

def get_user_accounts() -> List[Account]:
    """Get accounts for the current authenticated user"""
    if current_user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    response = requests.get(f"{banking_api_url}/customers/{current_user.customer_id}/accounts")
    if response.status_code == 404:
        return []
    return response.json()

def validate_account_access(account_id: str) -> bool:
    """Validate that the current user has access to the specified account"""
    if current_user is None:
        return False
    
    user_accounts = get_user_accounts()
    return any(account["id"] == account_id for account in user_accounts)


@mcp.tool()
@require_authentication
def list_accounts() -> List[Account]:
    """List all accounts and balances for the authenticated user."""
    return get_user_accounts()

@mcp.tool()
@require_authentication
def lock_account(account_id: str) -> Optional[Account]:
    """Lock an account by account id. Only works for user's own accounts."""
    if not validate_account_access(account_id):
        raise HTTPException(status_code=403, detail="Access denied: You can only lock your own accounts")
    
    response = requests.get(f"{banking_api_url}/accounts/{account_id}/lock")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Account not found")
    return response.json()

@mcp.tool()
@require_authentication
def list_transactions(account_id: str) -> List[Transaction]:
    """List all transactions for an account. Only works for user's own accounts."""
    if not validate_account_access(account_id):
        raise HTTPException(status_code=403, detail="Access denied: You can only view transactions for your own accounts")
    
    response = requests.get(f"{banking_api_url}/accounts/{account_id}/transactions")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Account not found")
    return response.json()

@mcp.tool()
@require_authentication
def search_documents(query: str) -> List[Document]:
    """Search for documents belonging to the authenticated user."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    response = requests.get(f"{banking_api_url}/customers/{current_user.customer_id}/documents")
    if response.status_code == 404:
        return []
    
    documents = response.json()
    return [doc for doc in documents if query.lower() in doc["content"].lower()]

@mcp.tool()
@require_authentication
def get_user_profile() -> Dict[str, Any]:
    """Get the authenticated user's profile information."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    response = requests.get(f"{banking_api_url}/customers/{current_user.customer_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="User profile not found")
    return response.json()

@mcp.tool()
@require_authentication
def get_account_balance(account_id: str) -> Dict[str, Any]:
    """Get balance for a specific account. Only works for user's own accounts."""
    if not validate_account_access(account_id):
        raise HTTPException(status_code=403, detail="Access denied: You can only view balances for your own accounts")
    
    user_accounts = get_user_accounts()
    account = next((acc for acc in user_accounts if acc["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return {
        "account_id": account["id"],
        "account_number": account["account_number"],
        "balance": account["balance"],
        "currency": account["currency"],
        "type": account["type"]
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8010)