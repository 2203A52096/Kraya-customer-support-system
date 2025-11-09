import json
import pickle
import random
import pandas as pd

# -------------------------
# Load Models and Data
# -------------------------
# Food
with open("food/food_weight_model_final.pkl", "rb") as f:
    food_model = pickle.load(f)
with open("food/tfidf_vectorizer_final.pkl", "rb") as f:
    food_vectorizer = pickle.load(f)

# Fabric
with open("fabric/fashion_fabric_model.pkl", "rb") as f:
    fabric_model = pickle.load(f)
with open("fabric/fashion_vectorizer_best(1).pkl", "rb") as f:
    fabric_vectorizer = pickle.load(f)

# Electronics JSON
with open("electronics/electronics.json", "r") as f:
    electronics_data = json.load(f)


# -------------------------
# Food Prediction Function
# -------------------------
def predict_food_label(ingredients, label, calories, protein, carbs, fiber, fat, sugar):
    text_input = f"{ingredients} {label}"
    vectorized = food_vectorizer.transform([text_input])
    predicted_label = food_model.predict(vectorized)[0]

    if predicted_label.lower() == label.lower():
        if label.lower() == "weight loss":
            return "✅ The taken food product is suitable for weight loss."
        else:
            return "✅ The taken food product is suitable for weight gain."
    else:
        return f"⚠️ This food may not be suitable for {label.lower()}."


# -------------------------
# Fabric Prediction Function
# -------------------------
def predict_fabric_recommendation(skin_tone, weather, work_level, season):
    text_input = f"{skin_tone} {weather} {work_level} {season}"
    vectorized = fabric_vectorizer.transform([text_input])
    outfit = fabric_model.predict(vectorized)[0]

    recommended_fabrics = random.choice(["Cotton", "Linen", "Silk", "Denim"])
    avoid_fabrics = random.choice(["Wool", "Polyester", "Nylon", "Velvet"])

    return {
        "Recommended Outfit": outfit,
        "Recommended Fabric": recommended_fabrics,
        "Avoid Fabrics": avoid_fabrics,
    }


# -------------------------
# Electronics "Mistral-like" Function
# -------------------------
def mistral_like_response(user_query):
    canned_responses = [
        "🔌 Please check the power connection and ensure the adapter is properly plugged in.",
        "⚙️ Try restarting your device and updating its firmware.",
        "💡 If your product is unresponsive, check for software updates or connectivity issues.",
        "📶 Make sure the device is connected to a stable power or network source.",
        "🧰 Try resetting to factory settings if the issue persists.",
    ]
    return random.choice(canned_responses)
