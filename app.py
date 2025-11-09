import json
import pickle
import random
import pandas as pd

# -------------------------
# Load models and vectorizers
# -------------------------
# Food model
with open("food/food_weight_model_final.pkl", "rb") as f:
    food_model = pickle.load(f)
with open("food/tfidf_vectorizer_final.pkl", "rb") as f:
    food_vectorizer = pickle.load(f)

# Fabric model
with open("fabric/fashion_fabric_model.pkl", "rb") as f:
    fabric_model = pickle.load(f)
with open("fabric/fashion_vectorizer_best(1).pkl", "rb") as f:
    fabric_vectorizer = pickle.load(f)

# Electronics data
with open("electronics/electronics.json", "r") as f:
    electronics_data = json.load(f)


# -------------------------
# Food Prediction Function
# -------------------------
def predict_food_label(ingredients, label, calories, protein, carbs, fiber, fat, sugar):
    text_input = f"{ingredients} {label}"
    vectorized = food_vectorizer.transform([text_input])
    predicted_label = food_model.predict(vectorized)[0]

    if predicted_label == label.lower():
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
    input_text = f"{skin_tone} {weather} {work_level} {season}"
    vectorized = fabric_vectorizer.transform([input_text])
    outfit = fabric_model.predict(vectorized)[0]

    # Add two extra outputs
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
    responses = [
        "It seems you’re asking about a connectivity issue — please check the power cable and try again.",
        "You might want to reset your device and update the firmware.",
        "If the product isn’t responding, try restarting or checking for software updates.",
        "Ensure your device is connected properly — sometimes the issue is with the adapter or port.",
    ]
    return random.choice(responses)
