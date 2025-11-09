import streamlit as st
import pickle
import json
import random

# ===============================
# 📦 Load Models & Vectorizers
# ===============================
@st.cache_resource
def load_models():
    # --- Food ---
    with open("food/food_weight_model_final.pkl", "rb") as f:
        food_model = pickle.load(f)
    with open("food/tfidf_vectorizer_final.pkl", "rb") as f:
        food_vectorizer = pickle.load(f)

    # --- Fabric ---
    with open("fabric/fashion_fabric_model.pkl", "rb") as f:
        fabric_model = pickle.load(f)
    with open("fabric/fashion_vectorizer_best(1).pkl", "rb") as f:
        fabric_vectorizer = pickle.load(f)

    # --- Electronics ---
    with open("electronics/electronics.json", "r") as f:
        electronics_data = json.load(f)

    return food_model, food_vectorizer, fabric_model, fabric_vectorizer, electronics_data


food_model, food_vectorizer, fabric_model, fabric_vectorizer, electronics_data = load_models()

# ===============================
# ⚡ Mistral-Mimic Function
# ===============================
def mimic_mistral(query, electronics_data):
    """
    Mimics how a Mistral model might respond to an electronics-related query.
    Uses keywords from electronics.json and generates natural responses.
    """
    query_lower = query.lower()
    best_match = None

    for key, response in electronics_data.items():
        if key.lower() in query_lower:
            best_match = response
            break

    generic_responses = [
        "Please try restarting your device and checking if any updates are available.",
        "Ensure your cables and connections are secure, and try a different power outlet.",
        "You might want to check for software or driver updates related to your device.",
        "Reset your device settings and see if the issue persists.",
        "If this continues, consider contacting the service center for further assistance."
    ]

    if best_match:
        reply = f"🔍 Based on your issue, here’s what might help:\n\n{best_match}"
    else:
        reply = f"🤖 Here's a general troubleshooting tip:\n\n{random.choice(generic_responses)}"

    # Add an LLM-like tone
    return (
        f"{reply}\n\n"
        "If the problem still exists, please let me know the exact model or error message — "
        "I’ll try to guide you more precisely."
    )

# ===============================
# 🎨 Streamlit UI
# ===============================
st.set_page_config(page_title="Customer Support Assistant", page_icon="🤖", layout="centered")

st.markdown("<h1 style='text-align: center;'>🤖 Smart Customer Support Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Instant intelligent responses for Food, Fabric, and Electronics queries.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Input section ---
st.subheader("🗣️ Describe your issue")
user_query = st.text_area("Enter your query here:", height=120, placeholder="e.g., My food packet seems expired or My washing machine is not starting...")

st.subheader("📦 Select Product Category")
category = st.selectbox("Choose a category:", ["Food", "Fabric", "Electronics"])

# --- Submit button ---
if st.button("Get Support Response"):
    if not user_query.strip():
        st.warning("⚠️ Please enter your issue or query before submitting.")
    else:
        st.markdown("---")
        st.subheader("💬 Response")

        # --- Food category ---
        if category == "Food":
            X = food_vectorizer.transform([user_query])
            prediction = food_model.predict(X)[0]
            st.success(f"🍎 **Food Response:** {prediction}")

        # --- Fabric category ---
        elif category == "Fabric":
            X = fabric_vectorizer.transform([user_query])
            prediction = fabric_model.predict(X)[0]
            st.success(f"🧵 **Fabric Response:** {prediction}")

        # --- Electronics category ---
        elif category == "Electronics":
            response = mimic_mistral(user_query, electronics_data)
            st.info(f"💡 **Electronics Response:**\n\n{response}")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit — Offline, No API Keys Needed.")
