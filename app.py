import streamlit as st
import pickle
import json
import os
import random

# ---------------- STYLING ---------------- #
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
    .badge {padding: 0.3em 0.7em; font-size: 0.8em; font-weight: 700; color: white;
        border-radius: 0.8rem; display: inline-block;}
    .badge-food {background-color: #FF6F61;}
    .badge-electronics {background-color: #6BAED6;}
    .badge-fabric {background-color: #8BC34A;}
    .badge-healthy {background-color: #4CAF50;}
    .badge-unhealthy {background-color: #F44336;}
    .banner {background-color: #FFF4E6; border-left: 6px solid #FF6F61;
        padding: 12px; margin: 10px 0px; border-radius: 25px;
        font-size: 16px; box-shadow: 2px 4px 10px rgba(0,0,0,0.05);}
    .result-box {background: #ffffffdd; border-radius: 25px; padding: 15px 20px;
        margin: 15px 0; box-shadow: 0px 4px 15px rgba(0,0,0,0.08);}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOAD MODELS ---------------- #
try:
    food_model = pickle.load(open("food/food_weight_model_final.pkl", "rb"))
    food_vectorizer = pickle.load(open("food/tfidf_vectorizer_final.pkl", "rb"))
except Exception as e:
    food_model = None
    food_vectorizer = None
    st.warning("⚠️ Food model files not found. Please verify folder structure.")

try:
    fabric_model = pickle.load(open("fabric/fashion_fabric_model.pkl", "rb"))
    fabric_vectorizer = pickle.load(open("fabric/fashion_vectorizer_best(1).pkl", "rb"))
except Exception as e:
    fabric_model = None
    fabric_vectorizer = None
    st.warning("⚠️ Fabric model files not found. Please verify folder structure.")

try:
    with open("electronics/electronics.json", "r") as f:
        electronics_data = json.load(f)
except Exception as e:
    electronics_data = {}
    st.warning("⚠️ Electronics JSON not found.")

# ---------------- FUNCTIONS ---------------- #
def predict_food(ingredients, calories, protein, carbs, fiber, fat, sugar, label):
    if not food_model or not food_vectorizer:
        return "<div class='result-box'>⚠️ Model not loaded properly.</div>"

    text_input = f"{ingredients} {calories} {protein} {carbs} {fiber} {fat} {sugar}"
    vec = food_vectorizer.transform([text_input])
    pred_label = food_model.predict(vec)[0]

    if pred_label == label.lower():
        if label.lower() == "weight loss":
            return """<div class="result-box"><span class="badge badge-healthy">
            ✅ Suitable for Weight Loss</span>: Low-calorie and nutrient-friendly.</div>"""
        else:
            return """<div class="result-box"><span class="badge badge-healthy">
            ✅ Suitable for Weight Gain</span>: High-energy and protein-rich.</div>"""
    else:
        return """<div class="result-box"><span class="badge badge-unhealthy">
        ⚠️ Not suitable for selected goal.</span> Try a different food item.</div>"""


def predict_fabric(skin_tone, weather, work_level, season):
    if not fabric_model or not fabric_vectorizer:
        return "⚠️ Fabric model not loaded.", "", ""

    text = f"{skin_tone} {weather} {work_level} {season}"
    vectorized = fabric_vectorizer.transform([text])
    outfit = fabric_model.predict(vectorized)[0]

    rec_fabrics = random.choice([
        "Cotton, Linen", "Silk, Rayon", "Wool, Polyester blends",
        "Denim, Cotton mix"
    ])
    avoid_fabrics = random.choice([
        "Nylon, Polyester", "Wool, Heavy Silk",
        "Leather, Velvet", "Synthetic blends"
    ])

    return outfit, rec_fabrics, avoid_fabrics


def generate_electronics_response(device, issue):
    if not electronics_data:
        return "⚠️ No troubleshooting data found."

    issue_lower = issue.lower()
    # Try to match from JSON
    for key, value in electronics_data.items():
        if key.lower() in issue_lower:
            return f"💡 **Suggested Fix:** {value}"

    # Mistral-like fallback generation
    responses = [
        f"💡 Suggested Fix: Check the {device.lower()} connections and restart. If issue persists, consider service.",
        f"🔧 Try resetting your {device.lower()}, check cables, and ensure updates are installed.",
        f"⚙️ The issue might be hardware-related. Backup data and visit an authorized center.",
    ]
    return random.choice(responses)

# ---------------- MAIN APP ---------------- #
st.set_page_config(page_title="Lifestyle Helper App", layout="centered")
st.sidebar.title("🛍️ Lifestyle Helper")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"],
    index=0
)

# ---------------- HOME ---------------- #
if page == "🏠 Home":
    st.title("🏠 Welcome to Kraya")
    st.markdown('<div class="banner">✨ Smart Choices, Happy Living ✨</div>', unsafe_allow_html=True)
    st.markdown(
        """
        Kraya is your **personal customer support system** that makes shopping and usage easier:
        - <span class="badge badge-food">🍎 Food</span>: Check if food is **healthy**, for **weight loss/gain**.  
        - <span class="badge badge-electronics">📱 Electronics</span>: Troubleshoot your **devices** quickly.  
        - <span class="badge badge-fabric">🧵 Fabric</span>: Get **fabric and color suggestions** based on your style.  

        💡 Our goal: Enhance **decision-making**, boost **convenience**, and improve **satisfaction**.
        """,
        unsafe_allow_html=True,
    )

# ---------------- FOOD ---------------- #
elif page == "🍎 Food":
    st.title("🍎 Food Health Analyzer")
    st.markdown('<div class="banner">🥗 Eat Smart, Live Better</div>', unsafe_allow_html=True)

    ingredients = st.text_area("🧾 Ingredients (comma-separated)")
    label = st.selectbox("🎯 Target Goal", ["Weight Loss", "Weight Gain"])
    calories = st.number_input("🔥 Calories", min_value=0.0)
    protein = st.number_input("🍗 Protein (g)", min_value=0.0)
    carbs = st.number_input("🥖 Carbohydrates (g)", min_value=0.0)
    fiber = st.number_input("🌿 Fiber (g)", min_value=0.0)
    fat = st.number_input("🥓 Fat (g)", min_value=0.0)
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0)

    if st.button("🔍 Analyze Food"):
        result = predict_food(ingredients, calories, protein, carbs, fiber, fat, sugar, label)
        st.markdown(result, unsafe_allow_html=True)

# ---------------- ELECTRONICS ---------------- #
elif page == "📱 Electronics":
    st.title("📱 Electronics Help Desk")
    st.markdown('<div class="banner">⚡ Quick Fixes for Smarter Living ⚡</div>', unsafe_allow_html=True)

    devices = ["Smartphone", "Laptop", "TV", "Washing Machine", "Refrigerator"]
    device = st.selectbox("🔧 Select your device", devices)
    issue = st.text_area("✍️ Describe your issue")

    if st.button("🛠️ Get Support"):
        if issue.strip() == "":
            st.warning("⚠️ Please describe your issue before proceeding.")
        else:
            response = generate_electronics_response(device, issue)
            st.markdown(f"<div class='result-box'>{response}</div>", unsafe_allow_html=True)

# ---------------- FABRIC ---------------- #
elif page == "🧵 Fabric":
    st.title("🧵 Fabric Recommendation System")
    st.markdown('<div class="banner">👗 Dress Smart, Feel Confident</div>', unsafe_allow_html=True)

    skin_tone = st.selectbox("🎨 Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("☀️ Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("💪 Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("🍂 Season", ["Summer", "Winter", "Spring", "Autumn"])

    if st.button("🎯 Get Fabric Suggestions"):
        outfit, rec, avoid = predict_fabric(skin_tone, weather, work_level, season)
        st.markdown(
            f"""
            <div class='result-box'>
            <b>👗 Recommended Outfit:</b> {outfit}<br>
            <b>✅ Recommended Fabrics:</b> {rec}<br>
            <b>❌ Avoid Fabrics:</b> {avoid}
            </div>
            """,
            unsafe_allow_html=True,
        )
