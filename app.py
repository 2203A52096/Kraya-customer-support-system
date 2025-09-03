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
        return "<span style='color:red; font-weight:bold;'>Unhealthy:</span> High sugar/fat content. May lead to weight gain, heart issues."
    elif calories < 100 and fat < 5 and sugar < 5:
        return "<span style='color:green; font-weight:bold;'>Healthy</span> and suitable for <b>weight loss</b>."
    elif calories > 300 and protein > 10:
        return "<span style='color:green; font-weight:bold;'>Healthy</span> and suitable for <b>weight gain</b> (high protein/calories)."
    else:
        return "<span style='color:orange; font-weight:bold;'>Moderately healthy</span>. Watch out for specific ingredients."

def suggest_fabric(skin_type, skin_tone, weather, work_level, season):
    avoid_fabrics = []
    preferred_fabrics = []
    color_suggestions = []

    if skin_type == "Sensitive":
        avoid_fabrics += ["Polyester", "Nylon"]
        preferred_fabrics += ["Cotton", "Bamboo"]
    elif skin_type == "Oily":
        avoid_fabrics += ["Silk"]
        preferred_fabrics += ["Linen", "Cotton"]
    else:
        preferred_fabrics += ["Cotton", "Linen"]

    if weather == "Hot":
        avoid_fabrics += ["Wool"]
        preferred_fabrics += ["Cotton", "Linen"]
    elif weather == "Cold":
        preferred_fabrics += ["Wool", "Fleece"]
    elif weather == "Humid":
        avoid_fabrics += ["Polyester"]
        preferred_fabrics += ["Bamboo", "Cotton"]

    if work_level == "High":
        preferred_fabrics += ["Moisture-wicking blends"]

    if season == "Winter":
        preferred_fabrics += ["Wool", "Fleece"]
    elif season == "Summer":
        preferred_fabrics += ["Cotton", "Linen"]

    if skin_tone == "Fair":
        color_suggestions = ["Soft pastels", "Cool blues", "Lavender"]
    elif skin_tone == "Medium":
        color_suggestions = ["Earth tones", "Olive", "Warm reds"]
    else:
        color_suggestions = ["Bright colors", "Bold yellows", "Vibrant blues"]

    avoid_fabrics = list(set(avoid_fabrics))
    preferred_fabrics = list(set(preferred_fabrics))

    return f"""
<div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
    <b style="color:red;">Avoid Fabrics:</b> {", ".join(avoid_fabrics)}<br><br>
    <b style="color:green;">Recommended Fabrics:</b> {", ".join(preferred_fabrics)}<br><br>
    <b style="color:blue;">Suggested Colors:</b> {", ".join(color_suggestions)}
</div>
"""

# ---------------- MAIN APP ---------------- #

st.set_page_config(page_title="Kraya - Lifestyle Helper", layout="centered")

st.sidebar.markdown("<h2 style='color:#2E8B57;'>Lifestyle Helper</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("Go to", ["Home", "Food", "Electronics", "Fabric"])

# ---------------- HOME PAGE ---------------- #

if page == "Home":
    st.markdown("<h1 style='color:#4682B4;'>Kraya: Smart Lifestyle Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("""
Welcome to **Kraya**, your smart assistant for healthier and better lifestyle decisions.

Choose a category from the sidebar:

- **Food**: Analyze food for health impact.
- **Electronics**: Get post-purchase support.
- **Fabric**: Know what suits your skin and weather.
    """)

# ---------------- FOOD PAGE ---------------- #

elif page == "Food":
    st.markdown("<h2 style='color:#D2691E;'>Food Health Analyzer</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("Enter Food Information")

    ingredients = st.text_area("Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    calories = st.number_input("Calories per serving", min_value=0)
    fat = st.number_input("Total Fat (g)", min_value=0.0)
    sugar = st.number_input("Sugar (g)", min_value=0.0)
    fiber = st.number_input("Dietary Fiber (g)", min_value=0.0)
    protein = st.number_input("Protein (g)", min_value=0.0)

    if st.button("Analyze"):
        result = analyze_food(ingredients, calories, fat, sugar, fiber, protein)
        st.markdown(f"<div style='background-color:#FFFACD; padding:15px; border-radius:10px;'>{result}</div>", unsafe_allow_html=True)

# ---------------- ELECTRONICS PAGE ---------------- #

elif page == "Electronics":
    st.markdown("<h2 style='color:#4169E1;'>Electronics Help Desk</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    devices = ["Smartphone", "Laptop", "TV", "Washing Machine", "Refrigerator"]
    device = st.selectbox("Select your device", devices)

    user_input = st.text_area("Describe your issue here")

    if st.button("Apply"):
        if user_input.strip() == "":
            st.warning("Please describe your issue before applying.")
        else:
            st.markdown("### Support Suggestion")
            user_input_lower = user_input.lower()

            suggestion = ""
            if "battery" in user_input_lower:
                suggestion = "Check if the battery is swollen or not holding charge. Try replacing it."
            elif "screen" in user_input_lower:
                suggestion = "Screen issues may be due to physical damage or loose connectors."
            elif "not turning on" in user_input_lower:
                suggestion = "Ensure the power cable is connected. Try a hard reset."
            elif "noise" in user_input_lower:
                suggestion = "Unusual noise may indicate motor issues or loose parts."
            else:
                suggestion = "Please contact customer support for detailed troubleshooting."

            st.markdown(f"<div style='background-color:#E6E6FA; padding:15px; border-radius:10px;'>{suggestion}</div>", unsafe_allow_html=True)

# ---------------- FABRIC PAGE ---------------- #

elif page == "Fabric":
    st.markdown("<h2 style='color:#8B008B;'>Fabric Recommendation System</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("Enter your profile")

    skin_type = st.selectbox("Skin Type", ["Dry", "Oily", "Sensitive", "Normal"])
    skin_tone = st.selectbox("Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("Season", ["Summer", "Winter", "Spring", "Autumn"])

    if st.button("Get Fabric Suggestions"):
        result = suggest_fabric(skin_type, skin_tone, weather, work_level, season)
        st.markdown(result, unsafe_allow_html=True)
