import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta


def predict_spending():
    conn = sqlite3.connect("budget.db")
    df = pd.read_sql_query(
        "SELECT amount, date FROM transactions WHERE user_id = 1", conn
    )
    conn.close()

    if len(df) < 2:
        return 0.0  # Not enough data for prediction

    # Convert date to numerical feature (days since earliest date)
    df["date"] = pd.to_datetime(df["date"])
    earliest_date = df["date"].min()
    df["days"] = (df["date"] - earliest_date).dt.days

    # Prepare data for linear regression
    X = df[["days"]].values
    y = df["amount"].values

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Predict for next 30 days
    next_date = (df["date"].max() + timedelta(days=30) - earliest_date).days
    predicted_amount = model.predict([[next_date]])[0]

    return round(predicted_amount, 2)
