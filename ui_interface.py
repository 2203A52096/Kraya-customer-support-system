import streamlit as st
import numpy as np

# -----------------------------
# Fake Mistral-like function
# -----------------------------
def mimic_mistral_response(query, electronics_data):
    """
    Mimics a Mistral-like model that generates contextual responses
    from JSON data without using any API.
    """
    query = query.lower()
    for item in electronics_data:
        for example in item["example_queries"]:
            if any(word in query for word in example.lower().split()):
                return (
                    f"**Device:** {item['device']}\n"
                    f"**Category:** {item['category']}\n"
                    f"**Problem:** {item['problem']}\n"
                    f"**Solution:** {item['solution']}"
                )
    return "I'm not sure. Please check device connections or describe the issue more specifically."

# -----------------------------
# Main Interface Function
# -----------------------------
def show_interface(food_model, food_vectorizer, fabric_model, fabric_vectorizer, electronics_data):

    st.title("🤖 Customer Support System")
    st.markdown("Get smart responses for **Food**, **Fabric**, and **Electronics** issues.")

    # Sidebar
    st.sidebar.title("🔧 Select a Category")
    category = st.sidebar.radio("Choose Product Category:", ["Food", "Fabric", "Electronics"])

    st.markdown("---")

    # ======================
    # FOOD SUPPORT SECTION
    # ======================
    if category == "Food":
        st.header("🍔 Food Query")
        query = st.text_input("Enter your food-related question:")
        if st.button("Get Response"):
            if query.strip():
                query_vec = food_vectorizer.transform([query])
                prediction = food_model.predict(query_vec)[0]
                st.success(f"✅ Response: {prediction}")
            else:
                st.warning("Please enter a valid query.")

    # ======================
    # FABRIC SUPPORT SECTION
    # ======================
    elif category == "Fabric":
        st.header("👕 Fabric Query")
        query = st.text_input("Enter your fabric-related question:")
        if st.button("Get Response"):
            if query.strip():
                query_vec = fabric_vectorizer.transform([query])
                prediction = fabric_model.predict(query_vec)[0]
                st.success(f"✅ Response: {prediction}")
            else:
                st.warning("Please enter a valid query.")

    # ======================
    # ELECTRONICS SUPPORT SECTION
    # ======================
    elif category == "Electronics":
        st.header("💻 Electronics Query")
        query = st.text_input("Describe your device issue:")
        if st.button("Get Response"):
            if query.strip():
                response = mimic_mistral_response(query, electronics_data)
                st.info(response)
            else:
                st.warning("Please enter a valid query.")
