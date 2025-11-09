import streamlit as st
import pickle
import json
from interface import load_interface, food_ui, electronics_ui, fabric_ui
import random

# ------------------ Load Models ------------------
@st.cache_resource
def load_food_model():
    with open("food/food_weight_model_final.pkl", "rb") as f:
        model = pickle.load(f)
    with open("food/tfidf_vectorizer_final.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer


@st.cache_resource
def load_fabric_model():
    with open("fabric/fashion_fabric_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("fabric/fashion_vectorizer_best(1).pkl", "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer


@st.cache_resource
def load_electronics_data():
    with open("electronics/electronics.json", "r") as f:
        data = json.load(f)
    return data


# ------------------ Electronics Response Generator ------------------
def generate_mistral_like_response(user_query, electronics_data):
    responses = [
        "Let’s troubleshoot this issue. Based on what you described, try checking the power source and connections.",
        "You might want to update the device firmware or reset the settings to default.",
        "If overheating occurs, clean the vents and ensure proper airflow.",
        "It could be a battery issue — try replacing or recalibrating it.",
        "Please provide more details about your model for a better recommendation."
    ]
    match = [val for key, val in electronics_data.items() if key.lower() in user_query.lower()]
    if match:
        return random.choice(match)
    return random.choice(responses)


# ------------------ Fabric Extra Recommendations ------------------
def extra_fabric_recommendations(predicted_outfit):
    extra = {
        "Casual Wear": ("Cotton", "Silk"),
        "Formal Wear": ("Linen", "Wool"),
        "Party Wear": ("Satin", "Denim"),
        "Winter Wear": ("Wool", "Nylon"),
        "Summer Wear": ("Cotton", "Polyester")
    }
    fabrics = extra.get(predicted_outfit, ("Cotton Blend", "Leather"))
    return fabrics


# ------------------ MAIN APP ------------------
st.set_page_config(page_title="Customer Support System", page_icon="🤖", layout="centered")

category = load_interface()

if category == "Food":
    inputs = food_ui()
    if inputs:
        model, vectorizer = load_food_model()
        text_features = vectorizer.transform([inputs["ingredients"]])
        prediction = model.predict(text_features)[0]

        st.subheader("Prediction Result")
        if prediction.lower() == inputs["label"].lower():
            st.success(f"The given food is suitable for **{inputs['label']}**.")
        else:
            st.error(f"The given food is not suitable for **{inputs['label']}**. Predicted goal: {prediction}")

elif category == "Electronics":
    query = electronics_ui()
    if query:
        data = load_electronics_data()
        response = generate_mistral_like_response(query, data)
        st.subheader("Assistant Response:")
        st.info(response)

elif category == "Fabric":
    inputs = fabric_ui()
    if inputs:
        model, vectorizer = load_fabric_model()
        text_input = f"{inputs['Skin Tone']} {inputs['Weather Condition']} {inputs['Work Level']} {inputs['Season']}"
        prediction = model.predict(vectorizer.transform([text_input]))[0]

        st.subheader("Recommended Outfit:")
        st.success(prediction)

        fabric, avoid = extra_fabric_recommendations(prediction)
        st.write(f"**Recommended Fabric:** {fabric}")
        st.write(f"**Avoid Fabrics:** {avoid}")
