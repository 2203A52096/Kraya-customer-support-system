import streamlit as st

# ---------------- STYLING ---------------- #
st.markdown(
    """
    <style>
    /* Sidebar background pastel color */
    [data-testid="stSidebar"] {
        background-color: #F7E9E9;  /* pastel pink */
        color: #5A3E36;
        border-radius: 20px;
    }
    /* Sidebar title */
    [data-testid="stSidebar"] > div:first-child {
        font-size: 24px;
        font-weight: 700;
        color: #9A5F6F;
    }
    /* Badge styles for keywords */
    .badge {
        display: inline-block;
        padding: 0.3em 0.7em;
        font-size: 0.8em;
        font-weight: 700;
        line-height: 1;
        color: white;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.8rem;
    }
    .badge-food {background-color: #FF6F61;}
    .badge-electronics {background-color: #6BAED6;}
    .badge-fabric {background-color: #8BC34A;}
    .badge-healthy {background-color: #4CAF50;}
    .badge-unhealthy {background-color: #F44336;}
    
    /* Banner with rounded cloud-like look */
    .banner {
        background-color: #FFF4E6;
        border-left: 6px solid #FF6F61;
        padding: 12px;
        margin: 10px 0px;
        border-radius: 25px;
        font-size: 16px;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.05);
    }
    /* Rounded box for results */
    .result-box {
        background: #ffffffdd;
        border-radius: 25px;
        padding: 15px 20px;
        margin: 15px 0;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- UTILITY FUNCTIONS ---------------- #
def analyze_food(ingredients, calories, fat, sugar, fiber, protein):
    ing_list = [i.strip().lower() for i in ingredients.split(",")]

    unhealthy_ingredients = ["sugar", "corn syrup", "hydrogenated oil", "trans fat", "artificial"]
    healthy_tags, unhealthy_tags = [], []

    for ing in ing_list:
        if any(bad in ing for bad in unhealthy_ingredients):
            unhealthy_tags.append(ing)
        elif "whole" in ing or "vegetable" in ing or "fiber" in ing:
            healthy_tags.append(ing)

    if len(unhealthy_tags) > 2 or sugar > 15 or fat > 20:
        return """
        <div class="result-box">
        <span class="badge badge-unhealthy">❌ Unhealthy</span>: High sugar/fat content. May lead to <b>weight gain</b> and health risks.
        </div>
        """
    elif calories < 100 and fat < 5 and sugar < 5:
        return """
        <div class="result-box">
        <span class="badge badge-healthy">✅ Healthy</span>: Suitable for <b>weight loss</b>, low calories & fat.
        </div>
        """
    elif calories > 300 and protein > 10:
        return """
        <div class="result-box">
        <span class="badge badge-healthy">✅ Healthy</span>: Good for <b>weight gain</b> with high protein & energy.
        </div>
        """
    else:
        return """
        <div class="result-box">
        <span style='color: #FFA500; font-weight:bold;'>⚠️ Moderately healthy</span>. Balanced but watch certain ingredients.
        </div>
        """

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

    avoid_fabrics = list(set(avoid_fabrics))
    preferred_fabrics = list(set(preferred_fabrics))

    return f"""
    <div class="result-box">
    <span style='color:#D9534F; font-weight:bold;'>❌ Avoid Fabrics:</span> {", ".join(avoid_fabrics)}<br><br>
    <span style='color:#5CB85C; font-weight:bold;'>✅ Recommended Fabrics:</span> {", ".join(preferred_fabrics)}<br><br>
    <span style='color:#0275D8; font-weight:bold;'>🎨 Suggested Colors:</span> {", ".join(color_suggestions)}
    </div>
    """

# ---------------- MAIN APP ---------------- #
st.set_page_config(page_title="Lifestyle Helper App", layout="centered")

st.sidebar.title("🛍️ Lifestyle Helper")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"],
)

# HOME PAGE
if page == "🏠 Home":
    st.title("🏠 Welcome to Kraya")
    st.markdown('<div class="banner">✨ Smart Choices, Happy Living ✨</div>', unsafe_allow_html=True)
    st.markdown(
        """
        Kraya is your **personal customer support system** that makes shopping and usage easier:  

        - <span class="badge badge-food">🍎 Food</span>: Check if food is **healthy**, for **weight loss/gain**.  
        - <span class="badge badge-electronics">📱 Electronics</span>: Troubleshoot your **devices** quickly.  
        - <span class="badge badge-fabric">🧵 Fabric</span>: Get fabric and **color suggestions** for your skin & season.  

        💡 Our goal: Enhance **decision-making**, boost **convenience**, and improve **satisfaction**.  
        """,
        unsafe_allow_html=True,
    )

# FOOD PAGE
elif page == "🍎 Food":
    st.title("🍎 Food Health Analyzer")
    st.markdown('<div class="banner">🥗 Eat Smart, Live Better</div>', unsafe_allow_html=True)
    st.info("Enter your food details and find out if it’s suitable for **weight loss, weight gain, or balanced nutrition**.")

    ingredients = st.text_area("🧾 Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    calories = st.number_input("🔥 Calories per serving", min_value=0)
    fat = st.number_input("🥓 Total Fat (g)", min_value=0.0)
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0)
    fiber = st.number_input("🌿 Dietary Fiber (g)", min_value=0.0)
    protein = st.number_input("🍗 Protein (g)", min_value=0.0)

    if st.button("🔍 Analyze Food"):
        result = analyze_food(ingredients, calories, fat, sugar, fiber, protein)
        st.markdown(result, unsafe_allow_html=True)

# ELECTRONICS PAGE
elif page == "📱 Electronics":
    st.title("📱 Electronics Help Desk")
    st.markdown('<div class="banner">⚡ Quick Fixes for Smarter Living ⚡</div>', unsafe_allow_html=True)
    st.info("Describe your problem, and Kraya will give **troubleshooting tips** for your electronic devices.")

    devices = ["Smartphone 📱", "Laptop 💻", "TV 📺", "Washing Machine 🧺", "Refrigerator ❄️"]
    device = st.selectbox("🔧 Select your device", devices)

    user_input = st.text_area("✍️ Describe your issue")

    if st.button("🛠️ Get Support"):
        if user_input.strip() == "":
            st.warning("⚠️ Please describe your issue before proceeding.")
        else:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### **🔧 Suggested Fix:**", unsafe_allow_html=True)
            user_input_lower = user_input.lower()
            if "battery" in user_input_lower:
                st.write("🔋 Battery not holding charge? Try replacing or checking for swelling.")
            elif "screen" in user_input_lower:
                st.write("🖥️ Screen flicker/cracks may mean loose connectors or damage.")
            elif "not turning on" in user_input_lower:
                st.write("⚡ Ensure cables are connected. Try a hard reset.")
            elif "noise" in user_input_lower:
                st.write("🔊 Strange noises often mean motor or loose part issues.")
            else:
                st.write("📞 Contact official service for advanced troubleshooting.")
            st.markdown('</div>', unsafe_allow_html=True)

# FABRIC PAGE
elif page == "🧵 Fabric":
    st.title("🧵 Fabric Recommendation System")
    st.markdown('<div class="banner">👗 Dress Smart, Feel Confident</div>', unsafe_allow_html=True)
    st.info("Get fabric and **color suggestions** tailored to your **skin, weather, work level, and season**.")

    skin_type = st.selectbox("👩 Skin Type", ["Dry", "Oily", "Sensitive", "Normal"])
    skin_tone = st.selectbox("🎨 Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("☀️ Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("💪 Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("🍂 Season", ["Summer", "Winter", "Spring", "Autumn"])

    if st.button("🎯 Get Fabric Suggestions"):
        result = suggest_fabric(skin_type, skin_tone, weather, work_level, season)
        st.markdown(result, unsafe_allow_html=True)
