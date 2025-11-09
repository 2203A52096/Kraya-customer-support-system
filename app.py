import streamlit as st
import pickle
import json
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
    .badge {
        display: inline-block;
        padding: 0.3em 0.7em;
        font-size: 0.8em;
        font-weight: 700;
        line-height: 1;
        color: white;
        text-align: center;
        border-radius: 0.8rem;
    }
    .badge-food {background-color: #FF6F61;}
    .badge-electronics {background-color: #6BAED6;}
    .badge-fabric {background-color: #8BC34A;}
    .badge-healthy {background-color: #4CAF50;}
    .badge-unhealthy {background-color: #F44336;}
    .banner {
        background-color: #FFF4E6;
        border-left: 6px solid #FF6F61;
        padding: 12px;
        margin: 10px 0px;
        border-radius: 25px;
        font-size: 16px;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.05);
    }
    .result-box {
        background: #ffffffdd;
        border-radius: 25px;
        padding: 15px 20px;
        margin: 15px 0;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOAD MODELS ---------------- #
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


# ---------------- ELECTRONICS RESPONSE ---------------- #
def generate_mistral_like_response(user_query, electronics_data):
    responses = [
        "Try restarting your device and checking for system updates.",
        "Ensure the cables are properly connected and no components are damaged.",
        "Try resetting to factory settings or clearing the cache memory.",
        "Check power sources and use an alternate socket or adapter.",
        "Please provide your model name for more specific troubleshooting steps."
    ]
    match = [val for key, val in electronics_data.items() if key.lower() in user_query.lower()]
    return random.choice(match) if match else random.choice(responses)


# ---------------- FABRIC EXTRAS ---------------- #
def extra_fabric_recommendations(predicted_outfit):
    extras = {
        "Casual Wear": ("Cotton", "Silk"),
        "Formal Wear": ("Linen", "Wool"),
        "Party Wear": ("Satin", "Denim"),
        "Winter Wear": ("Wool", "Nylon"),
        "Summer Wear": ("Cotton", "Polyester"),
    }
    return extras.get(predicted_outfit, ("Cotton Blend", "Leather"))


# ---------------- MAIN APP ---------------- #
st.set_page_config(page_title="Lifestyle Helper App", layout="centered")
st.sidebar.title("🛍️ Lifestyle Helper")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"],
)

# ---------------- HOME PAGE ---------------- #
if page == "🏠 Home":
    st.title("🏠 Welcome to Kraya")
    st.markdown('<div class="banner">✨ Smart Choices, Happy Living ✨</div>', unsafe_allow_html=True)
    st.markdown(
        """
        Kraya is your **personal customer support system** that makes shopping and usage easier:
        - <span class="badge badge-food">🍎 Food</span>: Check if food is **healthy**, for **weight loss/gain**.
        - <span class="badge badge-electronics">📱 Electronics</span>: Troubleshoot your **devices** quickly.
        - <span class="badge badge-fabric">🧵 Fabric</span>: Get fabric and **color suggestions** for your skin & season.

        💡 Our goal: Enhance **decision-making**, boost **convenience**, and improve **satisfaction**.
        """,
        unsafe_allow_html=True,
    )

# ---------------- FOOD PAGE ---------------- #
elif page == "🍎 Food":
    st.title("🍎 Food Health Analyzer")
    st.markdown('<div class="banner">🥗 Eat Smart, Live Better</div>', unsafe_allow_html=True)
    st.info("Enter food details and check if it’s suitable for **weight loss or weight gain**.")

    label = st.selectbox("🎯 Fitness Goal", ["Weight Loss", "Weight Gain"])
    ingredients = st.text_area("🧾 Ingredients (comma-separated)", "sugar, oats, milk, protein")
    calories = st.number_input("🔥 Calories per serving", min_value=0)
    protein = st.number_input("🍗 Protein (g)", min_value=0.0)
    carbs = st.number_input("🍞 Carbohydrates (g)", min_value=0.0)
    fiber = st.number_input("🌿 Fiber (g)", min_value=0.0)
    fat = st.number_input("🥓 Fat (g)", min_value=0.0)
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0)

    if st.button("🔍 Analyze Food"):
        model, vectorizer = load_food_model()
        text_features = vectorizer.transform([ingredients])
        prediction = model.predict(text_features)[0]

        if prediction.lower() == label.lower():
            st.markdown(
                f"""
                <div class="result-box">
                    <span class="badge badge-healthy">✅ Healthy</span>
                    The given food is suitable for <b>{label}</b>.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="result-box">
                    <span class="badge badge-unhealthy">❌ Not Suitable</span>
                    The given food is not suitable for <b>{label}</b>. Predicted goal: <b>{prediction}</b>.
                </div>
                """,
                unsafe_allow_html=True,
            )

# ---------------- ELECTRONICS PAGE ---------------- #
elif page == "📱 Electronics":
    st.title("📱 Electronics Help Desk")
    st.markdown('<div class="banner">⚡ Quick Fixes for Smarter Living ⚡</div>', unsafe_allow_html=True)
    st.info("Describe your problem and get intelligent troubleshooting tips.")

    devices = ["Smartphone 📱", "Laptop 💻", "TV 📺", "Washing Machine 🧺", "Refrigerator ❄️"]
    device = st.selectbox("🔧 Select your device", devices)
    query = st.text_area("✍️ Describe your issue")

    if st.button("🛠️ Get Support"):
        if not query.strip():
            st.warning("⚠️ Please describe your issue.")
        else:
            data = load_electronics_data()
            response = generate_mistral_like_response(query, data)
            st.markdown(
                f"""
                <div class="result-box">
                    <h4>🔧 Suggested Fix for {device}:</h4>
                    {response}
                </div>
                """,
                unsafe_allow_html=True,
            )

# ---------------- FABRIC PAGE ---------------- #
elif page == "🧵 Fabric":
    st.title("🧵 Fabric Recommendation System")
    st.markdown('<div class="banner">👗 Dress Smart, Feel Confident</div>', unsafe_allow_html=True)
    st.info("Get outfit and fabric suggestions based on your skin tone, weather, and work level.")

    skin_tone = st.selectbox("🎨 Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("☀️ Weather Condition", ["Sunny", "Rainy", "Cold", "Humid"])
    work_level = st.selectbox("💪 Work Level", ["Light", "Moderate", "Heavy"])
    season = st.selectbox("🍂 Season", ["Summer", "Winter", "Monsoon", "Spring"])

    if st.button("🎯 Recommend Outfit"):
        model, vectorizer = load_fabric_model()
        text_input = f"{skin_tone} {weather} {work_level} {season}"
        prediction = model.predict(vectorizer.transform([text_input]))[0]
        fabric, avoid = extra_fabric_recommendations(prediction)

        st.markdown(
            f"""
            <div class="result-box">
                <h4>👗 Recommended Outfit:</h4> {prediction}<br><br>
                <span style='color:#5CB85C; font-weight:bold;'>✅ Recommended Fabric:</span> {fabric}<br>
                <span style='color:#D9534F; font-weight:bold;'>❌ Avoid Fabrics:</span> {avoid}
            </div>
            """,
            unsafe_allow_html=True,
        )
