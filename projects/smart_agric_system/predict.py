import pickle
import json
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
import threading
import os

from tensorflow.keras.preprocessing import image
import onnxruntime as ort

# =========================
# 🔁 IRRIGATION MODEL (UNCHANGED)
# =========================
with open("pipeline.pkl","rb") as f:
    model_Irr = pickle.load(f)

# =========================
# 🔁 PEST MODEL → ONNX ONLY CHANGE
# =========================
session = ort.InferenceSession("model.onnx")
input_name = session.get_inputs()[0].name

with open("class_mapping.json", "r") as f:
    class_indices = json.load(f)

labels = {v:k for k,v in class_indices.items()}

# =========================
# (ALL YOUR FUNCTIONS UNCHANGED)
# =========================
def extract_info(label):
    if "(" in label:
        disease = label.split("(")[0].strip()
        crop = label.split("(")[-1].replace(")", "").strip()
    else:
        disease = label
        crop = "Unknown"
    return disease, crop


def get_treatment(disease):
    d = disease.lower()

    if "blight" in d or "rot" in d or "spot" in d:
        return {
            "type": "Fungal",
            "treatment": "Apply fungicide (Mancozeb / Chlorothalonil)",
            "extra": "Remove infected leaves and improve airflow"
        }

    elif "bacterial" in d:
        return {
            "type": "Bacterial",
            "treatment": "Use copper-based bactericide",
            "extra": "Avoid overhead watering"
        }

    elif "virus" in d or "mosaic" in d:
        return {
            "type": "Viral",
            "treatment": "No chemical cure - remove infected plants",
            "extra": "Control insects like aphids"
        }

    elif "aphid" in d or "mite" in d or "weevil" in d or "midge" in d:
        return {
            "type": "Insect",
            "treatment": "Use insecticide (Neem oil / Imidacloprid)",
            "extra": "Monitor spread and isolate plants"
        }

    elif "healthy" in d:
        return {
            "type": "Healthy",
            "treatment": "No treatment needed",
            "extra": "Maintain good farming practices"
        }

    else:
        return {
            "type": "Unknown",
            "treatment": "Consult agricultural expert",
            "extra": "Monitor plant condition"
        }


def confidence_logic(prob):
    if prob >= 0.85:
        return "HIGH"
    elif prob >= 0.6:
        return "MEDIUM"
    else:
        return "LOW"


def pest_decision(class_id, prob):

    label = labels[class_id]
    disease, crop = extract_info(label)
    base = get_treatment(disease)
    confidence = confidence_logic(prob)

    if confidence == "LOW":
        note = "Low confidence - verify manually before applying treatment"
    elif confidence == "MEDIUM":
        note = "Moderate confidence - monitor before full treatment"
    else:
        note = "High confidence - take action"

    return {
        "result": crop,
        "disease": disease,
        "con": confidence,
        "confidence": prob,
        "type": base["type"],
        "confidenced": confidence,
        "treatment": base["treatment"],
        "extra_action": base["extra"],
        "note": note
    }


# =========================
# 💧 IRRIGATION (UNCHANGED)
# =========================
def irrigation_decision(prob:int,crop:str):

    crop_thresholds = {
        "Rice": {"high": 0.6, "medium": 0.4},
        "Maize": {"high": 0.7, "medium": 0.5},
        "Sugarcane":{"high": 0.65, "medium": 0.45},
        "Potato":{"high": 0.6, "medium": 0.4},
        "Wheat":{"high": 0.75, "medium": 0.55},
        "Cotton":{"high": 0.8, "medium": 0.6}
    }

    thresholds = crop_thresholds[crop]

    if prob >= thresholds["high"]:
        return {
            "result": "HIGH",
            "confidence": prob,
            "crop": crop,
            "note": "Ensure sufficient water supply",
            "action": "Irrigate immediately"
        }

    elif prob >= thresholds["medium"]:
        return {
            "result": "MEDIUM",
            "confidence": prob,
            "crop": crop,
            "action": "Irrigate soon",
            "note": "Monitor soil closely"
        }

    else:
        return {
            "result": "LOW",
            "confidence": prob,
            "crop": crop,
            "action": "No irrigation needed",
            "note": "Soil moisture is sufficient"
        }


# =========================
# ⚡ FINAL DECISION (UNCHANGED)
# =========================
def final_decision(pest_result, irrigation_result):

    disease = pest_result["disease"].lower()
    pest_conf = pest_result["con"]
    irrigation_action = irrigation_result["action"]

    final_action = []
    warnings = []

    if "healthy" in disease:
        final_action.append("Crop is healthy ✅")
    else:
        final_action.append(pest_result["treatment"])
        final_action.append(pest_result["extra_action"])

    if "fungal" in pest_result["type"].lower():
        if "irrigate immediately" in irrigation_action.lower():
            warnings.append("⚠️ Avoid overwatering — may worsen fungal disease")

    if "bacterial" in pest_result["type"].lower():
        warnings.append("⚠️ Avoid overhead irrigation")

    if pest_conf == "LOW":
        warnings.append("⚠️ Pest detection confidence is low — verify manually")

    return {
        "result": f"Pest Result --> {pest_result['disease']} -- Irrigation Result --> {irrigation_result['action']}",
        "details":{
            "confidence": f"Pest Confidence --> {pest_result['confidence']:.2f} -- Irrigation Confidence --> {irrigation_result['confidence']:.2f}",
            "crop": pest_result["result"],
            "actions": final_action,
        }
    }


# =========================
# 🚀 PREDICT (ONLY PEST PART CHANGED)
# =========================
def predict(data):

    data_image = data.pop("image")
    data_df = data

    df = pd.DataFrame([data_df])
    crop = data["Crop_Type"]
    img_path = data_image

    if not img_path or not os.path.exists(img_path):
        return {'error': 'No image provided'}

    irrigation_result_holder = {}
    pest_result_holder = {}

    def run_irrigation():
        prob = model_Irr.predict_proba(df)[0][0]
        irrigation_result_holder["result"] = irrigation_decision(prob, crop)

    def run_pest():

        img = image.load_img(img_path, target_size=(128,128))
        img_array = image.img_to_array(img)

        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array.astype(np.float32) / 255.0

        # 🔁 ONLY CHANGE: TensorFlow → ONNX
        outputs = session.run(None, {input_name: img_array})
        proba = outputs[0][0]

        class_id = int(np.argmax(proba))
        confidence = float(proba[class_id])

        pest_result_holder["result"] = pest_decision(class_id, confidence)

    t1 = threading.Thread(target=run_irrigation)
    t2 = threading.Thread(target=run_pest)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    return final_decision(
        pest_result=pest_result_holder["result"],
        irrigation_result=irrigation_result_holder["result"]
    )