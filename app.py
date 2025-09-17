import streamlit as st

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="Kraya - Lifestyle Helper", layout="centered")

# ---------------- CUSTOM CSS ---------------- #
st.markdown(
    """
    <style>
    /* Sidebar background pastel color */
    [data-testid="stSidebar"] {
        background-color: #F7E9E9;  /* pastel pink */
        color: #5A3E36;
    }
    /* Sidebar title */
    [data-testid="stSidebar"] > div:first-child {
        font-size: 24px;
        font-weight: 700;
        color: #9A5F6F;
    }
    /* Badge styles */
    .badge {
        display: inline-block;
        padding: 0.25em 0.6em;
        font-size: 0.75em;
        font-weight: 700;
        color: white;
        border-radius: 0.25rem;
    }
    .badge-food {background-color: #FF6F61;}
    .badge-electronics {background-color: #6BAED6;}
    .badge-fabric {background-color: #8BC34A;}
    .badge-healthy {background-color: #4CAF50;}
    .badge-unhealthy {background-color: #F44336;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- UTILITY FUNCTIONS ---------------- #
def analyze_food(ingredients, calories, fat, sugar, fiber, protein):
    ing_list = [i.strip().lower() for i in ingredients.split(",")]
    unhealthy_ingredients = ["sugar", "corn syrup", "hydrogenated oil", "trans fat", "artificial"]

    unhealthy_tags = [ing for ing in ing_list if any(bad in ing for bad in unhealthy_ingredients)]
    healthy_tags = [ing for ing in ing_list if "whole" in ing or "vegetable" in ing or "fiber" in ing]

    if len(unhealthy_tags) > 2 or sugar > 15 or fat > 20:
        return """<span class="badge badge-unhealthy">❌ Unhealthy</span>: 
                  <b>High sugar/fat</b> content. May lead to <b>weight gain</b> & heart issues."""
    elif calories < 100 and fat < 5 and sugar < 5:
        return """<span class="badge badge-healthy">✅ Healthy</span>: 
                  Good for <b>weight loss</b>. Low calories & sugar."""
    elif calories > 300 and protein > 10:
        return """<span class="badge badge-healthy">✅ Healthy</span>: 
                  Supports <b>weight gain</b> (high protein & calories)."""
    else:
        return """<span style='color: #FFA500; font-weight:bold;'>⚠️ Moderately Healthy</span>: 
                  Balanced but watch for <b>ingredients</b>."""

def suggest_fabric(skin_type, skin_tone, weather, work_level, season):
    avoid_fabrics, preferred_fabrics, color_suggestions = [], [], []

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

    return f"""
    <div style='font-size:16px;'>
    <span style='color:#D9534F; font-weight:bold;'>❌ Avoid Fabrics:</span> {", ".join(set(avoid_fabrics))}<br><br>
    <span style='color:#5CB85C; font-weight:bold;'>✅ Recommended Fabrics:</span> {", ".join(set(preferred_fabrics))}<br><br>
    <span style='color:#0275D8; font-weight:bold;'>🎨 Suggested Colors:</span> {", ".join(color_suggestions)}
    </div>
    """

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🛍️ Lifestyle Helper")
page = st.sidebar.radio("Go to", ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"])

# ---------------- PAGES ---------------- #
if page == "🏠 Home":
    st.title("🏠 Kraya - Lifestyle Helper")
    st.markdown(
        """
        <h3 style='color:#6A1B9A;'>✨ Smarter Choices, Healthier Living ✨</h3>
        <p style='font-size:16px;'>
        Welcome to <b>Kraya</b>, a <b>customer support system</b> that guides you in three domains:
        </p>
        - <span class="badge badge-food">🍎 Food</span>: <b>Check healthiness</b> & impact on <b>weight</b>.  
        - <span class="badge badge-fabric">🧵 Fabric</span>: <b>Suggests fabrics & colors</b> for <b>skin & weather</b>.  
        - <span class="badge badge-electronics">📱 Electronics</span>: <b>Troubleshooting assistant</b> for devices.  
        <br>
        <p style='color:#444;'>Kraya ensures <b>better decisions, higher satisfaction, and convenience</b>. 🚀</p>
        """,
        unsafe_allow_html=True,
    )

elif page == "🍎 Food":
    st.title("🍎 Food Health Analyzer")
    st.markdown(
        """
        <p style='font-size:15px; color:#444;'>
        This module <b>analyzes ingredients, calories, sugar, fat, and protein</b> to tell if a food is 
        <span style='color:#4CAF50; font-weight:bold;'>Healthy</span> or 
        <span style='color:#F44336; font-weight:bold;'>Unhealthy</span>.  
        It also provides <b>weight loss</b> and <b>weight gain</b> recommendations. 🥗🍩
        </p>
        """,
        unsafe_allow_html=True,
    )

    ingredients = st.text_area("Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    calories = st.number_input("Calories per serving", min_value=0)
    fat = st.number_input("Total Fat (g)", min_value=0.0)
    sugar = st.number_input("Sugar (g)", min_value=0.0)
    fiber = st.number_input("Dietary Fiber (g)", min_value=0.0)
    protein = st.number_input("Protein (g)", min_value=0.0)

    if st.button("🔍 Analyze Food"):
        result = analyze_food(ingredients, calories, fat, sugar, fiber, protein)
        st.markdown(result, unsafe_allow_html=True)

elif page == "📱 Electronics":
    st.title("📱 Electronics Help Desk")
    st.markdown(
        """
        <p style='font-size:15px; color:#444;'>
        The <b>Electronics module</b> works like a <b>troubleshooting assistant</b>.  
        Select a <b>device</b>, describe your <b>issue</b>, and Kraya will suggest possible fixes.  
        Covers <b>battery, screen, power, and noise</b> issues. ⚡🔧
        </p>
        """,
        unsafe_allow_html=True,
    )

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

elif page == "🧵 Fabric":
    st.title("🧵 Fabric Recommendation System")
    st.markdown(
        """
        <p style='font-size:15px; color:#444;'>
        This module recommends <b>fabrics and colors</b> based on your <b>skin type, tone, weather, activity level, 
        and season</b>.  
        Helps in choosing <b>comfortable</b> and <b>stylish</b> outfits. 👗🎨
        </p>
        """,
        unsafe_allow_html=True,
    )

    skin_type = st.selectbox("Skin Type", ["Dry", "Oily", "Sensitive", "Normal"])
    skin_tone = st.selectbox("Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("Season", ["Summer", "Winter", "Spring", "Autumn"])

    if st.button("🎯 Get Fabric Suggestions"):
        result = suggest_fabric(skin_type, skin_tone, weather, work_level, season)
        st.markdown(result, unsafe_allow_html=True)

# ---------------- FOOTER ---------------- #
st.markdown(
    """
    <hr>
    <center>
    <p style='color:#777; font-size:14px;'>
    💡 <b>Kraya</b> - Your Lifestyle Support System for <span style='color:#FF6F61;'>Food</span>, 
    <span style='color:#8BC34A;'>Fabric</span>, and <span style='color:#6BAED6;'>Electronics</span>.
    </p>
    </center>
    """,
    unsafe_allow_html=True,
)
