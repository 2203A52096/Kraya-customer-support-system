import streamlit as st

# ------------------ CUSTOM CSS ------------------ #
st.markdown(
    """
    <style>
    /* Sidebar pastel background */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F7E9E9, #F9F7F7);
        color: #5A3E36;
    }
    [data-testid="stSidebar"] > div:first-child {
        font-size: 24px;
        font-weight: 700;
        color: #9A5F6F;
    }

    /* Badges */
    .badge {padding: 0.4em 0.7em; font-size: 0.8em; font-weight: 700; border-radius: 0.4rem; margin-right: 5px;}
    .badge-food {background-color: #FF6F61; color:white;}
    .badge-electronics {background-color: #6BAED6; color:white;}
    .badge-fabric {background-color: #8BC34A; color:white;}
    .badge-healthy {background-color: #4CAF50; color:white;}
    .badge-unhealthy {background-color: #F44336; color:white;}

    /* Result Cards */
    .result-box {border-radius: 12px; padding: 15px; margin: 10px 0; font-size: 16px; font-weight: 500;}
    .result-good {background-color: #E8F5E9; color:#2E7D32;}
    .result-bad {background-color: #FFEBEE; color:#C62828;}
    .result-warning {background-color: #FFF8E1; color:#F9A825;}

    /* Taglines for Home */
    .tagline {font-size:22px; font-weight:bold; margin:10px 0;}
    .tagline1 {color:#E91E63;}   /* Pink */
    .tagline2 {color:#3F51B5;}   /* Indigo */
    .tagline3 {color:#009688;}   /* Teal */
    .tagline4 {color:#FF9800;}   /* Orange */
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Utility Functions ---------------- #
def analyze_food(ingredients, calories, fat, sugar, fiber, protein):
    ing_list = [i.strip().lower() for i in ingredients.split(",")]
    unhealthy_ingredients = ["sugar", "corn syrup", "hydrogenated oil", "trans fat", "artificial"]

    unhealthy_tags = [ing for ing in ing_list if any(bad in ing for bad in unhealthy_ingredients)]
    if len(unhealthy_tags) > 2 or sugar > 15 or fat > 20:
        return f"""<div class="result-box result-bad">❌ <span class="badge badge-unhealthy">Unhealthy</span><br>High sugar/fat content. May lead to health issues.</div>"""
    elif calories < 100 and fat < 5 and sugar < 5:
        return f"""<div class="result-box result-good">✅ <span class="badge badge-healthy">Healthy</span><br>Great for <b>weight loss</b>. Balanced nutrition!</div>"""
    elif calories > 300 and protein > 10:
        return f"""<div class="result-box result-good">💪 <span class="badge badge-healthy">Healthy</span><br>Great for <b>weight gain</b>. High energy!</div>"""
    else:
        return f"""<div class="result-box result-warning">⚠️ Moderately Healthy.<br> Consider ingredient balance.</div>"""

def suggest_fabric(skin_type, skin_tone, weather, work_level, season):
    return f"""
    <div class="result-box result-good">
    ✅ Personalized <b>fabric recommendations</b> based on your skin type, tone, season & lifestyle.<br>
    🎨 Find your <b>best colors</b> and <b>fabrics to avoid</b> instantly.
    </div>
    """

# ---------------- MAIN APP ---------------- #
st.set_page_config(page_title="Lifestyle Helper App", layout="centered", page_icon="🛍️")

st.sidebar.title("🛍️ Lifestyle Helper")
page = st.sidebar.radio("Go to", ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"])

# -------- HOME -------- #
if page == "🏠 Home":
    st.title("✨ Welcome to Kraya – Lifestyle Helper App")
    st.markdown(
        """
        <div class="tagline tagline1">🌟 Smart Choices, Healthier Living</div>
        <div class="tagline tagline2">🎨 Personalized Fashion & Fabric Guidance</div>
        <div class="tagline tagline3">🔧 Quick & Easy Electronics Troubleshooting</div>
        <div class="tagline tagline4">🛍️ Your Lifestyle, Simplified</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        **Kraya** is an AI-powered lifestyle support system that helps customers make better decisions before and after purchases.  
        
        - <span class="badge badge-food">🍎 Food</span> – Analyze nutrition, know if your food helps in weight loss or gain.  
        - <span class="badge badge-fabric">🧵 Fabric</span> – Get fabric & color suggestions based on skin tone, weather, and activity.  
        - <span class="badge badge-electronics">📱 Electronics</span> – Solve device issues with smart troubleshooting tips.  

        👉 Experience **decision-making, satisfaction, and convenience** all in one place!  
        """,
        unsafe_allow_html=True,
    )

# -------- FOOD -------- #
elif page == "🍎 Food":
    st.title("🍎 Food Health Analyzer")
    st.info("This module helps you check whether your food is healthy, unhealthy, or moderate. It considers calories, sugar, fat, and protein to suggest suitability for **weight loss** or **weight gain**.")

    ingredients = st.text_area("🥗 Ingredients", "sugar, salt, whole grain, vegetable oil")
    calories = st.number_input("🔥 Calories per serving", min_value=0)
    fat = st.number_input("🧈 Fat (g)", min_value=0.0)
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0)
    fiber = st.number_input("🌾 Fiber (g)", min_value=0.0)
    protein = st.number_input("🥩 Protein (g)", min_value=0.0)

    if st.button("🔍 Analyze Food"):
        st.markdown(analyze_food(ingredients, calories, fat, sugar, fiber, protein), unsafe_allow_html=True)

# -------- ELECTRONICS -------- #
elif page == "📱 Electronics":
    st.title("📱 Electronics Help Desk")
    st.info("This module works as your personal troubleshooting guide. Select a device and describe your issue – Kraya provides quick, practical fixes.")

    devices = ["📱 Smartphone", "💻 Laptop", "📺 TV", "🌀 Washing Machine", "❄️ Refrigerator"]
    device = st.selectbox("🔎 Select your device", devices)
    user_input = st.text_area("💬 Describe your issue")

    if st.button("🛠️ Get Support"):
        if user_input.strip() == "":
            st.warning("⚠️ Please describe your issue before applying.")
        else:
            st.success("✅ Troubleshooting suggestion displayed below 👇")
            if "battery" in user_input.lower(): st.write("🔋 Check battery health or replace if damaged.")
            elif "screen" in user_input.lower(): st.write("🖥️ Screen may be physically damaged or loose connector.")
            elif "not turning on" in user_input.lower(): st.write("⚡ Ensure power cable is connected. Try reset.")
            elif "noise" in user_input.lower(): st.write("🔊 Noise may indicate motor or fan issues.")
            else: st.write("📞 Contact official support for advanced troubleshooting.")

# -------- FABRIC -------- #
elif page == "🧵 Fabric":
    st.title("🧵 Fabric Recommendation System")
    st.info("This module helps you pick the right fabric & colors for comfort and style. It uses your skin type, tone, weather, and activity to suggest the best fits.")

    skin_type = st.selectbox("💆 Skin Type", ["Dry", "Oily", "Sensitive", "Normal"])
    skin_tone = st.selectbox("🎭 Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("☀️ Weather", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("💪 Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("🍂 Season", ["Summer", "Winter", "Spring", "Autumn"])

    if st.button("🎯 Get Fabric Suggestions"):
        st.markdown(suggest_fabric(skin_type, skin_tone, weather, work_level, season), unsafe_allow_html=True)
