import pickle
import json
from sklearn.pipeline import Pipeline
import pandas as pd
with open("pipeline.pkl","rb") as f:
    model= pickle.load(f)



def irrigation_decision(prob:int,crop:str):
    crop_thresholds = {
    "Rice":     {"high": 0.6, "medium": 0.4},
    "Maize":    {"high": 0.7, "medium": 0.5},
    "Sugarcane":{"high": 0.65, "medium": 0.45},
    "Potato":   {"high": 0.6, "medium": 0.4},
    "Wheat":    {"high": 0.75, "medium": 0.55},
    "Cotton":   {"high": 0.8, "medium": 0.6}
    }
    thresholds = crop_thresholds[crop]

    if prob >= thresholds["high"]:
        return {
            "result": "Irrigation Needed --> HIGH",
            "confidence":prob,
            "details": {"crop":crop,
            "note":"Ensure sufficient water supply",
            "action": "Irrigate immediately"}      
        }

    elif prob >= thresholds["medium"]:
        return {
            "result": "Irrigation Needed --> MEDIUM",
            "confidence":prob,
            "details":{
                "crop":crop,
            "action": "Irrigate soon",
            "note": "Monitor soil closely"}
        }

    else:
        return {
            "result": "Irrigation Needed --> LOW",
            "confidence":prob,
            "details":{
                "crop":crop,
            "action": "No irrigation needed",
            "note": "Soil moisture is sufficient"}
        }
def predict(data):
    df=  pd.DataFrame([data])
    prob= model.predict_proba(df)[0][0]
    crop= data["Crop_Type"]
    #return {"result":f"{prob}"}
    return irrigation_decision(prob,crop)