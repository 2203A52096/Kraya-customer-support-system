import streamlit as st
import pickle
import json
import random

# ===========================
# LOAD MODELS AND DATA
# ===========================
@st.cache_resource
def load_assets():
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


food_model, food_vectorizer, fabric_model, fabric_vectorizer, electronics_data = load_assets()

# ===========================
# MIMIC MISTRAL MODEL (OFFLINE)
# ===========================
def mimic_mistral_response(user_query: str, electronics_data: list):
    """
    Simulates an intelligent LLM-like response for electronics troubleshooting.
    """
    query = user_query.lower()
    best_match = None
    max_match_count = 0

    for item in electronics_data:
        matches = sum(q.lower() in query for q in item["example_queries"])
        if matches > max_match_count:
            best_match = item
            max_match_count = matches

        # Partial keyword matching
        if item["problem"].lower() in query or item["category"].lower() in query:
            best_match = item
            break

    if best_match:
        response = f"""
        **📱 Device:** {best_match['device']}  
        **⚙️ Category:** {best_match['category']}  
        **❗ Problem:** {best_match['problem']}  

        **💡 Suggested Solution:**  
        {best_match['solution']}
        """
    else:
        fallback = [
            "Try restarting your device and checking for software updates.",
            "Ensure all cables and connections are secure.",
            "Reset the device settings to default.",
            "If the issue persists, consider professional servicing."
        ]
        response = f"🤖 I couldn’t find an exact match, but here’s a suggestion:\n\n{random.choice(fallback)}"
    return response


# ===========================
# STREAMLIT UI (SAME AS ORIGINAL)
# ===========================

# --- Page setup ---
st.set_page_config(page_title="Kraya Customer Support", layout="centered")

# --- Sidebar Styling ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #F7E9E9;
        color: #5A3E36;
        border-radius: 20px;
    }
    [data-testid="stSidebar"] > div:first-child {
        font-size: 24px;
        font-weight: 700;
        color: #9A5F6F;
    }
    .badge {display:inline-block;padding:0.3em 0.7em;font-size:0.8em;font-weight:700;line-height:1;color:white;text-align:center;white-space:nowrap;border-radius:0.8rem;}
    .badge-food {background-color:#FF6F61;}
    .badge-electronics {background-color:#6BAED6;}
    .badge-fabric {background-color:#8BC34A;}
    .banner {background-color:#FFF4E6;border-left:6px solid #FF6F61;padding:12px;margin:10px 0;border-radius:25px;font-size:16px;box-shadow:2px 4px 10px rgba(0,0,0,0.05);}
    .result-box {background:#ffffffdd;border-radius:25px;padding:15px 20px;margin:15px 0;box-shadow:0px 4px 15px rgba(0,0,0,0.08);}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar ---
st.sidebar.title("🛍️ Lifestyle Helper")
page = st.sidebar.radio("Navigate", ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"])

# ===========================
# HOME PAGE
# ===========================
if page == "🏠 Home":
    st.title("🏠 Welcome to Kraya")
    st.markdown('<div class="banner">✨ Smart Choices, Happy Living ✨</div>', unsafe_allow_html=True)
    st.markdown(
        """
        Kraya is your **personal customer support system** that makes shopping and usage easier:

        - <span class="badge badge-food">🍎 Food</span>: Analyze **food health** with ML models.  
        - <span class="badge badge-electronics">📱 Electronics</span>: Get **smart troubleshooting** help.  
        - <span class="badge badge-fabric">🧵 Fabric</span>: Get **personalized fabric suggestions**.

        💡 Our goal: Enhance **decision-making**, boost **convenience**, and improve **satisfaction**.
        """,
        unsafe_allow_html=True,
    )

# ===========================
# FOOD PAGE
# ===========================
elif page == "🍎 Food":
    st.title("🍎 Food Health Analyzer")
    st.markdown('<div class="banner">🥗 Eat Smart, Live Better</div>', unsafe_allow_html=True)
    st.info("Enter your food details and find out if it’s suitable for **weight loss, weight gain, or balanced nutrition.**")

    ingredients = st.text_area("🧾 Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    calories = st.number_input("🔥 Calories per serving", min_value=0)
    fat = st.number_input("🥓 Total Fat (g)", min_value=0.0)
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0)
    fiber = st.number_input("🌿 Dietary Fiber (g)", min_value=0.0)
    protein = st.number_input("🍗 Protein (g)", min_value=0.0)

    if st.button("🔍 Analyze Food"):
        features = f"{ingredients} calories:{calories} fat:{fat} sugar:{sugar} fiber:{fiber} protein:{protein}"
        vectorized = food_vectorizer.transform([features])
        prediction = food_model.predict(vectorized)[0]
        st.markdown(f"<div class='result-box'>🍎 **Prediction:** {prediction}</div>", unsafe_allow_html=True)

# ===========================
# ELECTRONICS PAGE
# ===========================
elif page == "📱 Electronics":
    st.title("📱 Electronics Help Desk")
    st.markdown('<div class="banner">⚡ Quick Fixes for Smarter Living ⚡</div>', unsafe_allow_html=True)
    st.info("Describe your problem, and Kraya will give **smart troubleshooting tips** for your electronic devices.")

    user_input = st.text_area("✍️ Describe your issue")

    if st.button("🛠️ Get Support"):
        if not user_input.strip():
            st.warning("⚠️ Please describe your issue before proceeding.")
        else:
            response = mimic_mistral_response(user_input, electronics_data)
            st.markdown(f"<div class='result-box'>{response}</div>", unsafe_allow_html=True)

# ===========================
# FABRIC PAGE
# ===========================
elif page == "🧵 Fabric":
    st.title("🧵 Fabric Recommendation System")
    st.markdown('<div class="banner">👗 Dress Smart, Feel Confident</div>', unsafe_allow_html=True)
    st.info("Get fabric and **color suggestions** tailored to your **skin, weather, work level, and season.**")

    user_input = st.text_area("🧵 Describe your fabric needs or preferences")

    if st.button("🎯 Get Fabric Suggestions"):
        vectorized = fabric_vectorizer.transform([user_input])
        prediction = fabric_model.predict(vectorized)[0]
        st.markdown(f"<div class='result-box'>🧵 **Recommended Fabric/Style:** {prediction}</div>", unsafe_allow_html=True)
