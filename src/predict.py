import pandas as pd
import joblib

def make_predictions(df, model_path="models/stock_model.pkl"):
    saved = joblib.load(model_path)
    model = saved["model"]
    features = saved["features"]

    latest = df.sort_values(["Symbol", "Date"]).groupby("Symbol").tail(1).copy()
    latest = latest.dropna(subset=features)

    latest["PredictedNextClose"] = model.predict(latest[features])
    latest["PredictedMove"] = latest["PredictedNextClose"] - latest["Close"]
    latest["PredictedMovePct"] = (latest["PredictedMove"] / latest["Close"]) * 100

    return latest[["Date", "Symbol", "Close", "PredictedNextClose", "PredictedMove", "PredictedMovePct"]]
