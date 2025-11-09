import streamlit as st
import pickle
import pandas as pd
import json
import requests

# ---------------- STYLING ---------------- #
st.markdown("""
<style>
[data-testid="stSidebar"] {background-color: #F7E9E9; color: #5A3E36; border-radius: 20px;}
[data-testid="stSidebar"] > div:first-child {font-size: 24px; font-weight: 700; color: #9A5F6F;}
.badge {display:inline-block; padding:0.3em 0.7em; font-size:0.8em; font-weight:700; border-radius:0.8rem; color:white;}
.badge-food {background-color:#FF6F61;} .badge-electronics{background-color:#6BAED6;} .badge-fabric{background-color:#8BC34A;}
.badge-healthy{background-color:#4CAF50;} .badge-unhealthy{background-color:#F44336;}
.banner {background-color:#FFF4E6; border-left:6px solid #FF6F61; padding:12px; margin:10px 0; border-radius:25px;}
.result-box {background:#ffffffdd; border-radius:25px; padding:15px 20px; margin:15px 0; box-shadow:0px 4px 15px rgba(0,0,0,0.08);}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODELS ---------------- #
@st.cache_resource
def load_food_model():
    return pickle.load(open("food/food_weight_model_final.pkl", "rb"))

@st.cache_resource
def load_fabric_model():
    return pickle.load(open("fabric/fashion_fabric_model.pkl", "rb"))

food_model = load_food_model()
fabric_model = load_fabric_model()

# ---------------- LOAD ELECTRONICS KNOWLEDGE BASE ---------------- #
with open("electronics/electronics.json", "r") as f:
    electronics_data = json.load(f)

# ---------------- MISTRAL API FUNCTION ---------------- #
API_URL = "https://api.together.xyz/inference"
API_KEY = st.secrets["TOGETHER_API_KEY"]  # store in Streamlit Cloud secrets

def get_mistral_response(prompt):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 250
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["output"][0]["text"]
    else:
        return "⚠️ API error: Unable to fetch Mistral response."

# ---------------- FOOD PREDICTION ---------------- #
def predict_food_health(ingredients, calories, fat, sugar, fiber, protein):
    try:
        # Prepare feature input for ML model
        df = pd.DataFrame([[calories, fat, sugar, fiber, protein]],
                          columns=["Calories", "Fat", "Sugar", "Fiber", "Protein"])
        pred = food_model.predict(df)[0]

        if pred == 0:
            label = "❌ Unhealthy"
            color = "badge-unhealthy"
            text = "High sugar or fat content. Not suitable for frequent consumption."
        elif pred == 1:
            label = "⚠️ Moderate"
            color = "badge-food"
            text = "Balanced nutritional value. Can be consumed occasionally."
        else:
            label = "✅ Healthy"
            color = "badge-healthy"
            text = "Good nutritional balance. Recommended for daily intake."
        return f"<div class='result-box'><span class='badge {color}'>{label}</span>: {text}</div>"

    except Exception as e:
        return f"<div class='result-box'>⚠️ Error analyzing food: {e}</div>"

# ---------------- FABRIC PREDICTION ---------------- #
def predict_fabric(skin_type, skin_tone, weather, work_level, season):
    try:
        df = pd.DataFrame([[skin_type, skin_tone, weather, work_level, season]],
                          columns=["SkinType", "SkinTone", "Weather", "WorkLevel", "Season"])
        pred = fabric_model.predict(df)[0]
        return f"""
        <div class='result-box'>
        <span class='badge badge-fabric'>🧵 Recommended Fabric</span>: <b>{pred}</b><br>
        💡 Tip: Choose this fabric for comfort and better skin compatibility.
        </div>
        """
    except Exception as e:
        return f"<div class='result-box'>⚠️ Error generating recommendation: {e}</div>"

# ---------------- ELECTRONICS TROUBLESHOOTING ---------------- #
def troubleshoot_electronic(device, user_query):
    # Step 1: Try to match from JSON
    for item in electronics_data:
        if item["device"].lower() in device.lower():
            for example in item["example_queries"]:
                if any(word in user_query.lower() for word in example.lower().split()):
                    return f"<div class='result-box'><b>🔧 Suggested Fix:</b> {item['solution']}</div>"

    # Step 2: Fallback → use Mistral model for reasoning
    prompt = f"User issue: {user_query}\nDevice: {device}\nBased on this, suggest troubleshooting steps."
    ai_reply = get_mistral_response(prompt)
    return f"<div class='result-box'><b>🤖 AI Suggestion:</b><br>{ai_reply}</div>"

# ---------------- MAIN APP ---------------- #
st.set_page_config(page_title="Kraya - AI Lifestyle Helper", layout="centered")
st.sidebar.title("🛍️ Lifestyle Helper")

page = st.sidebar.radio("Navigate", ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"])

# HOME PAGE
if page == "🏠 Home":
    st.title("🏠 Welcome to Kraya")
    st.markdown('<div class="banner">✨ Smart Choices, AI Powered ✨</div>', unsafe_allow_html=True)
    st.markdown("""
    Kraya is your **AI-based lifestyle assistant** that helps with:
    - <span class="badge badge-food">🍎 Food</span>: ML model predicts health level.  
    - <span class="badge badge-electronics">📱 Electronics</span>: Mistral AI suggests smart fixes.  
    - <span class="badge badge-fabric">🧵 Fabric</span>: ML model recommends best fabric.  
    """, unsafe_allow_html=True)

# FOOD PAGE
elif page == "🍎 Food":
    st.title("🍎 Food Health Analyzer (ML-based)")
    st.markdown('<div class="banner">🥗 Eat Smart, Live Better</div>', unsafe_allow_html=True)

    ingredients = st.text_area("🧾 Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    calories = st.number_input("🔥 Calories per serving", min_value=0)
    fat = st.number_input("🥓 Total Fat (g)", min_value=0.0)
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0)
    fiber = st.number_input("🌿 Dietary Fiber (g)", min_value=0.0)
    protein = st.number_input("🍗 Protein (g)", min_value=0.0)

    if st.button("🔍 Analyze Food"):
        st.markdown(predict_food_health(ingredients, calories, fat, sugar, fiber, protein), unsafe_allow_html=True)

# ELECTRONICS PAGE
elif page == "📱 Electronics":
    st.title("📱 Electronics Help Desk (Mistral Powered)")
    st.markdown('<div class="banner">⚡ AI Smart Fixes for Devices ⚡</div>', unsafe_allow_html=True)

    devices = ["Smartphone", "Laptop", "TV", "Washing Machine", "Refrigerator"]
    device = st.selectbox("🔧 Select your device", devices)
    user_input = st.text_area("✍️ Describe your issue")

    if st.button("🛠️ Get Support"):
        if user_input.strip() == "":
            st.warning("⚠️ Please describe your issue before proceeding.")
        else:
            with st.spinner("Analyzing your problem..."):
                st.markdown(troubleshoot_electronic(device, user_input), unsafe_allow_html=True)

# FABRIC PAGE
elif page == "🧵 Fabric":
    st.title("🧵 Fabric Recommendation System (ML-based)")
    st.markdown('<div class="banner">👗 Dress Smart, Feel Confident</div>', unsafe_allow_html=True)

    skin_type = st.selectbox("👩 Skin Type", ["Dry", "Oily", "Sensitive", "Normal"])
    skin_tone = st.selectbox("🎨 Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("☀️ Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("💪 Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("🍂 Season", ["Summer", "Winter", "Spring", "Autumn"])

    if st.button("🎯 Get Fabric Suggestions"):
        st.markdown(predict_fabric(skin_type, skin_tone, weather, work_level, season), unsafe_allow_html=True)
