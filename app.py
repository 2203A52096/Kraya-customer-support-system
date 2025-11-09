import streamlit as st
import pickle
import json
from ui_interface import show_interface


# =======================
# Load ML Models
# =======================
@st.cache_resource
def load_food_model():
    model = pickle.load(open("food/food_weight_model_final.pkl", "rb"))
    vectorizer = pickle.load(open("food/tfidf_vectorizer_final.pkl", "rb"))
    return model, vectorizer


@st.cache_resource
def load_fabric_model():
    model = pickle.load(open("fabric/fashion_fabric_model.pkl", "rb"))
    vectorizer = pickle.load(open("fabric/fashion_vectorizer_best(1).pkl", "rb"))
    return model, vectorizer


@st.cache_data
def load_electronics_data():
    with open("electronics/electronics.json", "r") as f:
        data = json.load(f)
    return data


# =======================
# Load all resources
# =======================
food_model, food_vectorizer = load_food_model()
fabric_model, fabric_vectorizer = load_fabric_model()
electronics_data = load_electronics_data()

# =======================
# Run Interface
# =======================
show_interface(
    food_model,
    food_vectorizer,
    fabric_model,
    fabric_vectorizer,
    electronics_data
)
