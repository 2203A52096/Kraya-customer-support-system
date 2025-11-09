import streamlit as st
import pickle
import json
import random

# ===========================
# Load ML Models and Vectorizers
# ===========================
@st.cache_resource
def load_models():
    # Food
    with open("food/food_weight_model_final.pkl", "rb") as f:
        food_model = pickle.load(f)
    with open("food/tfidf_vectorizer.pkl", "rb") as f:
        food_vectorizer = pickle.load(f)
    
    # Fabric
    with open("fabric/fashion_fabric_model.pkl", "rb") as f:
        fabric_model = pickle.load(f)
    with open("fabric/fashion_vectorizer_best(1).pkl", "rb") as f:
        fabric_vectorizer = pickle.load(f)
    
    # Electronics responses
    with open("electronics/electronics.json", "r") as f:
        electronics_data = json.load(f)
    
    return food_model, food_vectorizer, fabric_model, fabric_vectorizer, electronics_data


food_model, food_vectorizer, fabric_model, fabric_vectorizer, electronics_data = load_models()


# ===========================
# Mock Mistral-Like Function
# ===========================
def mimic_mistral(user_query, electronics_data):
    """
    Mimics how a Mistral LLM would respond to an electronics issue.
    Uses keyword matching + natural phrasing + random tone variety.
    """
    query = user_query.lower()
    best_match = None

    for keyword, response in electronics_data.items():
        if keyword.lower() in query:
            best_match = response
            break

    default_responses = [
        "Try restarting your device and checking all cable connections.",
        "Please make sure your device firmware or software is up to date.",
        "Reset the settings to default — this often fixes unexpected issues.",
        "If the issue continues, contact official customer support for advanced help.",
        "Ensure the device is not overheating and has proper ventilation."
    ]

    if best_match:
        base_response = f"Here’s what I found for your issue related to **{keyword.capitalize()}**:\n\n{best_match}"
    else:
        base_response = f"{random.choice(default_responses)}"

    tone_options = [
        "Hope that helps! 😊",
        "That should fix it! 🔧",
        "Give that a try and let me know how it goes!",
        "That’s my best suggestion for now! ⚡",
        "I’m confident this will solve your issue. 👍"
    ]

    return f"{base_response}\n\n{random.choice(tone_options)}"


# ===========================
# STYLING
# ===========================
st.markdown("""
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
""", unsafe_allow_html=True)

# ===========================
# APP CONFIG
# ===========================
st.set_page_config(page_title="Kraya - Customer Support System", layout="centered")
st.sidebar.title("🛍️ Lifestyle Helper")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"]
)

# ===========================
# HOME PAGE
# ===========================
if page == "🏠 Home":
    st.title("🏠 Welcome to Kraya")
    st.markdown('<div class="banner">✨ Smart Choices, Happy Living ✨</div>', unsafe_allow_html=True)
    st.markdown("""
    Kraya is your **AI-powered customer support assistant** that helps with:
    - <span class="badge badge-food">🍎 Food</span>: Check if food is **healthy**, **balanced**, or **risky**.
    - <span class="badge badge-electronics">📱 Electronics</span>: Get smart **troubleshooting tips**.
    - <span class="badge badge-fabric">🧵 Fabric</span>: Discover the **best fabrics** for comfort and season.

    💡 Our goal: Enhance **decision-making**, boost **convenience**, and improve **satisfaction**.
    """, unsafe_allow_html=True)

# ===========================
# FOOD PAGE
# ===========================
elif page == "🍎 Food":
    st.title("🍎 Food Health Analyzer (ML-Based)")
    st.markdown('<div class="banner">🥗 Eat Smart, Live Better</div>', unsafe_allow_html=True)
    st.info("Enter food details to check if it's healthy, balanced, or unhealthy based on your trained model.")

    user_input = st.text_area("🧾 Describe your food ingredients or item", 
                              "Example: sugar, salt, oats, milk, chocolate")

    if st.button("🔍 Analyze Food"):
        if user_input.strip() == "":
            st.warning("Please enter your food details.")
        else:
            X_input = food_vectorizer.transform([user_input])
            prediction = food_model.predict(X_input)[0]
            st.markdown(f"""
            <div class="result-box">
            <span class="badge badge-food">🍎 Food Analysis</span><br><br>
            The model predicts this food as: <b>{prediction}</b>
            </div>
            """, unsafe_allow_html=True)

# ===========================
# ELECTRONICS PAGE
# ===========================
elif page == "📱 Electronics":
    st.title("📱 Electronics Support Desk (Mistral-Mimic)")
    st.markdown('<div class="banner">⚡ Smart Fixes for Everyday Devices ⚡</div>', unsafe_allow_html=True)
    st.info("Describe your problem and get instant smart support tips.")

    user_query = st.text_area("✍️ Describe your issue here", "Example: My phone battery drains too fast")

    if st.button("🛠️ Get Support"):
        if user_query.strip() == "":
            st.warning("Please enter your issue before proceeding.")
        else:
            response = mimic_mistral(user_query, electronics_data)
            st.markdown(f"""
            <div class="result-box">
            <span class="badge badge-electronics">📱 Electronics Response</span><br><br>
            {response}
            </div>
            """, unsafe_allow_html=True)

# ===========================
# FABRIC PAGE
# ===========================
elif page == "🧵 Fabric":
    st.title("🧵 Fabric Recommendation System (ML-Based)")
    st.markdown('<div class="banner">👗 Dress Smart, Feel Confident</div>', unsafe_allow_html=True)
    st.info("Enter your preferences or description to get fabric recommendations using your trained model.")

    user_input = st.text_area("🪡 Describe your skin type, tone, or weather", 
                              "Example: I have sensitive skin and live in a hot area")

    if st.button("🎯 Get Fabric Suggestion"):
        if user_input.strip() == "":
            st.warning("Please enter a description.")
        else:
            X_input = fabric_vectorizer.transform([user_input])
            prediction = fabric_model.predict(X_input)[0]
            st.markdown(f"""
            <div class="result-box">
            <span class="badge badge-fabric">🧵 Fabric Suggestion</span><br><br>
            The model suggests: <b>{prediction}</b>
            </div>
            """, unsafe_allow_html=True)
