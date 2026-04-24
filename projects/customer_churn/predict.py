import pickle
import pandas as pd
import os

# Get current folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load trained model
model_path = os.path.join(BASE_DIR, "churn_model.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)


def churn_decision(prob):
    """
    Categorize customer churn risk and provide suggestions.
    """
    percentage = round(prob * 100, 2)

    if percentage >= 70:
        return {
            "result": "High Risk Churner 🔴",
            "confidence": prob,
            "details":{
            "note": "Offer discounts, loyalty rewards, or immediate customer support intervention."}
        }

    elif percentage >= 40:
        return {
            "result": "Medium Risk Churner 🟡",
            "confidence": prob,
            "details":{
            "note": "Send personalized offers, survey feedback, or improve service engagement."}
        }

    else:
        return {
            "result": "Low Risk Churner 🟢",
            "confidence": prob,
            "details":{
            "note": "Maintain engagement with regular updates and loyalty programs."}
        }


def predict(data):
    """
    Takes user input and predicts churn risk level.
    """
    df = pd.DataFrame([data])

    # Probability of churn ("Yes")
    prob = model.predict_proba(df)[0][1]

    return churn_decision(prob)