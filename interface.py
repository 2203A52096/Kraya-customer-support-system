# interface.py
import streamlit as st
from sentence_transformers import SentenceTransformer, util
import numpy as np
import random
import pandas as pd
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
        You can also pick a fabric you are thinking of wearing — I’ll give my buddy verdict! 💃🕺
    </div>
    """, unsafe_allow_html=True)

    # ================== USER INPUTS ==================
    skin_tone = st.selectbox("🎨 Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("☀️ Weather Condition", ["Hot", "Cold", "Humid", "Dry"])
    work_level = st.selectbox("💪 Work Level", ["High", "Medium", "Low"])
    season = st.selectbox("🍂 Season", ["Summer", "Winter", "Spring", "Autumn"])

    # Fabric mapping
    fabric_map = {
        "Breathable": ["Cotton", "Linen", "Rayon"],
        "Synthetic": ["Polyester", "Nylon"],
        "Warm": ["Wool", "Velvet"],
        "LightSoft": ["Satin", "Silk", "Chiffon", "Georgette"],
        "Denim": ["Denim"]
    }

    # Flatten list of fabrics for dropdown
    all_fabrics = []
    for fabrics in fabric_map.values():
        all_fabrics.extend(fabrics)
    all_fabrics = sorted(all_fabrics)

    # ================== USER FABRIC CHOICE ==================
    user_fabric = st.selectbox("👗 Fabric You Want to Wear", all_fabrics)

    # ================== ENCODINGS ==================
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

            # Get actual fabrics in the predicted group
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

            if user_fabric in fabric_map[pred_group]:
                message = (
                    f"🎉 Hurray! Your choice of '<i>{user_fabric}</i>' is FABULOUS for your selections! 😎💫<br>"
                    f"Buddy prediction: <b>{pred_group}</b> – meaning all these fab fabrics are safe too: <b>{fabrics_in_group}</b> 🌟<br>"
                    f"Looks like your fashion sense is already on point! 🕺💃<br>"
                    f"Go ahead, flaunt that fabric, twirl a bit, and feel like a superstar! ✨👗👕"
                )
            else:
                message = (
                    f"🤔 Hmm… you chose '<i>{user_fabric}</i>', but your Fabric Buddy thinks <b>{pred_group}</b> fabrics would be more comfy & stylish! 🧵✨<br>"
                    f"Options you can rock: <b>{fabrics_in_group}</b> 🌟<br>"
                    f"Don’t worry, buddy loves your choice too, but consider trying one of these next time for max wow factor! 😄<br>"
                    f"Remember: confidence + fabric = legendary combo! 💃🕺"
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
                - Pick fabrics suited for your weather: breathable for hot 🌞, warm for cold ❄️.<br>
                - Fabrics + skin tone = instant style points 🎨💯<br>
                - LightSoft fabrics = silky clouds on your skin ☁️✨<br>
                - Denim & Synthetic = durable, casual vibes 😎<br>
                - Confidence is the best accessory – twirl like a superstar! 💃🕺<br>
                - Try new fabrics, but always let comfort be your buddy! 😄
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Oopsie! Something went wrong during prediction: {e} 😅")



# ---------------- ELECTRONICS PAGE ---------------- #

def electronics_page(electronics_data, embed_model):
    st.title("📱 Electronics Fixing Buddy 🤖✨")

    # ================== BANNER ==================
    st.markdown("""
    <div style="
        padding:20px; 
        text-align:center; 
        border-radius:15px; 
        background: linear-gradient(135deg, #e1bee7, #ce93d8);
        color:#6a1b9a;
        font-size:22px;
        font-weight:700;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom:20px;
    ">
    ⚡ Quick Fixes for Smarter Living – Your Tech Buddy is Here! ⚡
    </div>
    """, unsafe_allow_html=True)

    # ================== INTRO CARD ==================
    intro_card_style = """
        padding:35px; 
        border-radius:20px; 
        background:linear-gradient(135deg, #e3f2f9, #c7e8f6); 
        box-shadow: 2px 2px 20px rgba(0,0,0,0.08);
        font-size:16px;
        line-height:1.8;
        color:#37474f;
        margin-bottom:20px;
    """

    intro_html = f"""<div style="{intro_card_style}">
🎉 <b>Welcome, gadget wizard!</b> 🛠️<br><br>
Feeling frustrated because your <b style="color:#0277bd;">device is misbehaving</b>? 
Fear not! I’m your <b style="color:#6a1b9a;">friendly, slightly nerdy buddy</b> ready to save the day ⚡<br><br>
Here’s how I roll:<br>
1️⃣ <b style="color:#00796b;">Step-by-step fixes 🔧</b> – so simple even your cat could watch you do it 😹<br>
2️⃣ <b style="color:#ff8f00;">Funny, quirky tips 😜</b> – expect random tech humor and puns!<br>
3️⃣ <b style="color:#d32f2f;">Serious advice 📞</b> – only when things get really spicy 🌶️<br><br>
So spill the beans, the weirder your description, the more fun our buddy adventure! 🤖💬
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
            st.warning("⚠️ Come on, buddy needs some clues! Describe the problem 😅")
            return

        if not electronics_data:
            st.warning("⚠️ Whoops! I don’t have any electronics data loaded 😬")
            return

        user_emb = embed_model.encode(user_input, convert_to_tensor=True)

        best_match = None
        max_score = -1

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

        # ================== SOLUTION CARD ==================
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

        solution_html = f'<div style="{solution_card_style}">'

        buddy_headers_good = [
            "😎 Buddy Tip Incoming:", 
            "🛠️ Genius Hack:", 
            "💡 Quick Fix Alert:", 
            "🤔 Try This Clever Move:"
        ]
        buddy_headers_fallback = [
            "😬 Hmm… Not sure:", 
            "🤖 Brainstorming Mode:", 
            "⚡ Device Acting Up:", 
            "📞 Call in Reinforcements:"
        ]

        if best_match and max_score > 0.6:
            solution_html += f'<h3 style="color:#d81b60;">{random.choice(buddy_headers_good)}</h3>'
            steps = best_match["solution"].split(", ")
            for i, step in enumerate(steps, start=1):
                solution_html += f'<p style="margin:5px 0;">🔹 <b>Step {i}:</b> {step} ✅</p>'

            if 'tips' in best_match:
                solution_html += f'<p style="margin-top:10px; padding:10px; background:#fff3e0; border-radius:10px;">💡 <b>Extra Buddy Tips:</b> {best_match["tips"]}</p>'
            
            # Add funny closing comment
            solution_html += f'<p style="margin-top:10px; font-style:italic; color:#6a1b9a;">🎉 Remember: Even if you break it more, at least you had fun! 😜</p>'
        else:
            solution_html += f'<h3 style="color:#d32f2f;">{random.choice(buddy_headers_fallback)}</h3>'
            solution_html += "<p>I couldn’t find an exact fix 😅, but try some buddy-approved tricks:</p>"
            solution_html += "<ul style='margin-left:20px;'>"
            solution_html += "<li>🔌 Double-check your cables and connections</li>"
            solution_html += "<li>🔄 Restart your device – it loves a nap 😴</li>"
            solution_html += "<li>💾 Update the software if possible – gadgets like to stay trendy 💅</li>"
            solution_html += "<li>📞 Call official support if all else fails – don’t worry, they speak human too 😎</li>"
            solution_html += "</ul>"
            solution_html += f'<p style="margin-top:10px; font-style:italic; color:#6a1b9a;">🎉 Your buddy is cheering you on! You got this! 💪🤖</p>'

        solution_html += "</div>"
        st.markdown(solution_html, unsafe_allow_html=True)

# ---------------- MAIN UI ---------------- #
def show_ui(food_model, food_vectorizer, fabric_model, electronics_data):
    from PIL import Image

    # Apply global styles
    add_styles()

    # ---------------- SIDEBAR ---------------- #
    st.sidebar.title("🛍️ Lifestyle Helper")
    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"]
    )

    # ---------------- HOME PAGE ---------------- #
    if page == "🏠 Home":
        st.title("🏠 Welcome to ✨ Kraya ✨")
        st.markdown(
            '<div class="banner">✨ The funny buddy for shoppers in trouble ✨</div>',
            unsafe_allow_html=True
        )

        # ---------------- SYSTEM DESCRIPTION ---------------- #
        st.markdown(
            """
            Kraya is your **personal customer support buddy** – yes, the one that’s always chill, 
            sometimes sarcastic, and totally obsessed with helping you! 😎
            """,
            unsafe_allow_html=True
        )

        # ---------------- FIRST IMAGE (AFTER DESCRIPTION) ---------------- #
        try:
            img_desc = Image.open("assets/home1.png")
            st.image(
                img_desc,
                caption="Kraya: Your quirky, smart, life-saving buddy 😎",
                width=1000  # adjust size
            )
        except FileNotFoundError:
            st.warning("⚠️ 'home1.png' not found in the assets folder!")

        # ---------------- ADDITIONAL SYSTEM DESCRIPTION ---------------- #
        st.markdown(
            """
            Here’s the lowdown on what I do:<br>
            🍎 **Food**: ML-powered health analyzer. I’ll tell you if that snack is your friend or foe. 🥗😅<br>
            📱 **Electronics**: AI-powered troubleshooting. Your gadgets have drama? I got the tea ☕🔧<br>
            🧵 **Fabric**: Personalized outfit recommendations. Dress smart, slay harder! 👗💃
            """,
            unsafe_allow_html=True
        )

        # ---------------- SECOND IMAGE (ORIGINAL PLACE) ---------------- #
        try:
            img_banner = Image.open("assets/home2.png")
            st.image(
                img_banner,
                caption="Kraya in action: Helping you shop smart and slay! 💃",
                width=400  # adjust size
            )
        except FileNotFoundError:
            st.warning("⚠️ 'home2.png' not found in the assets folder!")

        # ---------------- NEW INFORMATIVE PASTEL CARD ---------------- #
        st.markdown("""
        <div style="
            padding:20px;
            border-radius:15px;
            background: linear-gradient(135deg, #e1f5fe, #b3e5fc);
            color:#0d47a1;
            font-size:16px;
            line-height:1.6;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.08);
            margin-top:15px;
        ">
            💡 <b>Pro Tips & FAQs:</b><br><br>
            1️⃣ Navigate using the sidebar like a boss to reach Food, Electronics, or Fabric pages.<br>
            2️⃣ Fill in ALL the details — I’m smart, but I’m not psychic 🤖✨<br>
            3️⃣ For Food: list ingredients, calories, macros, and your goal — I’ll judge (nicely) 🥗💪<br>
            4️⃣ For Electronics: spill all the gadget drama. The weirder, the better! 📱🤯<br>
            5️⃣ For Fabric: give me skin tone, weather, season, and outfit vibes — I’ll roast or praise accordingly 😎👗<br>
            6️⃣ Remember: I’m your guide, not a replacement for your nutritionist, tech expert, or stylist. But I am super funny 😜<br>
            7️⃣ Have fun! I live to help, crack jokes, and make your shopping & styling smarter.<br><br>
            📌 Check back often — I’m learning new tricks every day! 🤖✨
        </div>
        """, unsafe_allow_html=True)

    # ---------------- FOOD PAGE ---------------- #
    elif page == "🍎 Food":
        if not food_model or not food_vectorizer:
            st.warning("⚠️ Food model or vectorizer not loaded properly!")
        else:
            food_page(food_model, food_vectorizer)

    # ---------------- FABRIC PAGE ---------------- #
    elif page == "🧵 Fabric":
        if not fabric_model:
            st.warning("⚠️ Fabric model not loaded properly!")
        else:
            fabric_page(fabric_model)

    # ---------------- ELECTRONICS PAGE ---------------- #
    elif page == "📱 Electronics":
        if not electronics_data:
            st.warning("⚠️ Electronics data not loaded properly!")
        else:
            embed_model = SentenceTransformer('all-MiniLM-L6-v2')
            electronics_page(electronics_data, embed_model)
