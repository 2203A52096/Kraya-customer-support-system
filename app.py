# app.py
import pickle
import json
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
    food_model = pickle.load(open("food/food_weight_model_final.pkl", "rb"))
    food_vectorizer = pickle.load(open("food/tfidf_vectorizer_final.pkl", "rb"))
except:
    st.warning("⚠️ Food model or vectorizer not loaded properly.")
    food_model, food_vectorizer = None, None

# -----------------------------------------
# Load Fabric Model
# -----------------------------------------
try:
    fabric_model = pickle.load(open("fabric/fashion_fabric_model.pkl", "rb"))
except:
    st.warning("⚠️ Fabric model not loaded properly.")
    fabric_model = None

# -----------------------------------------
# Load Electronics JSON
# -----------------------------------------
try:
    with open("electronics/electronics.json", "r") as f:
        electronics_data = json.load(f)
except:
    st.warning("⚠️ Electronics JSON not found.")
    electronics_data = None

# -----------------------------------------
# Run UI 
# -----------------------------------------
show_ui(food_model, food_vectorizer, fabric_model, electronics_data)
