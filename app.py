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

    /* Sidebar title */
    [data-testid="stSidebar"] > div:first-child {
        font-size: 24px;
        font-weight: 700;
        color: #9A5F6F;
    }

    /* Badge styles */
    .badge {
        display: inline-block;
        padding: 0.4em 0.7em;
        font-size: 0.8em;
        font-weight: 700;
        line-height: 1;
        color: white;
        text-align: center;
        border-radius: 0.4rem;
        margin-right: 5px;
    }
    .badge-food {background-color: #FF6F61;}
    .badge-electronics {background-color: #6BAED6;}
    .badge-fabric {background-color: #8BC34A;}
    .badge-healthy {background-color: #4CAF50;}
    .badge-unhealthy {background-color: #F44336;}

    /* Result container */
    .result-box {
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        font-size: 16px;
        font-weight: 500;
    }
    .result-good {background-color: #E8F5E9; color:#2E7D32;}
    .result-bad {background-color: #FFEBEE; color:#C62828;}
    .result-warning {background-color: #FFF8E1; color:#F9A825;}
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
        return f"""
        <div class="result-box result-bad">
        ❌ <span class="badge badge-unhealthy">Unhealthy</span><br>
        High sugar/fat content. May lead to weight gain, heart issues.
        </div>
        """
    elif calories < 100 and fat < 5 and sugar < 5:
        return f"""
        <div class="result-box result-good">
        ✅ <span class="badge badge-healthy">Healthy</span><br>
        Suitable for <strong>weight loss</strong>. Low calories & balanced.
        </div>
        """
    elif calories > 300 and protein > 10:
        return f"""
        <div class="result-box result-good">
        💪 <span class="badge badge-healthy">Healthy</span><br>
        Suitable for <strong>weight gain</strong> (high protein/calories).
        </div>
        """
    else:
        return f"""
        <div class="result-box result-warning">
        ⚠️ Moderately Healthy.<br> Watch out for specific ingredients.
        </div>
        """

def suggest_fabric(skin_type, skin_tone, weather, work_level, season):
    avoid_fabrics, preferred_fabrics, color_suggestions = [], [], []

    if skin_type == "Sensitive":
        avoid_fabrics += ["Polyester", "Nylon"]; preferred_fabrics += ["Cotton", "Bamboo"]
    elif skin_type == "Oily":
        avoid_fabrics += ["Silk"]; preferred_fabrics += ["Linen", "Cotton"]
    else:
        preferred_fabrics += ["Cotton", "Linen"]

    if weather == "Hot":
        avoid_fabrics += ["Wool"]; preferred_fabrics += ["Cotton", "Linen"]
    elif weather == "Cold":
        preferred_fabrics += ["Wool", "Fleece"]
    elif weather == "Humid":
        avoid_fabrics += ["Polyester"]; preferred_fabrics += ["Bamboo", "Cotton"]

    if work_level == "High": preferred_fabrics += ["Moisture-wicking blends"]
    if season == "Winter": preferred_fabrics += ["Wool", "Fleece"]
    elif season == "Summer": preferred_fabrics += ["Cotton", "Linen"]

    if skin_tone == "Fair": color_suggestions = ["Soft pastels 🌸", "Cool blues 💙", "Lavender 💜"]
    elif skin_tone == "Medium": color_suggestions = ["Earth tones 🌍", "Olive 🫒", "Warm reds ❤️"]
    else: color_suggestions = ["Bright colors 🌈", "Bold yellows 💛", "Vibrant blues 💙"]

    avoid_fabrics, preferred_fabrics = list(set(avoid_fabrics)), list(set(preferred_fabrics))

    return f"""
    <div class="result-box result-good">
    ❌ <b>Avoid Fabrics:</b> {", ".join(avoid_fabrics)}<br><br>
    ✅ <b>Recommended Fabrics:</b> {", ".join(preferred_fabrics)}<br><br>
    🎨 <b>Best Colors for You:</b> {", ".join(color_suggestions)}
    </div>
    """

# ---------------- MAIN APP ---------------- #
st.set_page_config(page_title="Lifestyle Helper App", layout="centered", page_icon="🛍️")

st.sidebar.title("🛍️ Lifestyle Helper")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"],
)

# -------- HOME -------- #
if page == "🏠 Home":
    st.title("✨ Welcome to Kraya")
    st.markdown(
        """
        Explore lifestyle assistance in 3 main areas:
        
        - <span class="badge badge-food">🍎 Food</span> – Check if food is healthy  
        - <span class="badge badge-electronics">📱 Electronics</span> – Troubleshooting assistant  
        - <span class="badge badge-fabric">🧵 Fabric</span> – Style & fabric recommendations  
        """,
        unsafe_allow_html=True,
    )

# -------- FOOD -------- #
elif page == "🍎 Food":
    st.title("🍎 Food Health Analyzer")
    st.subheader("📝 Enter Food Details")

    ingredients = st.text_area("🥗 Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    calories = st.number_input("🔥 Calories per serving", min_value=0)
    fat = st.number_input("🧈 Total Fat (g)", min_value=0.0)
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0)
    fiber = st.number_input("🌾 Dietary Fiber (g)", min_value=0.0)
    protein = st.number_input("🥩 Protein (g)", min_value=0.0)

    if st.button("🔍 Analyze Food"):
        result = analyze_food(ingredients, calories, fat, sugar, fiber, protein)
        st.markdown(result, unsafe_allow_html=True)

# -------- ELECTRONICS -------- #
elif page == "📱 Electronics":
    st.title("📱 Electronics Help Desk")
    st.subheader("🔧 Troubleshoot your device")

    devices = ["📱 Smartphone", "💻 Laptop", "📺 TV", "🌀 Washing Machine", "❄️ Refrigerator"]
    device = st.selectbox("🔎 Select your device", devices)

    user_input = st.text_area("💬 Describe your issue")
    if st.button("🛠️ Get Support"):
        if user_input.strip() == "":
            st.warning("⚠️ Please describe your issue before applying.")
        else:
            st.markdown("### 🔧 Suggested Fix")
            ui = user_input.lower()
            if "battery" in ui: st.success("🔋 Check battery health. Replace if swollen/not holding charge.")
            elif "screen" in ui: st.info("🖥️ Possible screen damage or loose connectors.")
            elif "not turning on" in ui: st.error("⚡ Check power cable. Try a hard reset.")
            elif "noise" in ui: st.warning("🔊 Noise may indicate motor or fan issues.")
            else: st.write("📞 Please contact customer support for detailed troubleshooting.")

# -------- FABRIC -------- #
elif page == "🧵 Fabric":
    st.title("🧵 Fabric Recommendation System")
    st.subheader("👤 Enter Your Profile")

    skin_type = st.selectbox("💆 Skin Type", ["Dry", "Oily", "Sensitive", "Normal"])
    skin_tone = st.selectbox("🎭 Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("☀️ Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("💪 Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("🍂 Season", ["Summer", "Winter", "Spring", "Autumn"])

    if st.button("🎯 Get Fabric Suggestions"):
        result = suggest_fabric(skin_type, skin_tone, weather, work_level, season)
        st.markdown(result, unsafe_allow_html=True)
