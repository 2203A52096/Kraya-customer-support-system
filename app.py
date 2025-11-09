import streamlit as st
import pickle
import json
import difflib
import random

# ---------------- Load Models ---------------- #
# Food
food_model = pickle.load(open("food_weight_model_final.pkl", "rb"))
food_vectorizer = pickle.load(open("tfidf_vectorizer_final.pkl", "rb"))

# Fabric
fabric_model = pickle.load(open("fashion_fabric_model.pkl", "rb"))
fabric_vectorizer = pickle.load(open("fashion_vectorizer_best(1).pkl", "rb"))

# Electronics JSON
with open("electronics.json", "r") as f:
    electronics_data = json.load(f)


# ---------------- Mistral-like Response Generator ---------------- #
def mistral_like_response(user_query):
    """Simulate Mistral model by finding best matching problem or query from JSON."""
    all_problems = []
    for item in electronics_data:
        all_problems.extend(item["example_queries"])
        all_problems.append(item["problem"])
        all_problems.append(item["category"])

    closest_match = difflib.get_close_matches(user_query, all_problems, n=1, cutoff=0.3)
    if not closest_match:
        return {
            "device": "Unknown Device",
            "issue": user_query,
            "solution": "Sorry, I couldn't find a matching issue in the database. Please describe it in more detail."
        }

    matched = closest_match[0]
    for item in electronics_data:
        if matched in item["example_queries"] or matched == item["problem"] or matched == item["category"]:
            return {
                "device": item["device"],
                "issue": item["problem"],
                "solution": item["solution"]
            }

    # Fallback if somehow no match found
    return {
        "device": "General Device",
        "issue": user_query,
        "solution": "Try restarting your device or checking for software updates."
    }


# ---------------- Prediction Functions ---------------- #
def predict_food(ingredients, label, calories, protein, carbs, fiber, fat, sugar):
    input_text = f"{ingredients} {calories} {protein} {carbs} {fiber} {fat} {sugar}"
    vectorized = food_vectorizer.transform([input_text])
    prediction = food_model.predict(vectorized)[0]

    if prediction == label:
        if label.lower() == "weight loss":
            result = "✅ The taken food product is suitable for weight loss."
        else:
            result = "✅ The taken food product is suitable for weight gain."
    else:
        result = f"⚠️ The food may not align with your goal ({label}). Predicted as {prediction}."
    return prediction, result


def predict_fabric(skin_tone, weather, work_level, season):
    # Combine inputs into a descriptive string
    input_text = f"{skin_tone} {weather} {work_level} {season}"
    vectorized = fabric_vectorizer.transform([input_text])
    outfit = fabric_model.predict(vectorized)[0]

    # Extra logic for fabric suggestions
    if weather.lower() in ["hot", "summer", "sunny"]:
        rec_fabric = "Cotton, Linen"
        avoid = "Wool, Polyester"
    elif weather.lower() in ["cold", "winter"]:
        rec_fabric = "Wool, Fleece"
        avoid = "Silk, Rayon"
    else:
        rec_fabric = "Denim, Nylon"
        avoid = "Velvet"

    return outfit, rec_fabric, avoid


# ---------------- Streamlit UI ---------------- #
st.set_page_config(page_title="Smart Customer Support System", layout="centered")
st.title("🤖 Smart Customer Support System")

option = st.sidebar.selectbox(
    "Select Category",
    ["Food Recommendation", "Electronics Support", "Fabric Recommendation"]
)

# ---------------- Food Section ---------------- #
if option == "Food Recommendation":
    st.header("🥗 Food Suitability Prediction")

    ingredients = st.text_input("Ingredients (comma separated)")
    label = st.selectbox("Your Goal", ["weight loss", "weight gain"])
    calories = st.number_input("Calories", 0, 2000, 250)
    protein = st.number_input("Protein (g)", 0.0, 200.0, 10.0)
    carbs = st.number_input("Carbohydrates (g)", 0.0, 300.0, 30.0)
    fiber = st.number_input("Fiber (g)", 0.0, 100.0, 5.0)
    fat = st.number_input("Fat (g)", 0.0, 100.0, 5.0)
    sugar = st.number_input("Sugar (g)", 0.0, 100.0, 10.0)

    if st.button("Predict Food Suitability"):
        pred, result = predict_food(ingredients, label, calories, protein, carbs, fiber, fat, sugar)
        st.success(f"Predicted Label: **{pred}**")
        st.info(result)


# ---------------- Electronics Section ---------------- #
elif option == "Electronics Support":
    st.header("🔌 Electronics Support Chat")

    user_query = st.text_input("Describe your issue:")
    if st.button("Get Help"):
        response = mistral_like_response(user_query)
        st.markdown(f"""
        **Device:** {response['device']}  
        **Issue:** {response['issue']}  

        💡 **Suggested Fix:** {response['solution']}
        """)


# ---------------- Fabric Section ---------------- #
elif option == "Fabric Recommendation":
    st.header("👕 Fabric and Outfit Recommendation")

    skin_tone = st.selectbox("Skin Tone", ["Fair", "Medium", "Dark"])
    weather = st.selectbox("Weather Condition", ["Hot", "Cold", "Rainy", "Humid"])
    work_level = st.selectbox("Work Level", ["High", "Moderate", "Low"])
    season = st.selectbox("Season", ["Summer", "Winter", "Monsoon", "Spring"])

    if st.button("Recommend Fabric and Outfit"):
        outfit, rec, avoid = predict_fabric(skin_tone, weather, work_level, season)
        st.success(f"👗 Recommended Outfit: **{outfit}**")
        st.info(f"✅ Recommended Fabrics: **{rec}**")
        st.warning(f"🚫 Avoid Fabrics: **{avoid}**")
