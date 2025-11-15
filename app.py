# app.py
import pickle
import json
import joblib
import streamlit as st
from interface import show_ui

st.set_page_config(
    page_title="Customer Support Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------------------
# Load Food Model + Vectorizer
# -----------------------------------------
try:
    with open("food/food_weight_model_final.pkl", "rb") as f:
        food_model = pickle.load(f)
    with open("food/tfidf_vectorizer_final.pkl", "rb") as f:
        food_vectorizer = pickle.load(f)
except Exception as e:
    st.warning(f"⚠️ Food model/vectorizer not loaded properly: {e}")
    food_model, food_vectorizer = None, None

# -----------------------------------------
# Load Fabric Model (JOBLIB — No vectorizer)
# -----------------------------------------
try:
    fabric_model = joblib.load("fabric/fabric_ml_pipeline.joblib")
except Exception as e:
    st.warning(f"⚠️ Fabric model not loaded properly: {e}")
    fabric_model = None

# -----------------------------------------
# Load Electronics JSON
# -----------------------------------------
try:
    with open("electronics/electronics.json", "r") as f:
        electronics_data = json.load(f)
except Exception as e:
    st.warning(f"⚠️ Electronics JSON not found: {e}")
    electronics_data = None

# -----------------------------------------
# Run UI
# -----------------------------------------
show_ui(food_model, food_vectorizer, fabric_model, electronics_data)
