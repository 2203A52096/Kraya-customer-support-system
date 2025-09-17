import streamlit as st

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Customer Support System",
    page_icon="🤝",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
cloud_background = """
<style>
/* Background with subtle cloud-like gradient */
.stApp {
    background: linear-gradient(135deg, #f0f9ff, #cbebff, #e6f7ff, #ffffff);
    background-attachment: fixed;
    font-family: 'Segoe UI', sans-serif;
}

/* Cloud-like padded container */
.cloud-box {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 50px;
    padding: 30px 40px;
    box-shadow: 2px 4px 20px rgba(0,0,0,0.1);
    margin-bottom: 30px;
}

/* Highlighted keywords */
.keyword {
    color: #0077b6;
    font-weight: bold;
}

/* Tagline style */
.tagline {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 15px;
}
</style>
"""

st.markdown(cloud_background, unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "🍎 Food Domain", "👗 Fabric Domain", "💻 Electronics Domain"])

# -------------------- HOME --------------------
if page == "🏠 Home":
    st.markdown('<div class="cloud-box">', unsafe_allow_html=True)
    st.title("🤝 Customer Support System")
    st.markdown(
        """
        <p class="tagline" style="color:#ff6f61;">Smart Guidance, Smarter Choices.</p>
        <p class="tagline" style="color:#2a9d8f;">Personalized Assistance at Your Fingertips.</p>
        <p class="tagline" style="color:#457b9d;">Making Decisions Easier and Better.</p>
        """,
        unsafe_allow_html=True
    )
    st.write(
        """
        This project provides **domain-specific assistance** across  
        **Food**, **Fabric**, and **Electronics**.  
        It enhances **decision-making**, improves **satisfaction**,  
        and ensures **convenience** for customers.
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- FOOD DOMAIN --------------------
elif page == "🍎 Food Domain":
    st.markdown('<div class="cloud-box">', unsafe_allow_html=True)
    st.header("🍎 Food Assistance")
    st.write(
        """
        In the **Food domain**, the system helps customers by suggesting if a chosen  
        product is **healthy**, suitable for **weight loss** or **weight gain**.  
        It provides **diet-friendly insights** for better health decisions.
        """
    )
    food_choice = st.text_input("Enter a food item:")
    if food_choice:
        st.success(f"The system analyzes **{food_choice}** and provides health recommendations.")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- FABRIC DOMAIN --------------------
elif page == "👗 Fabric Domain":
    st.markdown('<div class="cloud-box">', unsafe_allow_html=True)
    st.header("👗 Fabric & Fashion Assistance")
    st.write(
        """
        In the **Fabric domain**, the system suggests **fabric types**  
        and **dress colors** based on **skin tone** and user preferences.  
        It enhances **fashion choices** and ensures **comfort + style**.
        """
    )
    skin_type = st.selectbox("Select your skin tone:", ["Fair", "Medium", "Olive", "Dark"])
    color_pref = st.color_picker("Pick your favorite color:")
    if skin_type:
        st.success(f"For **{skin_type}** skin tone, light pastel shades and elegant fabrics are recommended!")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- ELECTRONICS DOMAIN --------------------
elif page == "💻 Electronics Domain":
    st.markdown('<div class="cloud-box">', unsafe_allow_html=True)
    st.header("💻 Electronics Troubleshooting Assistant")
    st.write(
        """
        In the **Electronics domain**, the system acts as a **troubleshooting guide**,  
        providing **quick solutions** for user issues with devices.  
        It improves **user experience** and reduces **confusion**.
        """
    )
    device = st.selectbox("Select your device type:", ["Mobile", "Laptop", "Television", "Other"])
    issue = st.text_area("Describe your issue:")
    if issue:
        st.success(f"Possible solution: Restart your **{device}**, check connections, or update settings.")
    st.markdown('</div>', unsafe_allow_html=True)
