import streamlit as st

def load_interface():
    st.sidebar.title("Customer Support System")
    st.sidebar.write("Choose a category to get started:")

    category = st.sidebar.radio(
        "Select Category:",
        ["Food", "Electronics", "Fabric"]
    )

    return category


def food_ui():
    st.header("🍎 Food Product Suitability Checker")
    st.write("Enter details about your food product to see if it suits your fitness goal.")

    label = st.selectbox("Select Label (Goal):", ["Weight Loss", "Weight Gain"])
    ingredients = st.text_area("Ingredients:")
    calories = st.number_input("Calories:", min_value=0)
    protein = st.number_input("Protein (g):", min_value=0.0)
    carbs = st.number_input("Carbohydrates (g):", min_value=0.0)
    fiber = st.number_input("Fiber (g):", min_value=0.0)
    fat = st.number_input("Fat (g):", min_value=0.0)
    sugar = st.number_input("Sugar (g):", min_value=0.0)

    if st.button("Predict"):
        return {
            "label": label,
            "ingredients": ingredients,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fiber": fiber,
            "fat": fat,
            "sugar": sugar
        }
    return None


def electronics_ui():
    st.header("💡 Electronics Support Assistant")
    st.write("Describe your issue or ask a question about any electronic device.")

    query = st.text_area("Enter your question:")
    if st.button("Get Response"):
        return query
    return None


def fabric_ui():
    st.header("👕 Fabric & Outfit Recommendation")
    st.write("Get outfit suggestions based on your skin tone, weather, and work level.")

    skin_tone = st.selectbox("Skin Tone:", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("Weather Condition:", ["Sunny", "Rainy", "Cold", "Humid"])
    work_level = st.selectbox("Work Level:", ["Light", "Moderate", "Heavy"])
    season = st.selectbox("Season:", ["Summer", "Winter", "Monsoon", "Spring"])

    if st.button("Recommend Outfit"):
        return {
            "Skin Tone": skin_tone,
            "Weather Condition": weather,
            "Work Level": work_level,
            "Season": season
        }
    return None
