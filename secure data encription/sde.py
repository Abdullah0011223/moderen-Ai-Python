import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# In-memory storage
stored_data = {}
failed_attempts = {}
authorized_users = {"admin": "admin123"}  # simple login
session_state = st.session_state

# Generate and store a single Fernet key in session
if "fernet_key" not in session_state:
    session_state.fernet_key = Fernet.generate_key()
    session_state.fernet = Fernet(session_state.fernet_key)

# Session state tracking
for key in ["page", "authorized", "current_user"]:
    if key not in session_state:
        session_state[key] = "home" if key == "page" else False if key == "authorized" else None

# Utility functions
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_text(text):
    return session_state.fernet.encrypt(text.encode()).decode()

def decrypt_text(cipher_text):
    return session_state.fernet.decrypt(cipher_text.encode()).decode()

# Pages
def home_page():
    st.title("🔐 Secure Data Encryption System")
    st.write("Choose an action:")
    if st.button("📝 Store New Data"):
        session_state.page = "insert"
    if st.button("🔍 Retrieve Data"):
        session_state.page = "retrieve"

def insert_data_page():
    st.title("📝 Store New Data")
    username = st.text_input("Enter your username:")
    data = st.text_area("Enter the data to encrypt:")
    passkey = st.text_input("Enter a secure passkey:", type="password")
    if st.button("Encrypt and Store"):
        if username and data and passkey:
            encrypted_text = encrypt_text(data)
            stored_data[username] = {
                "encrypted_text": encrypted_text,
                "passkey": hash_passkey(passkey)
            }
            failed_attempts[username] = 0
            st.success("Data encrypted and stored successfully.")
        else:
            st.warning("Please fill in all fields.")
    if st.button("🔙 Back to Home"):
        session_state.page = "home"

def retrieve_data_page():
    st.title("🔍 Retrieve Encrypted Data")
    username = st.text_input("Enter your username:")
    passkey = st.text_input("Enter your passkey:", type="password")
    if st.button("Decrypt Data"):
        if username in stored_data:
            attempts = failed_attempts.get(username, 0)
            if attempts >= 3:
                st.error("Too many failed attempts. Reauthorization required.")
                session_state.page = "login"
                return

            if hash_passkey(passkey) == stored_data[username]["passkey"]:
                decrypted_text = decrypt_text(stored_data[username]["encrypted_text"])
                st.success("Decryption successful!")
                st.code(decrypted_text, language="text")
                failed_attempts[username] = 0
            else:
                failed_attempts[username] = attempts + 1
                st.error(f"Incorrect passkey. Attempt {failed_attempts[username]} of 3.")
                if failed_attempts[username] >= 3:
                    st.warning("Redirecting to login for reauthorization...")
                    session_state.page = "login"
        else:
            st.error("Username not found.")
    if st.button("🔙 Back to Home"):
        session_state.page = "home"

def login_page():
    st.title("🔐 Reauthorization Required")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if authorized_users.get(user) == pwd:
            st.success("Login successful!")
            session_state.page = "retrieve"
        else:
            st.error("Invalid credentials.")
    if st.button("🔙 Back to Home"):
        session_state.page = "home"

# Page routing
if session_state.page == "home":
    home_page()
elif session_state.page == "insert":
    insert_data_page()
elif session_state.page == "retrieve":
    retrieve_data_page()
elif session_state.page == "login":
    login_page()
