#!/usr/bin/env python3
"""
Mock Banking API for MCP Demo

This module provides a mock banking API that simulates real banking operations.
In a production environment, this would connect to actual banking systems.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import random

app = FastAPI(title="Mock Banking API", description="Demo banking API for MCP integration")

# Mock data storage
customers = {
    "CUST001": {
        "id": "CUST001",
        "name": "John Smith",
        "email": "john.smith@email.com",
        "phone": "+1-555-0123",
        "address": "123 Main St, Anytown, USA",
        "date_of_birth": "1985-03-15",
        "ssn": "123-45-6789",
        "risk_profile": "moderate",
        "created_date": "2020-01-15"
    },
    "CUST002": {
        "id": "CUST002",
        "name": "Sarah Johnson",
        "email": "sarah.johnson@email.com",
        "phone": "+1-555-0456",
        "address": "456 Oak Ave, Somewhere, USA",
        "date_of_birth": "1990-07-22",
        "ssn": "987-65-4321",
        "risk_profile": "conservative",
        "created_date": "2018-06-10"
    },
    "CUST003": {
        "id": "CUST003",
        "name": "Michael Chen",
        "email": "michael.chen@email.com",
        "phone": "+1-555-0789",
        "address": "789 Pine Rd, Elsewhere, USA",
        "date_of_birth": "1988-11-08",
        "ssn": "456-78-9012",
        "risk_profile": "aggressive",
        "created_date": "2021-03-20"
    }
}

accounts = {
    "ACC001": {
        "id": "ACC001",
        "customer_id": "CUST001",
        "account_number": "1001-2345-6789-0123",
        "type": "checking",
        "balance": 5420.75,
        "currency": "USD",
        "status": "active",
        "created_date": "2020-01-15",
        "interest_rate": 0.01,
        "overdraft_limit": 1000.00,
        "status": "active"
    },
    "ACC002": {
        "id": "ACC002",
        "customer_id": "CUST001",
        "account_number": "2001-3456-7890-1234",
        "type": "savings",
        "balance": 15750.25,
        "currency": "USD",
        "status": "active",
        "created_date": "2020-01-15",
        "interest_rate": 0.025,
        "overdraft_limit": 0.00,
        "status": "active"
    },
    "ACC003": {
        "id": "ACC003",
        "customer_id": "CUST002",
        "account_number": "3001-4567-8901-2345",
        "type": "checking",
        "balance": 3200.50,
        "currency": "USD",
        "status": "active",
        "created_date": "2018-06-10",
        "interest_rate": 0.01,
        "overdraft_limit": 500.00,
        "status": "active"
    },
    "ACC004": {
        "id": "ACC004",
        "customer_id": "CUST002",
        "account_number": "4001-5678-9012-3456",
        "type": "investment",
        "balance": 45000.00,
        "currency": "USD",
        "status": "active",
        "created_date": "2019-01-15",
        "interest_rate": 0.0,
        "overdraft_limit": 0.00,
        "status": "active"
    },
    "ACC005": {
        "id": "ACC005",
        "customer_id": "CUST003",
        "account_number": "5001-6789-0123-4567",
        "type": "checking",
        "balance": 8750.00,
        "currency": "USD",
        "status": "active",
        "created_date": "2021-03-20",
        "interest_rate": 0.01,
        "overdraft_limit": 2000.00,
        "status": "active"
    }
}

transactions = {
    "TXN001": {
        "id": "TXN001",
        "account_id": "ACC001",
        "type": "deposit",
        "amount": 1000.00,
        "description": "Salary deposit",
        "date": "2024-01-15T09:00:00Z",
        "status": "completed",
        "reference": "SAL-2024-01"
    },
    "TXN002": {
        "id": "TXN002",
        "account_id": "ACC001",
        "type": "withdrawal",
        "amount": -250.00,
        "description": "ATM withdrawal",
        "date": "2024-01-16T14:30:00Z",
        "status": "completed",
        "reference": "ATM-001"
    },
    "TXN003": {
        "id": "TXN003",
        "account_id": "ACC001",
        "type": "transfer",
        "amount": -500.00,
        "description": "Transfer to savings",
        "date": "2024-01-17T10:15:00Z",
        "status": "completed",
        "reference": "TRF-001"
    },
    "TXN004": {
        "id": "TXN004",
        "account_id": "ACC002",
        "type": "transfer",
        "amount": 500.00,
        "description": "Transfer from checking",
        "date": "2024-01-17T10:15:00Z",
        "status": "completed",
        "reference": "TRF-001"
    }
}

documents = {
    "DOC001": {
        "id": "DOC001",
        "customer_id": "CUST001",
        "type": "statement",
        "content": "Customer statement for account ACC001. Account balance per 31st October 2024 is $5420.75.",
        "date": "2024-01-15T09:00:00Z",
    },
    "DOC002": {
        "id": "DOC002",
        "customer_id": "CUST001",
        "type": "statement",
        "content": "Customer statement for account ACC001. Account balance per 31st October 2024 is $5420.75.",
        "date": "2024-01-15T09:00:00Z",
    },
    "DOC003": {
        "id": "DOC003",
        "customer_id": "CUST002",
        "type": "statement",
        "content": "Customer statement for account ACC001. Account balance per 31st October 2024 is $15750.25.",
        "date": "2024-01-15T09:00:00Z",
    },
    "DOC004": {
        "id": "DOC004",
        "customer_id": "CUST002",
        "type": "statement",
        "content": "Customer statement for account ACC002. Account balance per 31st October 2024 is $15750.25.",
        "date": "2024-01-15T09:00:00Z",
    }
}

# Pydantic models
class Customer(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    address: str
    date_of_birth: str
    ssn: str
    risk_profile: str
    created_date: str

class Account(BaseModel):
    id: str
    customer_id: str
    account_number: str
    type: str
    balance: float
    currency: str
    status: str
    created_date: str
    interest_rate: float
    overdraft_limit: float

class Transaction(BaseModel):
    id: str
    account_id: str
    type: str
    amount: float
    description: str
    date: str
    status: str
    reference: str

class CreateAccountRequest(BaseModel):
    customer_id: str
    account_type: str
    initial_deposit: float = 0.0

class Document(BaseModel):
    id: str
    customer_id: str
    type: str
    content: str
    date: str


# API Endpoints
@app.get("/")
async def root():
    return {"message": "Mock Banking API", "version": "1.0.0"}

@app.get("/customers", response_model=List[Customer])
async def get_customers():
    """Get all customers"""
    return list(customers.values())

@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str):
    """Get customer by ID"""
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customers[customer_id]

@app.get("/customers/{customer_id}/accounts", response_model=List[Account])
async def get_customer_accounts(customer_id: str):
    """Get all accounts for a customer"""
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer_accounts = [acc for acc in accounts.values() if acc["customer_id"] == customer_id]
    return customer_accounts

@app.get("/accounts", response_model=List[Account])
async def get_accounts():
    """Get all accounts"""
    return list(accounts.values())

@app.get("/accounts/{account_id}", response_model=Account)
async def get_account(account_id: str):
    """Get account by ID"""
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_id]

@app.get("/accounts/{account_id}/transactions", response_model=List[Transaction])
async def get_account_transactions(account_id: str):
    """Get transaction history for an account"""
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account_transactions = [txn for txn in transactions.values() if txn["account_id"] == account_id]
    return account_transactions

@app.get("/customers/{customer_id}/documents", response_model=List[Document])
async def get_customer_documents(customer_id: str):
    """Get all documents for a customer"""
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer_documents = [doc for doc in documents.values() if doc["customer_id"] == customer_id]
    return customer_documents

@app.get("/accounts/{account_id}/lock", response_model=Account)
async def lock_account(account_id: str):
    """Lock an account"""
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    accounts[account_id]["status"] = "locked"
    return accounts[account_id]

@app.post("/accounts", response_model=Account)
async def create_account(request: CreateAccountRequest):
    """Create a new account"""
    if request.customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Validate account type
    valid_types = ["checking", "savings", "investment"]
    if request.account_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid account type. Must be one of: {valid_types}")
    
    # Generate new account
    account_id = f"ACC{str(len(accounts) + 1).zfill(3)}"
    account_number = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    # Set default values based on account type
    interest_rate = 0.025 if request.account_type == "savings" else 0.01
    overdraft_limit = 1000.00 if request.account_type == "checking" else 0.00
    
    new_account = {
        "id": account_id,
        "customer_id": request.customer_id,
        "account_number": account_number,
        "type": request.account_type,
        "balance": request.initial_deposit,
        "currency": "USD",
        "status": "active",
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "interest_rate": interest_rate,
        "overdraft_limit": overdraft_limit
    }
    
    accounts[account_id] = new_account
    
    # Create initial transaction if there's a deposit
    if request.initial_deposit > 0:
        txn_id = f"TXN{str(len(transactions) + 1).zfill(3)}"
        transactions[txn_id] = {
            "id": txn_id,
            "account_id": account_id,
            "type": "deposit",
            "amount": request.initial_deposit,
            "description": f"Initial deposit for {request.account_type} account",
            "date": datetime.now().isoformat() + "Z",
            "status": "completed",
            "reference": f"INIT-{account_id}"
        }
    
    return new_account

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    print("Starting Mock Banking API...")
    print("API will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
