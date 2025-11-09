# interface.py
import streamlit as st

# ---------------- STYLING ---------------- #
def add_styles():
    st.markdown(
        """
        <style>
        /* Sidebar background pastel color */
        [data-testid="stSidebar"] { 
            background-color: #F7E9E9; 
            color: #5A3E36; 
            border-radius: 20px; 
        }
        [data-testid="stSidebar"] > div:first-child { 
            font-size: 24px; font-weight: 700; color: #9A5F6F; 
        }
        .badge { display: inline-block; padding: 0.3em 0.7em; font-size: 0.8em; font-weight: 700; line-height: 1; color: white; text-align: center; white-space: nowrap; vertical-align: baseline; border-radius: 0.8rem; }
        .badge-food {background-color: #FF6F61;}
        .badge-electronics {background-color: #6BAED6;}
        .badge-fabric {background-color: #8BC34A;}
        .badge-healthy {background-color: #4CAF50;}
        .badge-unhealthy {background-color: #F44336;}
        .banner { background-color: #FFF4E6; border-left: 6px solid #FF6F61; padding: 12px; margin: 10px 0px; border-radius: 25px; font-size: 16px; box-shadow: 2px 4px 10px rgba(0,0,0,0.05); }
        .result-box { background: #ffffffdd; border-radius: 25px; padding: 15px 20px; margin: 15px 0; box-shadow: 0px 4px 15px rgba(0,0,0,0.08); }
        </style>
        """, unsafe_allow_html=True
    )

# ---------------- FOOD PAGE ---------------- #
def food_page(food_model, food_vectorizer):
    st.title("🍎 Food Health Analyzer")
    st.markdown('<div class="banner">🥗 Eat Smart, Live Better</div>', unsafe_allow_html=True)
    st.info("Enter your food details and find out if it’s suitable for weight loss, weight gain, or balanced nutrition.")

    ingredients = st.text_area("🧾 Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    calories = st.number_input("🔥 Calories per serving", min_value=0)
    fat = st.number_input("🥓 Total Fat (g)", min_value=0.0)
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0)
    fiber = st.number_input("🌿 Dietary Fiber (g)", min_value=0.0)
    protein = st.number_input("🍗 Protein (g)", min_value=0.0)

    if st.button("🔍 Analyze Food"):
        if not food_model or not food_vectorizer:
            st.warning("⚠️ Food ML model not loaded.")
            return

        # Convert ingredients to ML-ready features
        X = food_vectorizer.transform([ingredients])
        pred = food_model.predict(X)[0]

        # Display ML prediction
        if pred == "Unhealthy":
            st.markdown('<div class="result-box"><span class="badge badge-unhealthy">❌ Unhealthy</span>: Avoid this food.</div>', unsafe_allow_html=True)
        elif pred == "Healthy_WeightLoss":
            st.markdown('<div class="result-box"><span class="badge badge-healthy">✅ Healthy</span>: Good for weight loss.</div>', unsafe_allow_html=True)
        elif pred == "Healthy_WeightGain":
            st.markdown('<div class="result-box"><span class="badge badge-healthy">✅ Healthy</span>: Good for weight gain.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-box"><span style="color: #FFA500; font-weight:bold;">⚠️ Moderately healthy</span>: Balanced food.</div>', unsafe_allow_html=True)


# ---------------- FABRIC PAGE ---------------- #
def fabric_page(fabric_model, fabric_vectorizer):
    st.title("🧵 Fabric Recommendation System")
    st.markdown('<div class="banner">👗 Dress Smart, Feel Confident</div>', unsafe_allow_html=True)
    st.info("Get fabric and color suggestions tailored to your skin, weather, work level, and season.")

    skin_type = st.selectbox("👩 Skin Type", ["Dry", "Oily", "Sensitive", "Normal"])
    skin_tone = st.selectbox("🎨 Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("☀️ Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("💪 Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("🍂 Season", ["Summer", "Winter", "Spring", "Autumn"])

    if st.button("🎯 Get Fabric Suggestions"):
        if not fabric_model or not fabric_vectorizer:
            st.warning("⚠️ Fabric ML model not loaded.")
            return

        # Combine inputs for ML
        input_text = f"{skin_type}, {skin_tone}, {weather}, {work_level}, {season}"
        X = fabric_vectorizer.transform([input_text])
        pred = fabric_model.predict(X)[0]

        st.markdown(f'<div class="result-box"><span class="badge badge-fabric">🧵 Recommended Fabric:</span> {pred}</div>', unsafe_allow_html=True)


# ---------------- ELECTRONICS PAGE ---------------- #
def electronics_page(electronics_data):
    st.title("📱 Electronics Help Desk")
    st.markdown('<div class="banner">⚡ Quick Fixes for Smarter Living ⚡</div>', unsafe_allow_html=True)
    st.info("Describe your problem, and get troubleshooting tips.")

    devices = ["Smartphone 📱", "Laptop 💻", "TV 📺", "Washing Machine 🧺", "Refrigerator ❄️"]
    device = st.selectbox("🔧 Select your device", devices)
    user_input = st.text_area("✍️ Describe your issue")

    if st.button("🛠️ Get Support"):
        if not electronics_data:
            st.warning("⚠️ Electronics data not loaded.")
            return
        user_input_lower = user_input.lower()
        response = "📞 Contact official service for advanced troubleshooting."
        for keyword, tip in electronics_data.items():
            if keyword in user_input_lower:
                response = tip
                break
        st.markdown(f'<div class="result-box">{response}</div>', unsafe_allow_html=True)


# ---------------- MAIN UI ---------------- #
def show_ui(food_model, food_vectorizer, fabric_model, fabric_vectorizer, electronics_data):
    add_styles()
    st.sidebar.title("🛍️ Lifestyle Helper")
    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"]
    )

    # HOME PAGE
    if page == "🏠 Home":
        st.title("🏠 Welcome to Kraya")
        st.markdown('<div class="banner">✨ Smart Choices, Happy Living ✨</div>', unsafe_allow_html=True)
        st.markdown(
            """
            Kraya is your **personal customer support system**:
            - <span class="badge badge-food">🍎 Food</span>: ML-powered food health analyzer.
            - <span class="badge badge-electronics">📱 Electronics</span>: Troubleshoot your devices.
            - <span class="badge badge-fabric">🧵 Fabric</span>: Personalized fabric recommendations.
            """,
            unsafe_allow_html=True
        )

    elif page == "🍎 Food":
        food_page(food_model, food_vectorizer)
    elif page == "📱 Electronics":
        electronics_page(electronics_data)
    elif page == "🧵 Fabric":
        fabric_page(fabric_model, fabric_vectorizer)
