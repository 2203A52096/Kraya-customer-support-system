import streamlit as st
import random
import pandas as pd

# ---------------- ELECTRONICS MOCK FUNCTION ----------------
def mimic_mistral_response(query, data):
    """Simulate Mistral model using the electronics JSON data."""
    if not data:
        return "No electronics data found."
    query_lower = query.lower()
    for item in data:
        for ex in item["example_queries"]:
            if any(word in query_lower for word in ex.lower().split()):
                return f"**Device:** {item['device']}\n**Issue:** {item['problem']}\n\n💡 **Suggested Fix:** {item['solution']}"
    # Random fallback
    item = random.choice(data)
    return f"**Device:** {item['device']}\n**Issue:** {item['problem']}\n\n💡 **Suggested Fix:** {item['solution']}"

# ---------------- FABRIC PREDICTION FUNCTION ----------------
def predict_fabric(model, vectorizer, skin_tone, weather, work_level, season):
    if not model or not vectorizer:
        return "⚠️ Model not available.", "N/A", "N/A"

    text_input = f"{skin_tone} {weather} {work_level} {season}"
    vec = vectorizer.transform([text_input])
    outfit = model.predict(vec)[0]

    # Add extra generated context
    rec_fabric = random.choice(["Cotton", "Linen", "Silk", "Denim"])
    avoid_fabric = random.choice(["Wool", "Polyester", "Leather"])
    return outfit, rec_fabric, avoid_fabric

# ---------------- FOOD PREDICTION FUNCTION ----------------
def predict_food(model, vectorizer, ingredients, label, calories, protein, carbs, fiber, fat, sugar):
    if not model or not vectorizer:
        return "⚠️ Model not available."

    text = f"{ingredients} {calories} {protein} {carbs} {fiber} {fat} {sugar}"
    vec = vectorizer.transform([text])
    pred_label = model.predict(vec)[0]

    if pred_label.lower() == label.lower():
        if pred_label.lower() == "weight loss":
            return f"✅ The selected food product is suitable for **Weight Loss**."
        else:
            return f"✅ The selected food product is suitable for **Weight Gain**."
    else:
        return f"❌ The food might not match your target goal. Model predicted: **{pred_label}**"

# ---------------- MAIN UI FUNCTION ----------------
def show_ui(food_model, food_vectorizer, fabric_model, fabric_vectorizer, electronics_data):
    st.markdown("<h1 style='text-align:center;'>🤖 Smart Customer Support System</h1>", unsafe_allow_html=True)
    st.write("### Select a category to get AI-powered support:")

    section = st.sidebar.radio("Choose a Section", ["🍽️ Food", "💻 Electronics", "👗 Fabric"])

    # ---------------- FOOD SECTION ----------------
    if section == "🍽️ Food":
        st.subheader("🥗 Food Recommendation System")
        ingredients = st.text_area("Enter Ingredients:")
        label = st.selectbox("Target Label", ["Weight Loss", "Weight Gain"])
        col1, col2, col3 = st.columns(3)
        with col1:
            calories = st.number_input("Calories", min_value=0)
            protein = st.number_input("Protein (g)", min_value=0)
        with col2:
            carbs = st.number_input("Carbs (g)", min_value=0)
            fiber = st.number_input("Fiber (g)", min_value=0)
        with col3:
            fat = st.number_input("Fat (g)", min_value=0)
            sugar = st.number_input("Sugar (g)", min_value=0)

        if st.button("Predict Food Suitability"):
            result = predict_food(food_model, food_vectorizer, ingredients, label, calories, protein, carbs, fiber, fat, sugar)
            st.success(result)

    # ---------------- ELECTRONICS SECTION ----------------
    elif section == "💻 Electronics":
        st.subheader("🔌 Electronics Troubleshooter")
        query = st.text_area("Describe your issue:")
        if st.button("Get Solution"):
            response = mimic_mistral_response(query, electronics_data)
            st.markdown(response)

    # ---------------- FABRIC SECTION ----------------
    elif section == "👗 Fabric":
        st.subheader("🧵 Fabric Recommendation System")
        skin_tone = st.selectbox("Skin Tone", ["Fair", "Medium", "Dark"])
        weather = st.selectbox("Weather Condition", ["Sunny", "Rainy", "Cold", "Humid"])
        work_level = st.selectbox("Work Level", ["Low", "Moderate", "High"])
        season = st.selectbox("Season", ["Summer", "Winter", "Monsoon", "Autumn"])

        if st.button("Recommend Outfit"):
            outfit, rec, avoid = predict_fabric(fabric_model, fabric_vectorizer, skin_tone, weather, work_level, season)
            st.markdown(f"### 👗 Recommended Outfit: **{outfit}**")
            st.markdown(f"**✅ Recommended Fabric:** {rec}")
            st.markdown(f"**🚫 Avoid Fabric:** {avoid}")

    # ---------------- FOOTER ----------------
    st.markdown("---")
    st.markdown("<p style='text-align:center;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
