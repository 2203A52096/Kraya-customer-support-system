# app.py
import streamlit as st
import os
import io
import json
import pickle
from pathlib import Path
from typing import Any, Dict, Optional

# ML libs
import numpy as np

# safe imports for joblib/pickle
try:
    import joblib
except Exception:
    joblib = None

# optional transformers for local mistral
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    transformers_available = True
except Exception:
    transformers_available = False

# ---------------- STYLING (kept identical) ----------------
st.markdown(
    """
    <style>
    /* Sidebar background pastel color */
    [data-testid="stSidebar"] { background-color: #F7E9E9; color: #5A3E36; border-radius: 20px; }
    /* Sidebar title */
    [data-testid="stSidebar"] > div:first-child { font-size: 24px; font-weight: 700; color: #9A5F6F; }
    /* Badge styles for keywords */
    .badge { display: inline-block; padding: 0.3em 0.7em; font-size: 0.8em; font-weight: 700; line-height: 1; color: white;
             text-align: center; white-space: nowrap; vertical-align: baseline; border-radius: 0.8rem; }
    .badge-food {background-color: #FF6F61;}
    .badge-electronics {background-color: #6BAED6;}
    .badge-fabric {background-color: #8BC34A;}
    .badge-healthy {background-color: #4CAF50;}
    .badge-unhealthy {background-color: #F44336;}
    /* Banner with rounded cloud-like look */
    .banner { background-color: #FFF4E6; border-left: 6px solid #FF6F61; padding: 12px; margin: 10px 0px;
              border-radius: 25px; font-size: 16px; box-shadow: 2px 4px 10px rgba(0,0,0,0.05); }
    /* Rounded box for results */
    .result-box { background: #ffffffdd; border-radius: 25px; padding: 15px 20px; margin: 15px 0;
                   box-shadow: 0px 4px 15px rgba(0,0,0,0.08); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Utilities to load models ----------------

def try_load_pickle(path: Path) -> Optional[Any]:
    """Try to load a pickle/joblib file. Returns object or None."""
    if not path.exists():
        return None
    try:
        if joblib and path.suffix in {".pkl", ".joblib"}:
            return joblib.load(path)
        else:
            with open(path, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        st.warning(f"Failed to load {path.name}: {e}")
        return None

def load_food_model(food_dir: Path):
    """
    Attempts to load:
    - food/model.pkl (could be a sklearn pipeline or a dict{'model','vectorizer'})
    - food/vectorizer.pkl
    Returns dict with model and optional vectorizer or None.
    """
    ret = {"model": None, "vectorizer": None}
    mpath = food_dir / "model.pkl"
    vpath = food_dir / "vectorizer.pkl"
    obj = try_load_pickle(mpath)
    if obj is None and vpath.exists():
        # model missing but vectorizer present
        obj_v = try_load_pickle(vpath)
        if obj_v:
            ret["vectorizer"] = obj_v
    if obj is None:
        return ret
    # if obj looks like a dict
    if isinstance(obj, dict):
        ret["model"] = obj.get("model") or obj.get("clf") or obj.get("estimator")
        ret["vectorizer"] = obj.get("vectorizer", ret["vectorizer"])
    else:
        # could be pipeline (with .predict)
        ret["model"] = obj
    # also try separate vectorizer file
    if ret["vectorizer"] is None and vpath.exists():
        ret["vectorizer"] = try_load_pickle(vpath)
    return ret

def load_fabric_model(fabric_dir: Path):
    """Similar logic for fabric folder."""
    ret = {"model": None, "encoder": None}
    mpath = fabric_dir / "model.pkl"
    encpath = fabric_dir / "encoder.pkl"
    obj = try_load_pickle(mpath)
    if isinstance(obj, dict):
        ret["model"] = obj.get("model") or obj.get("clf")
        ret["encoder"] = obj.get("encoder", None)
    else:
        ret["model"] = obj
    if ret["encoder"] is None and encpath.exists():
        ret["encoder"] = try_load_pickle(encpath)
    return ret

# ---------------- Fallback rule functions (kept from original) ----------------
def analyze_food_rule(ingredients, calories, fat, sugar, fiber, protein):
    ing_list = [i.strip().lower() for i in ingredients.split(",") if i.strip()]
    unhealthy_ingredients = ["sugar", "corn syrup", "hydrogenated oil", "trans fat", "artificial"]
    healthy_tags, unhealthy_tags = [], []
    for ing in ing_list:
        if any(bad in ing for bad in unhealthy_ingredients):
            unhealthy_tags.append(ing)
        elif "whole" in ing or "vegetable" in ing or "fiber" in ing:
            healthy_tags.append(ing)
    if len(unhealthy_tags) > 2 or sugar > 15 or fat > 20:
        return """ <div class="result-box"> <span class="badge badge-unhealthy">❌ Unhealthy</span>: High sugar/fat content. May lead to <b>weight gain</b> and health risks. </div> """
    elif calories < 100 and fat < 5 and sugar < 5:
        return """ <div class="result-box"> <span class="badge badge-healthy">✅ Healthy</span>: Suitable for <b>weight loss</b>, low calories & fat. </div> """
    elif calories > 300 and protein > 10:
        return """ <div class="result-box"> <span class="badge badge-healthy">✅ Healthy</span>: Good for <b>weight gain</b> with high protein & energy. </div> """
    else:
        return """ <div class="result-box"> <span style='color: #FFA500; font-weight:bold;'>⚠️ Moderately healthy</span>. Balanced but watch certain ingredients. </div> """

def suggest_fabric_rule(skin_type, skin_tone, weather, work_level, season):
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
    return f""" <div class="result-box"> <span style='color:#D9534F; font-weight:bold;'>❌ Avoid Fabrics:</span> {", ".join(avoid_fabrics) or "None"}<br><br> <span style='color:#5CB85C; font-weight:bold;'>✅ Recommended Fabrics:</span> {", ".join(preferred_fabrics)}<br><br> <span style='color:#0275D8; font-weight:bold;'>🎨 Suggested Colors:</span> {", ".join(color_suggestions)} </div> """

# ---------------- ML-based inference helpers ----------------

def prepare_food_features(ingredients: str, calories: float, fat: float, sugar: float, fiber: float, protein: float, vectorizer=None):
    """
    Create feature vector for food ML model.
    If vectorizer is present, use it for ingredients and concat numeric features.
    Otherwise return simple numeric array.
    """
    num_feats = np.array([[calories, fat, sugar, fiber, protein]], dtype=float)
    if vectorizer is None:
        return num_feats
    try:
        ing_vec = vectorizer.transform([ingredients])
        # if ing_vec is sparse, convert and hstack
        try:
            from scipy.sparse import hstack as sp_hstack
            X = sp_hstack([ing_vec, num_feats])
            return X
        except Exception:
            # fallback: toarray
            ing_arr = ing_vec.toarray()
            return np.hstack([ing_arr, num_feats])
    except Exception as e:
        st.warning(f"Vectorizer transform failed: {e}. Using numeric features.")
        return num_feats

def predict_food_ml(food_model_info, ingredients, calories, fat, sugar, fiber, protein):
    model = food_model_info.get("model")
    vectorizer = food_model_info.get("vectorizer")
    if model is None:
        return None  # signal to fallback
    X = prepare_food_features(ingredients, calories, fat, sugar, fiber, protein, vectorizer)
    try:
        # if model has predict_proba, use confidence
        pred = model.predict(X)
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)
            conf = np.max(proba, axis=1)[0]
        else:
            conf = None
        label = pred[0] if isinstance(pred, (list, np.ndarray)) else pred
        return {"label": str(label), "confidence": float(conf) if conf is not None else None}
    except Exception as e:
        st.warning(f"Food model prediction failed: {e}")
        return None

def prepare_fabric_features(skin_type, skin_tone, weather, work_level, season, encoder=None):
    """
    Return X for model. If encoder present, use it.
    Otherwise simple manual encoding into numbers.
    """
    data = {"skin_type": skin_type, "skin_tone": skin_tone, "weather": weather, "work_level": work_level, "season": season}
    if encoder is not None:
        try:
            # encoder expected to have transform for dict-like or DataFrame input
            import pandas as pd
            df = pd.DataFrame([data])
            X = encoder.transform(df)
            return X
        except Exception as e:
            st.warning(f"Encoder transform failed: {e}. Falling back to numeric encoding.")
    # fallback: simple manual encoding (one-hot-ish)
    mapping = {
        "skin_type": {"Dry": 0, "Oily": 1, "Sensitive": 2, "Normal": 3},
        "skin_tone": {"Fair": 0, "Medium": 1, "Dark": 2},
        "weather": {"Hot": 0, "Cold": 1, "Humid": 2, "Dry": 3},
        "work_level": {"High": 2, "Medium": 1, "Low": 0},
        "season": {"Summer": 0, "Winter": 1, "Spring": 2, "Autumn": 3}
    }
    arr = np.array([[mapping["skin_type"].get(skin_type, 3),
                     mapping["skin_tone"].get(skin_tone, 0),
                     mapping["weather"].get(weather, 3),
                     mapping["work_level"].get(work_level, 1),
                     mapping["season"].get(season, 0)]], dtype=float)
    return arr

def predict_fabric_ml(fabric_model_info, skin_type, skin_tone, weather, work_level, season):
    model = fabric_model_info.get("model")
    encoder = fabric_model_info.get("encoder")
    if model is None:
        return None
    X = prepare_fabric_features(skin_type, skin_tone, weather, work_level, season, encoder)
    try:
        pred = model.predict(X)
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)
            conf = np.max(proba, axis=1)[0]
        else:
            conf = None
        label = pred[0] if isinstance(pred, (list, np.ndarray)) else pred
        return {"label": str(label), "confidence": float(conf) if conf is not None else None}
    except Exception as e:
        st.warning(f"Fabric model prediction failed: {e}")
        return None

# ---------------- Electronics: Mistral local / endpoint / fallback ----------------

def load_local_mistral_model(elec_dir: Path):
    """
    If there's a transformers-compatible model folder at electronic/local_mistral,
    attempt to create a pipeline for text-generation. Returns the pipeline or None.
    """
    model_folder = elec_dir / "local_mistral"
    if not model_folder.exists():
        return None, "no_local_folder"
    if not transformers_available:
        return None, "transformers_not_installed"
    try:
        # try to build a text-generation pipeline from local weights
        pipe = pipeline("text-generation", model=str(model_folder), device=-1)
        return pipe, "ok"
    except Exception as e:
        return None, f"pipeline_failed:{e}"

def call_mistral_endpoint(endpoint_url: str, prompt: str, timeout: int = 20):
    """
    Simple POST to a user-provided endpoint. This assumes the endpoint accepts JSON {"prompt": "..."}
    and returns JSON {"generated_text": "..."} or plain text. No API key is used.
    """
    import requests
    payload = {"prompt": prompt}
    try:
        resp = requests.post(endpoint_url, json=payload, timeout=timeout)
        if resp.status_code != 200:
            return None, f"HTTP {resp.status_code}: {resp.text}"
        try:
            data = resp.json()
            # try common keys
            text = data.get("generated_text") or data.get("text") or data.get("result") or data.get("output")
            if text:
                return text, None
            else:
                # maybe model returns array
                return json.dumps(data), None
        except Exception:
            # not JSON, return text
            return resp.text, None
    except Exception as e:
        return None, str(e)

# ---------------- App startup: load models ----------------
ROOT = Path(".")
food_info = load_food_model(ROOT / "food")
fabric_info = load_fabric_model(ROOT / "fabric")
# check local mistral availability
local_mistral_pipe, local_mistral_status = load_local_mistral_model(ROOT / "electronic")

# ---------------- MAIN APP (keeps UI) ----------------
st.set_page_config(page_title="Lifestyle Helper App", layout="centered")
st.sidebar.title("🛍️ Lifestyle Helper")
page = st.sidebar.radio(
    "Navigate", ["🏠 Home", "🍎 Food", "📱 Electronics", "🧵 Fabric"],
)

# HOME
if page == "🏠 Home":
    st.title("🏠 Welcome to Kraya")
    st.markdown('<div class="banner">✨ Smart Choices, Happy Living ✨</div>', unsafe_allow_html=True)
    st.markdown(
        """
        Kraya is your **personal customer support system** that makes shopping and usage easier:
        - <span class="badge badge-food">🍎 Food</span>: Check if food is **healthy**, for **weight loss/gain** (ML model used if available).
        - <span class="badge badge-electronics">📱 Electronics</span>: Troubleshoot your **devices** quickly (Mistral local/endpoint or fallback).
        - <span class="badge badge-fabric">🧵 Fabric</span>: Get fabric and **color suggestions** for your skin & season (ML model used if available).
        """,
        unsafe_allow_html=True,
    )

# FOOD PAGE
elif page == "🍎 Food":
    st.title("🍎 Food Health Analyzer")
    st.markdown('<div class="banner">🥗 Eat Smart, Live Better</div>', unsafe_allow_html=True)
    st.info("Enter your food details and find out if it’s suitable for **weight loss, weight gain, or balanced nutrition**.")
    ingredients = st.text_area("🧾 Ingredients (comma-separated)", "sugar, salt, whole grain, vegetable oil")
    calories = st.number_input("🔥 Calories per serving", min_value=0.0, value=0.0)
    fat = st.number_input("🥓 Total Fat (g)", min_value=0.0, value=0.0)
    sugar = st.number_input("🍬 Sugar (g)", min_value=0.0, value=0.0)
    fiber = st.number_input("🌿 Dietary Fiber (g)", min_value=0.0, value=0.0)
    protein = st.number_input("🍗 Protein (g)", min_value=0.0, value=0.0)

    if st.button("🔍 Analyze Food"):
        # Try ML first
        ml_res = predict_food_ml(food_info, ingredients, calories, fat, sugar, fiber, protein)
        if ml_res:
            label = ml_res.get("label")
            conf = ml_res.get("confidence")
            # flexible mapping: try to map common labels to healthy/unhealthy
            lower_label = label.lower()
            if "unhealthy" in lower_label or "bad" in lower_label or "junk" in lower_label:
                html = f""" <div class="result-box"> <span class="badge badge-unhealthy">❌ {label}</span> """
                if conf:
                    html += f"<br><small>Model confidence: {conf:.2f}</small>"
                html += "</div>"
            elif "healthy" in lower_label or "good" in lower_label or "healthy_gain" in lower_label or "gain" in lower_label:
                html = f""" <div class="result-box"> <span class="badge badge-healthy">✅ {label}</span> """
                if conf:
                    html += f"<br><small>Model confidence: {conf:.2f}</small>"
                html += "</div>"
            else:
                # unknown label: show label and confidence
                html = f""" <div class="result-box"> <span style='color:#FFA500; font-weight:bold;'>🔎 {label}</span> """
                if conf:
                    html += f"<br><small>Model confidence: {conf:.2f}</small>"
                html += "</div>"
            st.markdown(html, unsafe_allow_html=True)
        else:
            # fallback to rules
            st.markdown(analyze_food_rule(ingredients, calories, fat, sugar, fiber, protein), unsafe_allow_html=True)

# ELECTRONICS PAGE
elif page == "📱 Electronics":
    st.title("📱 Electronics Help Desk")
    st.markdown('<div class="banner">⚡ Quick Fixes for Smarter Living ⚡</div>', unsafe_allow_html=True)
    st.info("Describe your problem, and Kraya will give **troubleshooting tips**. Use local Mistral model, paste your endpoint (no API key), or fallback to heuristic.")
    devices = ["Smartphone 📱", "Laptop 💻", "TV 📺", "Washing Machine 🧺", "Refrigerator ❄️"]
    device = st.selectbox("🔧 Select your device", devices)
    user_input = st.text_area("✍️ Describe your issue", height=150)

    st.markdown("**Model selection (no API key required)**")
    elec_option = st.radio("Choose electronics response method:",
                           ("Local Mistral model (if available)", "HTTP endpoint (paste URL)", "Heuristic fallback (rules)"))

    endpoint_url = ""
    if elec_option == "HTTP endpoint (paste URL)":
        endpoint_url = st.text_input("Paste your endpoint URL (no API key):", "")

    # show status of local mistral
    if elec_option == "Local Mistral model (if available)":
        if local_mistral_pipe is None:
            st.info(f"Local Mistral not available: {local_mistral_status}. Place model weights under `electronic/local_mistral/` or use endpoint/fallback.")
        else:
            st.success("Local Mistral pipeline loaded.")

    if st.button("🛠️ Get Support"):
        if user_input.strip() == "":
            st.warning("⚠️ Please describe your issue before proceeding.")
        else:
            # handle each option
            if elec_option == "Local Mistral model (if available)" and local_mistral_pipe:
                prompt = f"Device: {device}\nIssue: {user_input}\nProvide step-by-step troubleshooting and recommended next steps."
                try:
                    gen = local_mistral_pipe(prompt, max_length=256, do_sample=False, num_return_sequences=1)
                    text = gen[0].get("generated_text") if isinstance(gen, list) else str(gen)
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown("### **🔧 Suggested Fix (Local Mistral):**", unsafe_allow_html=True)
                    st.write(text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Local Mistral generation failed: {e}. Falling back to heuristic.")
                    # fallback heuristic
                    user_input_lower = user_input.lower()
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown("### **🔧 Suggested Fix:**", unsafe_allow_html=True)
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

            elif elec_option == "HTTP endpoint (paste URL)" and endpoint_url.strip():
                prompt = f"Device: {device}\nIssue: {user_input}\nProvide concise troubleshooting steps."
                text, err = call_mistral_endpoint(endpoint_url.strip(), prompt)
                if err:
                    st.error(f"Endpoint call failed: {err}. Falling back to heuristic.")
                    user_input_lower = user_input.lower()
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown("### **🔧 Suggested Fix:**", unsafe_allow_html=True)
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
                else:
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown("### **🔧 Suggested Fix (Endpoint Response):**", unsafe_allow_html=True)
                    st.write(text)
                    st.markdown('</div>', unsafe_allow_html=True)

            else:
                # heuristic fallback
                user_input_lower = user_input.lower()
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown("### **🔧 Suggested Fix:**", unsafe_allow_html=True)
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
        # try fabric ML
        ml_res = predict_fabric_ml(fabric_info, skin_type, skin_tone, weather, work_level, season)
        if ml_res:
            label = ml_res.get("label")
            conf = ml_res.get("confidence")
            # try to interpret label or just display
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(f"### **🧵 Suggested Fabric(s): {label}**", unsafe_allow_html=True)
            if conf:
                st.markdown(f"<small>Model confidence: {conf:.2f}</small>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(suggest_fabric_rule(skin_type, skin_tone, weather, work_level, season), unsafe_allow_html=True)
