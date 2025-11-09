import streamlit as st
from app import predict_food_label, predict_fabric_recommendation, mistral_like_response

st.set_page_config(page_title="Customer Support System", layout="wide")
st.title("🤖 Smart Customer Support System")

# Sidebar for category selection
category = st.sidebar.selectbox(
    "Select Category",
    ["Food", "Electronics", "Fabric"]
)

# -------------------------
# Food Section
# -------------------------
if category == "Food":
    st.header("🍎 Food Recommendation")
    ingredients = st.text_input("Ingredients")
    label = st.selectbox("Goal Label", ["Weight Loss", "Weight Gain"])
    calories = st.number_input("Calories", min_value=0)
    protein = st.number_input("Protein (g)", min_value=0.0)
    carbs = st.number_input("Carbs (g)", min_value=0.0)
    fiber = st.number_input("Fiber (g)", min_value=0.0)
    fat = st.number_input("Fat (g)", min_value=0.0)
    sugar = st.number_input("Sugar (g)", min_value=0.0)

    if st.button("Predict"):
        result = predict_food_label(ingredients, label, calories, protein, carbs, fiber, fat, sugar)
        st.success(result)

# -------------------------
# Electronics Section
# -------------------------
elif category == "Electronics":
    st.header("💻 Electronics Support Chat")
    query = st.text_area("Describe your issue:")
    if st.button("Get Response"):
        response = mistral_like_response(query)
        st.info(response)

# -------------------------
# Fabric Section
# -------------------------
elif category == "Fabric":
    st.header("👗 Fabric Recommendation")
    skin_tone = st.selectbox("Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("Work Level", ["Low", "Medium", "High"])
    season = st.selectbox("Season", ["Summer", "Winter", "Rainy"])

    if st.button("Recommend"):
        result = predict_fabric_recommendation(skin_tone, weather, work_level, season)
        st.write("### Recommendation Results")
        st.write(f"👗 **Recommended Outfit:** {result['Recommended Outfit']}")
        st.write(f"🧵 **Recommended Fabric:** {result['Recommended Fabric']}")
        st.write(f"🚫 **Avoid Fabrics:** {result['Avoid Fabrics']}")
