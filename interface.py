import streamlit as st

def show_ui(predict_food, predict_fabric, get_electronic_response):
    st.set_page_config(page_title="Smart Customer Support", page_icon="🛍️", layout="centered")
    
    st.markdown(
        """
        <style>
        .main { background-color: #f7f9fc; }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            font-size: 16px;
        }
        h1, h2 { text-align: center; color: #2E4053; }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🛍️ Kraya Smart Customer Support System")
    st.markdown("### Get recommendations and support for Food, Electronics, and Fabrics")

    # Sidebar slider for section selection
    section = st.sidebar.radio("Choose Category", ["🥗 Food", "⚡ Electronics", "👗 Fabric"])

    # ================= FOOD =================
    if section == "🥗 Food":
        st.header("🍎 Food Recommendation System")
        st.markdown("Enter the nutritional details below:")

        ingredients = st.text_input("Ingredients")
        label = st.selectbox("Label", ["Weight Loss", "Weight Gain"])
        calories = st.number_input("Calories", min_value=0)
        protein = st.number_input("Protein (g)", min_value=0.0)
        carbs = st.number_input("Carbs (g)", min_value=0.0)
        fiber = st.number_input("Fiber (g)", min_value=0.0)
        fat = st.number_input("Fat (g)", min_value=0.0)
        sugar = st.number_input("Sugar (g)", min_value=0.0)

        if st.button("Predict Food Category"):
            data = {
                "ingredients": ingredients,
                "label": label,
                "calories": calories,
                "protein": protein,
                "carbs": carbs,
                "fiber": fiber,
                "fat": fat,
                "sugar": sugar
            }
            st.success(predict_food(data))

    # ================= ELECTRONICS =================
    elif section == "⚡ Electronics":
        st.header("🔌 Electronics Support Assistant")
        st.markdown("Describe your issue below:")

        query = st.text_area("Enter your electronic product query")

        if st.button("Get Support Response"):
            response = get_electronic_response(query)
            st.info(response)

    # ================= FABRIC =================
    elif section == "👗 Fabric":
        st.header("🧵 Fabric Recommendation System")

        skin = st.selectbox("Skin Tone", ["Fair", "Medium", "Dark"])
        weather = st.selectbox("Weather Condition", ["Hot", "Cold", "Rainy"])
        work = st.selectbox("Work Level", ["Low", "Medium", "High"])
        season = st.selectbox("Season", ["Summer", "Winter", "Monsoon"])

        if st.button("Recommend Fabrics"):
            inputs = {
                "Skin Tone": skin,
                "Weather Condition": weather,
                "Work Level": work,
                "Season": season
            }
            rec = predict_fabric(inputs)
            st.success(f"Recommended Outfit: {rec['Recommended Outfit']}")
            st.info(f"Recommended Fabric: {rec['Recommended Fabric']}")
            st.warning(f"Avoid Fabrics: {rec['Avoid Fabrics']}")
