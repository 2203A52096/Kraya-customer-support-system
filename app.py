import streamlit as st

# ---------- Custom Styling ---------- #
st.markdown("""
<style>
/* Smooth transitions for hover */
.stButton>button, .stSelectbox div {
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* Hover effect for buttons */
.stButton>button:hover {
  background-color: #d6bdd9 !important;
  color: #2c3e50 !important;
}

/* Headings */
h1, h2, h3 {
  color: #2c3e50;
  font-weight: bold;
  padding: 0.3rem 0;
}

/* Section container */
.section {
  background-color: #f0f5f9;
  padding: 15px;
  border-radius: 10px;
  margin-top: 20px;
}

/* Result output box */
.result-box {
  background-color: #fff8dc;
  padding: 12px;
  border-radius: 8px;
  font-style: italic;
  margin-top: 10px;
}

/* Sidebar tweaks */
.sidebar .sidebar-content {
  padding-top: 1rem;
  background-color: #f6f7fb;
}
</style>
""", unsafe_allow_html=True)

# ---------- Utility Functions ---------- #
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

    if len(unhealthy_tags) > 2 or sugar > 15 or fat > 20:
        return "_**Unhealthy:** High sugar/fat content. May lead to weight gain, heart issues._"
    elif calories < 100 and fat < 5 and sugar < 5:
        return "_**Healthy** and suitable for **weight loss**._"
    elif calories > 300 and protein > 10:
        return "_**Healthy** and suitable for **weight gain** (high protein/calories)._"
    else:
        return "_**Moderately healthy**. Watch out for specific ingredients._"

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
_**Avoid Fabrics:**_ {", ".join(avoid_fabrics)}  
_**Recommended Fabrics:**_ {", ".join(preferred_fabrics)}  
_**Suggested Colors for You:**_ {", ".join(color_suggestions)}
"""

# ---------- App Layout ---------- #
st.set_page_config(page_title="Selection Assistant", layout="centered")
st.sidebar.markdown("## **Selection Assistant**")
page = st.sidebar.radio("Go to", ["Home", "Food", "Electronics", "Fabric"])

# ---------- Pages ---------- #
if page == "Home":
    st.markdown("## **Kraya**")
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.write("""
Welcome to **Kraya**, your personal selection assistant for smarter decisions in:

- **Food**: Is it healthy?  
- **Electronics**: Need troubleshooting tips?  
- **Fabric**: Perfect match for your skin and weather  
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Food":
    st.markdown("## **Food Health Analyzer**")
    st.markdown('<div class="section">', unsafe_allow_html=True)

    ingredients = st.text_area("Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    calories = st.number_input("Calories per serving", min_value=0)
    fat = st.number_input("Total Fat (g)", min_value=0.0)
    sugar = st.number_input("Sugar (g)", min_value=0.0)
    fiber = st.number_input("Dietary Fiber (g)", min_value=0.0)
    protein = st.number_input("Protein (g)", min_value=0.0)

    if st.button("Analyze"):
        result = analyze_food(ingredients, calories, fat, sugar, fiber, protein)
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Electronics":
    st.markdown("## **Electronics AI Troubleshooter**")
    st.markdown('<div class="section">', unsafe_allow_html=True)

    device = st.selectbox("Select your device", ["Smartphone", "Laptop", "TV", "Washing Machine", "Refrigerator"])
    user_input = st.text_area("Describe your issue here")

    if st.button("Apply"):
        if user_input.strip() == "":
            st.warning("Please describe your issue before applying.")
        else:
            st.markdown("### **Support Suggestion**")
            user_input_lower = user_input.lower()

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

            st.markdown(f'<div class="result-box">{suggestion}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Fabric":
    st.markdown("## **Fabric Recommendation System**")
    st.markdown('<div class="section">', unsafe_allow_html=True)

    skin_type = st.selectbox("Skin Type", ["Dry", "Oily", "Sensitive", "Normal"])
    skin_tone = st.selectbox("Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("Season", ["Summer", "Winter", "Spring", "Autumn"])

    if st.button("Get Fabric Suggestions"):
        result = suggest_fabric(skin_type, skin_tone, weather, work_level, season)
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
