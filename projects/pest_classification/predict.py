import json
import os
from tensorflow.keras.preprocessing import image
import numpy as np
import onnxruntime as ort

# 🔁 ONNX MODEL LOAD (ONLY CHANGE)
session = ort.InferenceSession("model.onnx")
input_name = session.get_inputs()[0].name

with open("class_mapping.json", "r") as f:
    class_indices = json.load(f)

labels = {v:k for k,v in class_indices.items()}

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
        "result": f"{crop} -->{disease}",
        "confidence": prob,
        "details":{
        "type": base["type"],
        "confidenced": confidence,
        "treatment": base["treatment"],
        "extra_action": base["extra"],
        "note": note}
    }


def predict(data):
    img_path = data.get("image")

    if not img_path or not os.path.exists(img_path):
        return {'error': 'No image provided'}

    # 🔥 safe loading (prevents Render crashes from bad input types)
    img = image.load_img(img_path, target_size=(128,128))
    img_array = image.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array.astype(np.float32) / 255.0

    # 🔁 ONLY CHANGE HERE (TensorFlow → ONNX)
    outputs = session.run(None, {input_name: img_array})

    proba = outputs[0][0]

    class_id = int(np.argmax(proba))
    confidence = float(proba[class_id])

    return pest_decision(class_id, confidence)