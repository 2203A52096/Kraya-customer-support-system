# interface.py
import streamlit as st
from sentence_transformers import SentenceTransformer, util
import numpy as np
import random
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
    import streamlit as st

    # Custom CSS for styling
    st.markdown("""
    <style>
        .banner {
            background-color: #FFF3E0;
            padding: 15px;
            border-radius: 15px;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            color: #FF6F00;
        }
        .info-box {
            background-color: #E1F5FE;
            padding: 12px;
            border-left: 6px solid #0288D1;
            border-radius: 8px;
            font-style: italic;
        }
        .result-box {
            padding: 15px;
            border-radius: 12px;
            margin-top: 15px;
            font-size: 18px;
        }
        .badge-healthy {
            color: #155724;
            background-color: #d4edda;
            padding: 6px 12px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
        }
        .badge-unhealthy {
            color: #721c24;
            background-color: #f8d7da;
            padding: 6px 12px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
        }
        .section-header {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            color: #FF5722;
        }
    </style>
    """, unsafe_allow_html=True)

    # Page Title & Banner
    st.title("🍎 Food Mood-o-Meter 3000")
    st.markdown('<div class="banner">🥗 Should You Buy It? Let\'s Find Out!</div>', unsafe_allow_html=True)

    # Info section about the page
    st.markdown('<div class="info-box">💡 Enter the details of the food product you want to buy. Choose your goal: weight loss, weight gain, or balanced. Our AI will help you decide if it\'s a match for your goal!</div>', unsafe_allow_html=True)

    # Food input section
    st.markdown('<p class="section-header">🕵️‍♂️ Product Details</p>', unsafe_allow_html=True)
    ingredients = st.text_area("📝 Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    label = st.selectbox("🎯 Your Goal", ["Weight Loss 🏃‍♀️", "Weight Gain 💪", "Balanced 😇"])
    calories = st.number_input("🔥 Calories per serving", min_value=0)
    protein = st.number_input("🍗 Protein (g)", min_value=0.0)
    carbs = st.number_input("🥖 Carbs (g)", min_value=0.0)
    fiber = st.number_input("🌿 Fiber (g)", min_value=0.0)
    fat = st.number_input("🥓 Fat (g)", min_value=0.0)
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0)

    # Analyze button
    if st.button("🔮 Check If You Should Buy"):
        if not food_model or not food_vectorizer:
            st.warning("⚠️ Food AI is sleeping. Please load the model!")
            return

        # Prepare features for ML prediction
        feature_text = f"{ingredients} {calories} {protein} {carbs} {fiber} {fat} {sugar}"
        X = food_vectorizer.transform([feature_text])
        pred_label = food_model.predict(X)[0]

        # Determine suitability
        if pred_label.lower() in label.lower():
            st.markdown(
                f'<div class="result-box"><span class="badge-healthy">✅ Suitable!</span> This product matches your <b>{label}</b> goal. Go ahead and buy it! 🛒😋</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="result-box"><span class="badge-unhealthy">❌ Not Suitable!</span> The AI predicts <b>{pred_label}</b>. Better skip this product if you want <b>{label}</b>. 🚫🥴</div>',
                unsafe_allow_html=True
            )

    # Tips Section
    st.markdown('<p class="section-header">💡 Pro Tips</p>', unsafe_allow_html=True)
    st.markdown("""
    - Enter all ingredients and nutrients for best prediction. 🕵️‍♀️  
    - Double-check calories and macros. AI is smart but not psychic. 🤖  
    - Use this as guidance for shopping, not a replacement for your nutritionist. 🥼  
    - If unsure, choose something green and leafy. 🥦💚  
    """)


# ---------------- FABRIC PAGE ---------------- #
def fabric_page(fabric_model, fabric_vectorizer):
    st.title("🧵 Fabric Recommendation System")
    st.markdown('<div class="banner">👗 Dress Smart, Feel Confident</div>', unsafe_allow_html=True)
    
    # Quick tips above inputs
    st.info("Get outfit recommendations tailored to your **skin, weather, work level, and season**.")
    st.info("💡 Tip: Enter the outfit you are planning to wear to check if it’s suitable.")
    st.info("💡 Note: Recommendations are based on patterns in the dataset and your selections.")

    # User inputs
    skin_tone = st.selectbox("🎨 Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("☀️ Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("💪 Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("🍂 Season", ["Summer", "Winter", "Spring", "Autumn"])
    recommended_outfit = st.text_input("👗 Enter Outfit You Plan to Wear", "Casual")

    if st.button("🎯 Check Outfit Suitability"):
        # Combine all features exactly like in training
        feature_text = f"{skin_tone} {weather} {work_level} {season} {recommended_outfit}"

        try:
            # Transform using the trained vectorizer
            X = fabric_vectorizer.transform([feature_text])
            # Predict recommended outfit
            pred_outfit = fabric_model.predict(X)[0]

            # Display predicted outfit
            st.markdown(
                f"""<div class="result-box">
                <span style='color:#5CB85C; font-weight:bold;'>✅ Predicted Outfit:</span> {pred_outfit}
                </div>""",
                unsafe_allow_html=True,
            )

            # Check if user input matches prediction
            if recommended_outfit.strip().lower() == pred_outfit.strip().lower():
                st.success(f"🎉 The outfit '{recommended_outfit}' is suitable to wear according to your selections!")
            else:
                st.warning(f"⚠️ The outfit '{recommended_outfit}' may not be the best match. Predicted recommendation: '{pred_outfit}'")

            # Detailed notes below prediction
            st.markdown("""
            <div style='background-color:#FFF4E6; border-left:6px solid #FF6F61; padding:10px; border-radius:20px;'>
            <h4>📝 Informative Notes:</h4>
            <ul>
            <li>The recommendation considers your skin tone, weather, work level, and season.</li>
            <li>High work intensity? Prefer breathable or moisture-wicking fabrics.</li>
            <li>Seasonal advice: cotton/linen for summer, wool/fleece for winter.</li>
            <li>These are guidelines based on dataset patterns; consider personal comfort and style.</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

            # Optional collapsible tips
            with st.expander("💡 Outfit Guidelines and Tips"):
                st.write("""
                - Outfits are suggested to match your skin tone, season, and activity level.
                - You can adjust the outfit based on personal style and occasion.
                - Re-check recommendations if your environment or activity changes.
                """)

        except ValueError:
            st.warning("⚠️ Input format does not match the trained model. Please check your selections.")

# ---------------- ELECTRONICS PAGE ---------------- #

def electronics_page(electronics_data, embed_model):
    st.title("📱 Electronics Help Desk")

    # ================== BANNER ==================
    st.markdown("""
    <div style="
        padding:20px; 
        text-align:center; 
        border-radius:15px; 
        background: linear-gradient(135deg, #e0f7fa, #b2ebf2);
        color:#00796b;
        font-size:20px;
        font-weight:600;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom:20px;
    ">
    ⚡ Quick Fixes for Smarter Living ⚡
    </div>
    """, unsafe_allow_html=True)

    # ================== INTRO CARD (PASTEL BLUE) ==================
    intro_card_style = """
        padding:40px; 
        border-radius:20px; 
        background:linear-gradient(135deg, #e3f2f9, #c7e8f6); 
        box-shadow: 2px 2px 20px rgba(0,0,0,0.08);
        font-size:16px;
        line-height:1.8;
        color:#37474f;
        margin-bottom:20px;
    """

    intro_html = f"""<div style="{intro_card_style}">
🎉 <b>Welcome to the Electronics Help Desk!</b> 🛠️<br><br>
Stressed out because your <b style="color:#0277bd;">gadget is acting up</b>? 
Don’t worry, you’re in <b style="color:#f57f17;">good hands</b> (or circuits 😎)!<br><br>
Here’s what I do:<br>
1️⃣ <b style="color:#00796b;">Step-by-step troubleshooting 🔧</b> – I break things down so even your grandma could fix it.<br>
2️⃣ <b style="color:#ff8f00;">Fun and quirky tips 😜</b> – Expect some tech humor along the way!<br>
3️⃣ <b style="color:#d32f2f;">Professional advice if needed 📞</b> – When it’s above our paygrade, I’ll tell you straight.<br><br>
Think of me as your <b style="color:#6a1b9a;">friendly, slightly sarcastic, tech-savvy buddy</b> 
who’s always ready to <b style="color:#fbc02d;">save the day ⚡</b>.<br>
So go ahead, spill the beans about your gadget drama – <b style="color:#00796b;">the weirder, the better 🤖💬!</b><br><br>
</div>"""

    st.markdown(intro_html, unsafe_allow_html=True)

    # ================== DEVICE SELECTION ==================
    devices = ["Smartphone 📱", "Laptop 💻", "TV 📺", "Washing Machine 🧺", "Refrigerator ❄️"]
    device = st.selectbox("🔧 Choose your device", devices)

    # ================== USER INPUT ==================
    user_input = st.text_area("✍️ Describe your issue (don’t hold back!)", height=120)

    # ================== GET SUPPORT ==================
    if st.button("🛠️ Get Support"):
        if not user_input.strip():
            st.warning("⚠️ Please describe your problem first! Your tech buddy can’t guess 😅")
            return

        if not electronics_data:
            st.warning("⚠️ Oops! Electronics data is missing. Can’t provide tips without it.")
            return

        # EMBEDDING THE USER QUERY
        user_emb = embed_model.encode(user_input, convert_to_tensor=True)

        best_match = None
        max_score = -1

        # FIND BEST MATCH
        for item in electronics_data:
            if item['device'] != device.split()[0]:
                continue

            texts_to_compare = [item['problem']] + item.get('example_queries', [])
            for text in texts_to_compare:
                desc_emb = embed_model.encode(text, convert_to_tensor=True)
                score = util.pytorch_cos_sim(user_emb, desc_emb).item()
                if score > max_score:
                    max_score = score
                    best_match = item

        # ================== SOLUTION CARD (PASTEL PINK) ==================
        solution_card_style = """
            padding:25px; 
            border-radius:15px; 
            background:linear-gradient(135deg, #fce4ec, #f8bbd0); 
            box-shadow: 2px 2px 15px rgba(0,0,0,0.08);
            font-size:16px;
            line-height:1.6;
            color:#37474f;
            margin-top:15px;
        """

        funny_headers = ["😎 Tech Tip:", "🛠️ Pro Hack:", "💡 Quick Fix:", "🤔 Try this:"]
        fallback_headers = ["😬 Hmmm…", "🤖 Brainstorming…", "⚡ Device acting up…", "📞 Call the experts!"]

        solution_html = f'<div style="{solution_card_style}">'
        if best_match and max_score > 0.6:
            steps = best_match["solution"].split(", ")
            solution_html += f'<h3 style="color:#d81b60;">{random.choice(funny_headers)}</h3>'
            for i, step in enumerate(steps, start=1):
                solution_html += f'<p style="margin:5px 0;">🔹 <b>Step {i}:</b> {step} ✅</p>'
            if 'tips' in best_match:
                solution_html += f'<p style="margin-top:10px; padding:10px; background:#fff3e0; border-radius:10px;">💡 <b>Extra Tips:</b> {best_match["tips"]}</p>'
        else:
            solution_html += f'<h3 style="color:#d32f2f;">{random.choice(fallback_headers)}</h3>'
            solution_html += "<p>I couldn’t find an exact fix 😅, but you can try these:</p>"
            solution_html += "<ul style='margin-left:20px;'>"
            solution_html += "<li>🔌 Double-check your cables and connections</li>"
            solution_html += "<li>🔄 Restart your device</li>"
            solution_html += "<li>💾 Update the software if possible</li>"
            solution_html += "<li>📞 Contact official support if all else fails</li>"
            solution_html += "</ul>"

        solution_html += "</div>"

        st.markdown(solution_html, unsafe_allow_html=True)


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
            - <span class="badge badge-electronics">📱 Electronics</span>: AI-powered troubleshooting.
            - <span class="badge badge-fabric">🧵 Fabric</span>: Personalized fabric recommendations.
            """,
            unsafe_allow_html=True
        )

    elif page == "🍎 Food":
        food_page(food_model, food_vectorizer)
    elif page == "🧵 Fabric":
        fabric_page(fabric_model, fabric_vectorizer)
    elif page == "📱 Electronics":
        embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        electronics_page(electronics_data, embed_model)
