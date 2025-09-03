import streamlit as st

# ---------------- UTILITY FUNCTIONS ---------------- #

def analyze_food(ingredients, calories, fat, sugar, fiber, protein):
    ing_list = [i.strip().lower() for i in ingredients.split(",")]

    unhealthy_ingredients = ["sugar", "corn syrup", "hydrogenated oil", "trans fat", "artificial"]
    healthy_tags = []
    unhealthy_tags = []

    for ing in ing_list:
        if any(bad in ing for bad in unhealthy_ingredients):
            unhealthy_tags.append(ing)
        elif "whole" in ing or "vegetable" in ing or "fiber" in ing:
            healthy_tags.append(ing)

    # Rule-based analysis
    if len(unhealthy_tags) > 2 or sugar > 15 or fat > 20:
        return """
        <span style='color: red; font-weight: bold; font-size:18px;'>❌ Unhealthy:</span> 
        High sugar/fat content. May lead to weight gain, heart issues.
        """
    elif calories < 100 and fat < 5 and sugar < 5:
        return """
        <span style='color: green; font-weight: bold; font-size:18px;'>✅ Healthy</span> and suitable for 
        <span style='color: blue; font-weight: bold;'>weight loss</span>.
        """
    elif calories > 300 and protein > 10:
        return """
        <span style='color: green; font-weight: bold; font-size:18px;'>✅ Healthy</span> and suitable for 
        <span style='color: blue; font-weight: bold;'>weight gain</span> (high protein/calories).
        """
    else:
        return """
        <span style='color: orange; font-weight: bold; font-size:18px;'>⚠️ Moderately healthy</span>. 
        Watch out for specific ingredients.
        """

def suggest_fabric(skin_type, skin_tone, weather, work_level, season):
    avoid_fabrics = []
    preferred_fabrics = []
    color_suggestions = []

    # Skin type rules
    if skin_type == "Sensitive":
        avoid_fabrics += ["Polyester", "Nylon"]
        preferred_fabrics += ["Cotton", "Bamboo"]
    elif skin_type == "Oily":
        avoid_fabrics += ["Silk"]
        preferred_fabrics += ["Linen", "Cotton"]
    else:
        preferred_fabrics += ["Cotton", "Linen"]

    # Weather rules
    if weather == "Hot":
        avoid_fabrics += ["Wool"]
        preferred_fabrics += ["Cotton", "Linen"]
    elif weather == "Cold":
        preferred_fabrics += ["Wool", "Fleece"]
    elif weather == "Humid":
        avoid_fabrics += ["Polyester"]
        preferred_fabrics += ["Bamboo", "Cotton"]

    # work level
    if work_level == "High":
        preferred_fabrics += ["Moisture-wicking blends"]

    # Season
    if season == "Winter":
        preferred_fabrics += ["Wool", "Fleece"]
    elif season == "Summer":
        preferred_fabrics += ["Cotton", "Linen"]

    # Skin tone rules
    if skin_tone == "Fair":
        color_suggestions = ["Soft pastels", "Cool blues", "Lavender"]
    elif skin_tone == "Medium":
        color_suggestions = ["Earth tones", "Olive", "Warm reds"]
    else:
        color_suggestions = ["Bright colors", "Bold yellows", "Vibrant blues"]

    avoid_fabrics = list(set(avoid_fabrics))
    preferred_fabrics = list(set(preferred_fabrics))

    return f"""
    <div style='font-size:16px;'>
    <span style='color:#D9534F; font-weight:bold;'>❌ Avoid Fabrics:</span> {", ".join(avoid_fabrics)}<br><br>
    <span style='color:#5CB85C; font-weight:bold;'>✅ Recommended Fabrics:</span> {", ".join(preferred_fabrics)}<br><br>
    <span style='color:#0275D8; font-weight:bold;'>🎨 Suggested Colors for You:</span> {", ".join(color_suggestions)}
    </div>
    """

# ---------------- MAIN APP ---------------- #

st.set_page_config(page_title="Lifestyle Helper App", layout="centered")

st.sidebar.title("🛍️ Lifestyle Helper")
page = st.sidebar.radio("Go to", ["Home", "Food", "Electronics", "Fabric"])

# ---------------- HOME PAGE ---------------- #

if page == "Home":
    st.title("🏠 Kraya")
    st.markdown("""
    The customer support system for making better choices before purchasing and after purchasing a product in food, electronics, and fabric categories.

    -  **🍎 Food**: Check if your food is healthy or not.
    -  **📱 Electronics**: Get help for your electronic products.
    -  **🧵 Fabric**: Know what fabrics suit your skin and weather.
    """)

# ---------------- FOOD PAGE ---------------- #

elif page == "Food":
    st.title("🍎 Food Health Analyzer")

    st.subheader("Enter Food Information")

    ingredients = st.text_area("Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    calories = st.number_input("Calories per serving", min_value=0)
    fat = st.number_input("Total Fat (g)", min_value=0.0)
    sugar = st.number_input("Sugar (g)", min_value=0.0)
    fiber = st.number_input("Dietary Fiber (g)", min_value=0.0)
    protein = st.number_input("Protein (g)", min_value=0.0)

    if st.button("🔍 Analyze Food"):
        result = analyze_food(ingredients, calories, fat, sugar, fiber, protein)
        st.markdown(result, unsafe_allow_html=True)

# ---------------- ELECTRONICS PAGE ---------------- #

elif page == "Electronics":
    st.title("📱 Electronics Help Desk")

    devices = ["Smartphone", "Laptop", "TV", "Washing Machine", "Refrigerator"]
    device = st.selectbox("Select your device", devices)

    user_input = st.text_area("Describe your issue here")

    if st.button("🛠️ Get Support"):
        if user_input.strip() == "":
            st.warning("⚠️ Please describe your issue before applying.")
        else:
            st.markdown("### **🔧 Support Suggestion:**")
            user_input_lower = user_input.lower()

            if "battery" in user_input_lower:
                st.write("🔋 Check if the battery is swollen or not holding charge. Try replacing it.")
            elif "screen" in user_input_lower:
                st.write("🖥️ Screen issues may be due to physical damage or loose connectors.")
            elif "not turning on" in user_input_lower:
                st.write("⚡ Ensure the power cable is connected. Try a hard reset.")
            elif "noise" in user_input_lower:
                st.write("🔊 Unusual noise may indicate motor issues or loose parts.")
            else:
                st.write("📞 Please contact customer support for detailed troubleshooting.")

# ---------------- FABRIC PAGE ---------------- #

elif page == "Fabric":
    st.title("🧵 Fabric Recommendation System")

    st.subheader("Enter your profile")

    skin_type = st.selectbox("Skin Type", ["Dry", "Oily", "Sensitive", "Normal"])
    skin_tone = st.selectbox("Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("Season", ["Summer", "Winter", "Spring", "Autumn"])

    if st.button("🎯 Get Fabric Suggestions"):
        result = suggest_fabric(skin_type, skin_tone, weather, work_level, season)
        st.markdown(result, unsafe_allow_html=True)
