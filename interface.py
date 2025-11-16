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
    import time

    # ================== CUSTOM CSS ==================
    st.markdown("""
    <style>
        .banner {
            background: linear-gradient(135deg, #fff0f5, #ffe4e1);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            color: #d32f2f;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.08);
            margin-bottom: 15px;
        }
        .info-box {
            background: linear-gradient(135deg, #e0f7fa, #b2ebf2);
            padding: 18px;
            border-left: 6px solid #0288D1;
            border-radius: 12px;
            font-style: italic;
            margin-bottom: 15px;
            line-height: 1.5;
        }
        .result-box {
            padding: 20px;
            border-radius: 15px;
            margin-top: 15px;
            font-size: 18px;
            line-height:1.6;
            box-shadow: 1px 1px 8px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        .badge-healthy {
            color: #155724;
            background-color: #d4edda;
            padding: 8px 14px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 16px;
        }
        .badge-unhealthy {
            color: #721c24;
            background-color: #f8d7da;
            padding: 8px 14px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 16px;
        }
        .section-header {
            font-size: 22px;
            font-weight: bold;
            margin-top: 20px;
            color: #FF5722;
        }
    </style>
    """, unsafe_allow_html=True)

    # ================== PAGE TITLE & BANNER ==================
    st.title("🍎 Foody Buddy 🤗🛒")
    st.markdown("""<div class="banner">🥗 Snack Detective Activated! Let’s Check if It’s Buddy-Approved! 🎉</div>""", unsafe_allow_html=True)

    # ================== INFO CARD ==================
    st.markdown("""
    <div class="info-box">
        Hey hey hey! 😄 I’m your Foody Buddy! 🤗<br>
        I will help you figure out if that snack you’re eyeing is your new BFF 🍕🍩<br>
        I’m good at numbers (calories, protein, carbs… you name it!) and amazing at taste-checking with my imaginary taste buds 😋<br>
        Spill the beans (and sugar, and chocolate, and maybe a veggie or two) and I’ll tell you if it’s going to make your day awesome or… mildly hilarious 😜<br>
        Sit back, grab a snack for yourself while we analyze your snack. You deserve it! 🥳
    </div>
    """, unsafe_allow_html=True)

    # ================== USER INPUT ==================
    st.markdown('<p class="section-header">🕵️‍♂️ Snack Confessions Time!</p>', unsafe_allow_html=True)
    ingredients = st.text_area("📝 Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    label = st.selectbox("🎯 Your Goal", ["Weight Loss 🏃‍♀️", "Weight Gain 💪", "Balanced 😇"])
    calories = st.number_input("🔥 Calories per serving", min_value=0)
    protein = st.number_input("🍗 Protein (g)", min_value=0.0)
    carbs = st.number_input("🥖 Carbs (g)", min_value=0.0)
    fiber = st.number_input("🌿 Fiber (g)", min_value=0.0)
    fat = st.number_input("🥓 Fat (g)", min_value=0.0)
    sugar_val = st.number_input("🍬 Sugar (g)", min_value=0.0)

    # ================== ANALYZE BUTTON ==================
    if st.button("🔮 Foody Buddy, Analyze!"):
        if not food_model or not food_vectorizer:
            st.warning("⚠️ Oops! My buddy powers are napping… please load the model! 😴")
            return

        if not ingredients.strip():
            st.warning("⚠️ I can’t read empty snacks! Enter some ingredients, buddy! 🤓")
            return

        # ===== ML Prediction: ingredients + numeric features =====
        feature_text = f"{ingredients} {calories} {protein} {carbs} {fiber} {fat} {sugar_val}"
        X = food_vectorizer.transform([feature_text])
        pred_label = food_model.predict(X)[0]

        # ===== Funny Buddy Messages =====
        first_ing = ingredients.split(',')[0].strip()
        if pred_label.lower() in label.lower():
            result_color = "#d4edda"
            badge_class = "badge-healthy"
            emoji_sequence = ["🥳", "🎉", "🛒", "🍕"]
            message = (
                f"🎊 Woohoo! Looks like {first_ing} is giving a big high-five to your <b>{label}</b> goal! ✋😄<br>"
                f"Your Foody Buddy approves this snack 100%! 🏆<br>"
                f"Imagine confetti raining down and little cartoon snacks dancing around your plate 💃🍩🍪<br>"
                f"Calories, protein, carbs? Nailed it! Even your macros are cheering! 🎯💪<br>"
                f"Go grab it and enjoy like the snack superstar you are! 😋🤗"
            )
        else:
            result_color = "#f8d7da"
            badge_class = "badge-unhealthy"
            emoji_sequence = ["😅", "🤔", "🙈", "🍩"]
            message = (
                f"🤔 Hmmm… {first_ing} might be a little tricky for your <b>{label}</b> goal.<br>"
                f"But don’t worry! Your Foody Buddy isn’t here to judge, just to giggle along with you 😄<br>"
                f"Maybe it’s slightly off-target, but hey — calories, sugar, and fun levels all balanced-ish! ⚖️🍬<br>"
                f"Pro tip: sometimes a snack can be both naughty and nice — like a cookie wearing sunglasses 😎🍪<br>"
                f"Eat if you must, laugh a lot, and tell me how it goes! 🎉🤗"
            )

        # ===== Display animated verdict =====
        result_container = st.empty()
        for emoji in emoji_sequence:
            result_container.markdown(f"""
            <div class="result-box" style="background:{result_color};">
                <span class="{badge_class}">{emoji} Buddy Verdict!</span><br> {message}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.3)

    # ================== PRO TIPS CARD ==================
    st.markdown('<p class="section-header">💡 Buddy Tips for Snacking Fun</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #fff8e1, #ffe0b2); border-left: 6px solid #ff9800;">
        😄 Snack like a champion! Here’s what your buddy suggests:<br>
        - Always tell me all the ingredients. Secrets make me giggle 🤫🍫<br>
        - Veggies are friends too! Mix them with your snack for extra fun 🥦🎉<br>
        - Protein and fiber make you strong and keep your tummy happy 💪🍗<br>
        - Too many calories? No worries — we’ll pretend we’re counting imaginary points 🏅😂<br>
        - Sugar is sweet, but laughter is sweeter! Don’t forget to smile while munching 🍭😄<br>
        - Remember: I’m your buddy, not a diet guru. Eat, laugh, snack, repeat! 🎈🍕🤗<br>
        - Bonus tip: imagine tiny dancing snacks cheering you on — it works, trust me! 💃🍩🎊
    </div>
    """, unsafe_allow_html=True)


# ---------------- FABRIC PAGE ---------------- #
def fabric_page(fabric_model_dict):
    import streamlit as st
    import pandas as pd
    import time

    st.title("🧵 Styling Buddy 🤗✨")

    # ================== BANNER ==================
    st.markdown("""
    <div style="
        padding:20px;
        text-align:center;
        border-radius:15px;
        background: linear-gradient(135deg, #d0f0c0, #a0e0a0);
        color:#2e7d32;
        font-size:20px;
        font-weight:600;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom:15px;
    ">
        👗 Dress Smart, Feel Confident – Your Fabric Buddy is Here! 🎉
    </div>
    """, unsafe_allow_html=True)

    # ================== QUICK INFO ==================
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #e0f7fa, #b2ebf2);
        border-left:6px solid #0288D1;
        padding:18px;
        border-radius:12px;
        font-style:italic;
        line-height:1.6;
        margin-bottom:15px;
    ">
        Hey fashionista! 😎 I’m your Fabric Buddy 🤗<br>
        Tell me your <b>Skin Tone, Season, Weather, and Work Level</b> and I’ll suggest the perfect fabric group for you!<br>
        Sometimes I’ll even spill the exact fabrics you can wear. Fun + style = guaranteed! ✨👕<br>
        Ready to see your buddy’s recommendation? Let’s goooo! 💃🎈
    </div>
    """, unsafe_allow_html=True)

    # ================== USER INPUTS ==================
    skin_tone = st.selectbox("🎨 Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("☀️ Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("💪 Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("🍂 Season", ["Summer", "Winter", "Spring", "Autumn"])
    planned_outfit = st.text_input("👗 Enter Outfit You Plan to Wear (optional, for fun!)", "Casual")

    # ================== Fabric Group Mapping ==================
    fabric_map = {
        "Breathable": ["Cotton", "Linen", "Rayon"],
        "Synthetic": ["Polyester", "Nylon"],
        "Warm": ["Wool", "Velvet"],
        "LightSoft": ["Satin", "Silk", "Chiffon", "Georgette"],
        "Denim": ["Denim"]
    }

    # ================== Encodings ==================
    encode_skin = {"Fair": "Fair", "Medium": "Medium", "Dark": "Dark"}
    encode_weather = {"Hot": "Hot", "Cold": "Cold", "Humid": "Humid", "Dry": "Dry"}
    encode_work = {"High": "High", "Medium": "Medium", "Low": "Low"}
    encode_season = {"Summer": "Summer", "Winter": "Winter", "Spring": "Spring", "Autumn": "Autumn"}

    # ================== BUTTON ==================
    if st.button("🎯 Check Fabric Recommendation"):
        if fabric_model_dict is None:
            st.error("⚠️ My fabric senses are offline… load the model first 😢")
            return

        try:
            # Prepare input for prediction
            X_input = pd.DataFrame([[
                encode_season[season],
                encode_skin[skin_tone],
                encode_weather[weather],
                encode_work[work_level]
            ]], columns=["Season", "SkinTone", "Weather", "WorkLevel"])

            X_encoded = fabric_model_dict["encoder"].transform(X_input)
            pred_encoded = fabric_model_dict["model"].predict(X_encoded)[0]
            pred_group = fabric_model_dict["label"].inverse_transform([pred_encoded])[0]

            # Get actual fabrics in the group
            fabrics_in_group = ", ".join(fabric_map[pred_group])

            # ======= FUNNY BUDDY RESULT =======
            result_style = """
                padding:25px;
                border-radius:15px;
                background: linear-gradient(135deg, #ffe0b2, #ffcc80);
                box-shadow: 2px 2px 12px rgba(0,0,0,0.08);
                font-size:16px;
                line-height:1.6;
                color:#e65100;
                margin-top:15px;
            """

            message = (
                f"🎉 Your Fabric Buddy says: <b>{pred_group}</b>! 🧵💫<br>"
                f"That means you can rock these fabrics: <b>{fabrics_in_group}</b> 😎<br>"
                f"Planned outfit: '<i>{planned_outfit}</i>' looks fun, but using fabrics from this group will make you super comfy & stylish! 🌟<br>"
                f"Remember, your buddy only wants your wardrobe to shine! ✨💃🕺<br>"
                f"Go ahead, hug your fabrics, strut like a superstar, and flaunt your vibe! 💖👕👗"
            )

            st.markdown(f'<div style="{result_style}">{message}</div>', unsafe_allow_html=True)

            # ======= FABRIC BUDDY TIPS =======
            tips_style = """
                background-color:#f3e5f5;
                border-left:6px solid #ab47bc;
                padding:15px;
                border-radius:15px;
                margin-top:10px;
                line-height:1.6;
            """
            st.markdown(f"""
            <div style="{tips_style}">
                💡 <b>Fabric Buddy Tips:</b><br>
                - Always pick fabrics suited for your weather: breathable for hot 🌞, warm for cold ❄️.<br>
                - Skin tone + fabric color combo = instant style points 🎨💯<br>
                - LightSoft fabrics are like clouds on your skin – silky comfort ☁️✨<br>
                - Denim & Synthetic fabrics = durable & casual vibes 😎<br>
                - Confidence is your best accessory, buddy! Walk, twirl, snack on confidence 💃🕺<br>
                - Optional: Your planned outfit is always fun, but fabrics make it fabulous! 😄
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Oopsie! Something went wrong during prediction: {e} 😅")


# ---------------- ELECTRONICS PAGE ---------------- #

def electronics_page(electronics_data, embed_model):
    st.title("📱 Electronics fixing buddy")

    # ================== BANNER (Pastel Purple Gradient) ==================
    st.markdown("""
    <div style="
        padding:20px; 
        text-align:center; 
        border-radius:15px; 
        background: linear-gradient(135deg, #e1bee7, #ce93d8);
        color:#6a1b9a;
        font-size:20px;
        font-weight:600;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom:20px;
    ">
    ⚡ Quick Fixes for Smarter Living ⚡
    </div>
    """, unsafe_allow_html=True)

    # ================== INTRO CARD (Pastel Blue) ==================
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
            clean_device = device.split()[0].strip()
            if item['device'].lower() != clean_device.lower():
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
def show_ui(food_model, food_vectorizer, fabric_model, electronics_data):

    # Apply global styles
    add_styles()

    # Sidebar navigation
    st.sidebar.title("🛍️ Lifestyle Helper")
    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"]
    )

    # ---------------- HOME PAGE ---------------- #
    if page == "🏠 Home":
        # Existing banner and intro content
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

        # ---------------- NEW INFORMATIVE PASTEL CARD ---------------- #
        st.markdown("""
        <div style="
            padding:20px;
            border-radius:15px;
            background: linear-gradient(135deg, #e1f5fe, #b3e5fc); /* soft pastel blue */
            color:#0d47a1;
            font-size:16px;
            line-height:1.6;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.08);
            margin-top:15px;
        ">
            💡 <b>Pro Tips & FAQs:</b><br><br>
            1️⃣ Navigate using the sidebar to quickly access Food, Electronics, or Fabric pages.<br>
            2️⃣ Fill in all inputs for more accurate AI suggestions. Partial info may reduce prediction quality.<br>
            3️⃣ For Food: enter ingredients, nutrients, and your goal for a quick recommendation.<br>
            4️⃣ For Electronics: describe your gadget issue in detail to get step-by-step troubleshooting.<br>
            5️⃣ For Fabric: provide skin tone, weather, season, and activity level to get outfit advice.<br>
            6️⃣ Remember: AI provides guidance based on patterns in the dataset. Use your own judgment too!<br>
            7️⃣ Have fun! Kraya loves a little humor 😎 while helping you make smart choices.<br><br>
            📌 Keep checking back! The system is continuously learning to give better suggestions.
        </div>
        """, unsafe_allow_html=True)

    # ---------------- FOOD PAGE ---------------- #
    elif page == "🍎 Food":
        food_page(food_model, food_vectorizer)

    # ---------------- FABRIC PAGE ---------------- #
    elif page == "🧵 Fabric":
        fabric_page(fabric_model)

    # ---------------- ELECTRONICS PAGE ---------------- #
    elif page == "📱 Electronics":
        embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        electronics_page(electronics_data, embed_model)
