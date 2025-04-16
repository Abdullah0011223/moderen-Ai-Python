import streamlit as st
import re

# Page Config
st.set_page_config(page_title="Password Strength Checker", page_icon="🔐")

# Styling
st.markdown("""
    <style>
        body {
            background-color: black;
        }
        .stApp {
            background-color: black;
        }
        .stTextInput>div>div>input {
            font-size: 18px;
        }
        .stButton>button {
            background-color: #2E86C1;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5em 1.5em;
        }
        .stButton>button:hover {
            background-color: #1B4F72;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center; color:#2E86C1;'>🔐 Password Strength Checker</h1>", unsafe_allow_html=True)
st.markdown("---")

# Password Input
password = st.text_input("Enter your password:", type="password")

# Strength Check Function
def check_password_strength(password):
    score = 0
    messages = []

    if len(password) >= 8:
        score += 1
    else:
        messages.append("❌ Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        messages.append("❌ Include both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        messages.append("❌ Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        messages.append("❌ Include at least one special character (!@#$%^&*).")

    return score, messages

# Button to Check
if st.button("Check Password"):
    if password == "":
        st.warning("⚠️ Please enter a password to check.")
    else:
        score, feedback = check_password_strength(password)

        for msg in feedback:
            st.write(msg)

        if score == 4:
            st.success("✅ Strong Password!")
        elif score == 3:
            st.info("⚠️ Moderate Password - Consider adding more security features.")
        else:
            st.error("❌ Weak Password - Improve it using the suggestions above.")
