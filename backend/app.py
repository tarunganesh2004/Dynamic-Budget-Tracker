from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlite3
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from models import init_db
from predict import predict_spending

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Pydantic model for transaction input
class Transaction(BaseModel):
    amount: float
    category: str
    date: str  # Format: YYYY-MM-DD

# Pydantic model for prediction response
class Prediction(BaseModel):
    predicted_amount: float

# Add a transaction
@app.post("/transactions/", response_model=Transaction)
async def add_transaction(transaction: Transaction):
    try:
        conn = sqlite3.connect("budget.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO transactions (user_id, amount, category, date) VALUES (?, ?, ?, ?)",
            (1, transaction.amount, transaction.category, transaction.date)
        )
        conn.commit()
        conn.close()
        return transaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get all transactions
@app.get("/transactions/", response_model=List[Transaction])
async def get_transactions():
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    c.execute("SELECT amount, category, date FROM transactions WHERE user_id = ?", (1,))
    rows = c.fetchall()
    conn.close()
    return [{"amount": row[0], "category": row[1], "date": row[2]} for row in rows]

# Predict next month's spending
@app.get("/predict/", response_model=Prediction)
async def get_prediction():
    try:
        predicted_amount = predict_spending()
        return {"predicted_amount": predicted_amount}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))