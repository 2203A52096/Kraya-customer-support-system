import streamlit as st
import pickle
import json
import random

# ---------------- PAGE CONFIGURATION ---------------- #
st.set_page_config(page_title="Kraya - Smart Lifestyle Helper", layout="centered")

# ---------------- STYLING ---------------- #
st.markdown(
    """
    <style>
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F7E9E9; /* pastel pink */
        color: #5A3E36;
        border-radius: 20px;
    }
    [data-testid="stSidebar"] > div:first-child {
        font-size: 24px;
        font-weight: 700;
        color: #9A5F6F;
    }

    /* Banners & Result Boxes */
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

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.3em 0.7em;
        font-size: 0.8em;
        font-weight: 700;
        line-height: 1;
        color: white;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.8rem;
    }
    .badge-food {background-color: #FF6F61;}
    .badge-electronics {background-color: #6BAED6;}
    .badge-fabric {background-color: #8BC34A;}
    .badge-healthy {background-color: #4CAF50;}
    .badge-unhealthy {background-color: #F44336;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOAD MODELS ---------------- #
@st.cache_resource
def load_models():
    with open("food/food_weight_model_final.pkl", "rb") as f:
        food_model = pickle.load(f)
    with open("food/tfidf_vectorizer_final.pkl", "rb") as f:
        food_vectorizer = pickle.load(f)

    with open("fabric/fashion_fabric_model.pkl", "rb") as f:
        fabric_model = pickle.load(f)
    with open("fabric/fashion_vectorizer_best(1).pkl", "rb") as f:
        fabric_vectorizer = pickle.load(f)

    with open("electronics/electronics.json", "r") as f:
        electronics_data = json.load(f)

    return food_model, food_vectorizer, fabric_model, fabric_vectorizer, electronics_data


food_model, food_vectorizer, fabric_model, fabric_vectorizer, electronics_data = load_models()

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🛍️ Lifestyle Helper")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"],
    index=1
)

# ---------------- HOME PAGE ---------------- #
if page == "🏠 Home":
    st.title("🏠 Welcome to Kraya")
    st.markdown('<div class="banner">✨ Smart Choices, Happy Living ✨</div>', unsafe_allow_html=True)
    st.markdown(
        """
        Kraya is your **personal lifestyle assistant** that helps in smart daily decisions:
        - <span class="badge badge-food">🍎 Food</span>: Check if food is **healthy**, for **weight loss/gain**.
        - <span class="badge badge-electronics">📱 Electronics</span>: Troubleshoot your **devices** quickly.
        - <span class="badge badge-fabric">🧵 Fabric</span>: Get fabric & **color suggestions** for your style & comfort.
        """,
        unsafe_allow_html=True,
    )

# ---------------- FOOD PAGE ---------------- #
elif page == "🍎 Food":
    st.title("🍎 Food Health Analyzer")
    st.markdown('<div class="banner">🥗 Eat Smart, Live Better</div>', unsafe_allow_html=True)

    ingredients = st.text_area("🧾 Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    label = st.selectbox("🎯 Health Goal", ["Weight Loss", "Weight Gain"])
    calories = st.number_input("🔥 Calories", min_value=0)
    protein = st.number_input("🍗 Protein (g)", min_value=0.0)
    carbs = st.number_input("🍞 Carbs (g)", min_value=0.0)
    fiber = st.number_input("🌿 Fiber (g)", min_value=0.0)
    fat = st.number_input("🥓 Fat (g)", min_value=0.0)
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0)

    def predict_food(ingredients, label):
        text = f"{ingredients} {label}"
        vectorized = food_vectorizer.transform([text])
        predicted_label = food_model.predict(vectorized)[0]
        if predicted_label.lower() == label.lower():
            if label.lower() == "weight loss":
                return '<div class="result-box"><span class="badge badge-healthy">✅ Suitable</span> for <b>Weight Loss</b>.</div>'
            else:
                return '<div class="result-box"><span class="badge badge-healthy">✅ Suitable</span> for <b>Weight Gain</b>.</div>'
        else:
            return '<div class="result-box"><span class="badge badge-unhealthy">⚠️ Not Suitable</span> for your selected goal.</div>'

    if st.button("🔍 Analyze Food"):
        if not ingredients.strip():
            st.warning("Please enter ingredients first!")
        else:
            result = predict_food(ingredients, label)
            st.markdown(result, unsafe_allow_html=True)

# ---------------- ELECTRONICS PAGE ---------------- #
elif page == "📱 Electronics":
    st.title("📱 Electronics Help Desk")
    st.markdown('<div class="banner">⚡ Quick Fixes for Smarter Living ⚡</div>', unsafe_allow_html=True)

    query = st.text_area("💬 Describe your issue:")
    st.caption("Example: 'My phone is not charging' or 'Laptop running slow'")

    def mistral_like_response(user_query):
        q = user_query.lower()
        for item in electronics_data:
            for ex in item["example_queries"]:
                if any(word in q for word in ex.lower().split()):
                    return f"""
                    <div class="result-box">
                    <b>Device:</b> {item['device']}<br>
                    <b>Issue:</b> {item['problem']}<br><br>
                    💡 <b>Suggested Fix:</b> {item['solution']}
                    </div>
                    """
        return f"""
        <div class="result-box">
        ⚙️ Try restarting or resetting your device. If issue persists, check for updates or contact support.
        </div>
        """

    if st.button("🛠️ Get Support"):
        if not query.strip():
            st.warning("Please describe your issue first.")
        else:
            st.markdown(mistral_like_response(query), unsafe_allow_html=True)

# ---------------- FABRIC PAGE ---------------- #
elif page == "🧵 Fabric":
    st.title("🧵 Fabric Recommendation System")
    st.markdown('<div class="banner">👗 Dress Smart, Feel Confident</div>', unsafe_allow_html=True)

    skin_tone = st.selectbox("🎨 Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("☀️ Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("💪 Work Level", ["Low", "Medium", "High"])
    season = st.selectbox("🍂 Season", ["Summer", "Winter", "Rainy"])

    def predict_fabric(skin_tone, weather, work_level, season):
        text = f"{skin_tone} {weather} {work_level} {season}"
        vectorized = fabric_vectorizer.transform([text])
        outfit = fabric_model.predict(vectorized)[0]
        rec_fabric = random.choice(["Cotton", "Linen", "Silk", "Denim"])
        avoid_fabric = random.choice(["Wool", "Polyester", "Nylon", "Velvet"])
        return outfit, rec_fabric, avoid_fabric

    if st.button("🎯 Get Suggestions"):
        outfit, rec, avoid = predict_fabric(skin_tone, weather, work_level, season)
        st.markdown(
            f"""
            <div class="result-box">
            👗 <b>Recommended Outfit:</b> {outfit}<br><br>
            🌿 <b>Recommended Fabric:</b> {rec}<br><br>
            🚫 <b>Avoid Fabrics:</b> {avoid}
            </div>
            """,
            unsafe_allow_html=True,
        )
