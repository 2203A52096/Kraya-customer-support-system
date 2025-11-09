import streamlit as st
import pickle
import json
import random

# -------------------------
# PAGE CONFIGURATION
# -------------------------
st.set_page_config(page_title="Customer Support Assistant", layout="centered")
st.markdown(
    "<h1 style='text-align:center; color:#4CAF50;'>🤖 Smart Customer Support Assistant</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

# -------------------------
# LOAD MODELS
# -------------------------
@st.cache_resource
def load_models():
    # Load Food Model
    with open("food/food_weight_model_final.pkl", "rb") as f:
        food_model = pickle.load(f)
    with open("food/tfidf_vectorizer_final.pkl", "rb") as f:
        food_vectorizer = pickle.load(f)

    # Load Fabric Model
    with open("fabric/fashion_fabric_model.pkl", "rb") as f:
        fabric_model = pickle.load(f)
    with open("fabric/fashion_vectorizer_best(1).pkl", "rb") as f:
        fabric_vectorizer = pickle.load(f)

    # Load Electronics JSON
    with open("electronics/electronics.json", "r") as f:
        electronics_data = json.load(f)

    return food_model, food_vectorizer, fabric_model, fabric_vectorizer, electronics_data


food_model, food_vectorizer, fabric_model, fabric_vectorizer, electronics_data = load_models()

# -------------------------
# CATEGORY SLIDER
# -------------------------
category = st.select_slider(
    "Choose a category to get started:",
    options=["Food", "Electronics", "Fabric"],
    value="Food"
)
st.markdown("---")

# -------------------------
# FOOD SECTION
# -------------------------
if category == "Food":
    st.subheader("🥗 Food Suitability Prediction")

    col1, col2 = st.columns(2)
    with col1:
        ingredients = st.text_input("Enter Ingredients")
        label = st.selectbox("Select Goal", ["Weight Loss", "Weight Gain"])
        calories = st.number_input("Calories", min_value=0)
        protein = st.number_input("Protein (g)", min_value=0.0)
        carbs = st.number_input("Carbs (g)", min_value=0.0)
    with col2:
        fiber = st.number_input("Fiber (g)", min_value=0.0)
        fat = st.number_input("Fat (g)", min_value=0.0)
        sugar = st.number_input("Sugar (g)", min_value=0.0)

    def predict_food_label(ingredients, label, calories, protein, carbs, fiber, fat, sugar):
        text_input = f"{ingredients} {label}"
        vectorized = food_vectorizer.transform([text_input])
        predicted_label = food_model.predict(vectorized)[0]

        if predicted_label.lower() == label.lower():
            if label.lower() == "weight loss":
                return "✅ The taken food product is suitable for weight loss."
            else:
                return "✅ The taken food product is suitable for weight gain."
        else:
            return f"⚠️ This food may not be suitable for {label.lower()}."

    if st.button("🔍 Predict Suitability"):
        if ingredients.strip() == "":
            st.warning("Please enter ingredients to continue.")
        else:
            result = predict_food_label(ingredients, label, calories, protein, carbs, fiber, fat, sugar)
            st.success(result)

# -------------------------
# ELECTRONICS SECTION
# -------------------------
elif category == "Electronics":
    st.subheader("💻 Electronics Support Chatbot")

    query = st.text_area("Describe your issue:")
    st.caption("Example: 'My laptop is very slow while browsing' or 'TV not connecting to Wi-Fi'")

    def mistral_like_response(user_query):
        # Simulate AI-like reasoning using electronics.json
        user_query_lower = user_query.lower()
        for item in electronics_data:
            for example in item["example_queries"]:
                if any(word in user_query_lower for word in example.lower().split()):
                    return f"**Device:** {item['device']}\n\n**Issue:** {item['problem']}\n\n💡 **Suggested Solution:** {item['solution']}"
        # Default fallback response
        return random.choice([
            "⚙️ Try restarting your device and checking for software updates.",
            "🔌 Please check the power source and connections.",
            "📶 Verify your Wi-Fi or data connection settings.",
            "🧰 Reset the device to factory settings if the issue persists.",
            "💡 If the problem continues, please contact your nearest service center."
        ])

    if st.button("💬 Get Response"):
        if query.strip() == "":
            st.warning("Please describe your issue first.")
        else:
            response = mistral_like_response(query)
            st.info(response)

# -------------------------
# FABRIC SECTION
# -------------------------
elif category == "Fabric":
    st.subheader("👗 Fabric Recommendation System")

    col1, col2 = st.columns(2)
    with col1:
        skin_tone = st.selectbox("Skin Tone", ["Fair", "Medium", "Dark"])
        weather = st.selectbox("Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    with col2:
        work_level = st.selectbox("Work Level", ["Low", "Medium", "High"])
        season = st.selectbox("Season", ["Summer", "Winter", "Rainy"])

    def predict_fabric_recommendation(skin_tone, weather, work_level, season):
        text_input = f"{skin_tone} {weather} {work_level} {season}"
        vectorized = fabric_vectorizer.transform([text_input])
        outfit = fabric_model.predict(vectorized)[0]

        recommended_fabric = random.choice(["Cotton", "Linen", "Silk", "Denim"])
        avoid_fabric = random.choice(["Wool", "Polyester", "Nylon", "Velvet"])

        return outfit, recommended_fabric, avoid_fabric

    if st.button("✨ Get Recommendation"):
        outfit, rec_fabric, avoid_fabric = predict_fabric_recommendation(
            skin_tone, weather, work_level, season
        )
        st.markdown("### 🧵 Recommendation Results")
        st.write(f"👗 **Recommended Outfit:** {outfit}")
        st.write(f"🌿 **Recommended Fabric:** {rec_fabric}")
        st.write(f"🚫 **Avoid Fabrics:** {avoid_fabric}")
