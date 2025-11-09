import streamlit as st
import pickle
import json
from interface import show_ui  # import the interface

# ======== MODEL LOADING ========

# Load Food Model
try:
    food_model = pickle.load(open("food_weight_model_final.pkl", "rb"))
    food_vectorizer = pickle.load(open("tfidf_vectorizer_final.pkl", "rb"))
except Exception as e:
    st.warning("⚠️ Food model not loaded properly. Check file paths.")

# Load Fabric Model
try:
    fabric_model = pickle.load(open("fashion_fabric_model.pkl", "rb"))
    fabric_vectorizer = pickle.load(open("fashion_vectorizer_best(1).pkl", "rb"))
except Exception as e:
    st.warning("⚠️ Fabric model not loaded properly. Check file paths.")

# Load Electronics responses
try:
    with open("electronics_responses.json", "r") as f:
        electronics_data = json.load(f)
except Exception as e:
    electronics_data = {}
    st.warning("⚠️ Electronics JSON not found.")

# ======== FUNCTIONS ========

def predict_food(data):
    # data should be dict with input fields
    text = " ".join([str(v) for v in data.values()])
    x = food_vectorizer.transform([text])
    prediction = food_model.predict(x)[0]
    actual_label = data.get("label", "")
    
    if prediction == actual_label:
        if prediction.lower() == "weight loss":
            return "✅ This food product is suitable for weight loss!"
        elif prediction.lower() == "weight gain":
            return "✅ This food product is suitable for weight gain!"
    return f"⚠️ The given food product is predicted for {prediction} purposes."

def predict_fabric(inputs):
    text = " ".join([str(v) for v in inputs.values()])
    x = fabric_vectorizer.transform([text])
    recommendation = fabric_model.predict(x)[0]
    
    # simple extra info (mock)
    extra = {
        "Recommended Outfit": recommendation,
        "Recommended Fabric": "Cotton, Linen" if "summer" in text.lower() else "Wool, Silk",
        "Avoid Fabrics": "Polyester, Nylon" if "hot" in text.lower() else "None"
    }
    return extra

def get_electronic_response(query):
    # mimic mistral-like dynamic response using json knowledge
    for key, value in electronics_data.items():
        if key.lower() in query.lower():
            return value
    return "⚙️ Please provide more details about your electronic issue."


# ======== RUN UI ========
show_ui(predict_food, predict_fabric, get_electronic_response)
