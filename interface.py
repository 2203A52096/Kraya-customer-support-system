import streamlit as st
from app import predict_food_label, predict_fabric_recommendation, mistral_like_response

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="Customer Support Assistant", layout="centered")
st.markdown(
    "<h1 style='text-align:center; color:#4CAF50;'>🤖 Smart Customer Support Assistant</h1>",
    unsafe_allow_html=True,
)

# -------------------------
# Category Selector (Slider Style)
# -------------------------
st.markdown("---")
category = st.select_slider(
    "Choose a category to get started:",
    options=["Food", "Electronics", "Fabric"],
    value="Food"
)
st.markdown("---")

# -------------------------
# Food Section
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

    if st.button("🔍 Predict Suitability"):
        result = predict_food_label(ingredients, label, calories, protein, carbs, fiber, fat, sugar)
        st.success(result)

# -------------------------
# Electronics Section
# -------------------------
elif category == "Electronics":
    st.subheader("💻 Electronics Support Chatbot")
    query = st.text_area("Describe your issue:")
    if st.button("💬 Get Response"):
        response = mistral_like_response(query)
        st.info(response)

# -------------------------
# Fabric Section
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

    if st.button("✨ Get Recommendation"):
        result = predict_fabric_recommendation(skin_tone, weather, work_level, season)
        st.markdown("### 🧵 Recommendation Results")
        st.write(f"👗 **Recommended Outfit:** {result['Recommended Outfit']}")
        st.write(f"🌿 **Recommended Fabric:** {result['Recommended Fabric']}")
        st.write(f"🚫 **Avoid Fabrics:** {result['Avoid Fabrics']}")
