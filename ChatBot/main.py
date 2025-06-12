import streamlit as st
import requests
import time

# 💡 Gemini API key
API_KEY = "AIzaSyBv84DaFWfHMn809sT6zQ3rh3rnmyDwlLY"  # 🔐 Replace with your actual key
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Set page config
st.set_page_config(page_title="Ai Chatbot", layout="centered")

# ✅ Custom white UI
st.markdown("""
    <style>
        .stApp {
            background-color: white !important;
            color: black !important;
        }
        h1 {
            color: green !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🌟 AI Chatbot By Abdullah")

# Session state setup
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}  # {title: [messages]}
if "chat_index" not in st.session_state:
    st.session_state.chat_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm Ai 🤖 — How can I help you today?"}
    ]
if "current_title" not in st.session_state:
    st.session_state.current_title = f"Chat {st.session_state.chat_index + 1}"

# Function to call Gemini
def get_gemini_response(prompt):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Error: {e}"

# Sidebar: Chat history with delete option
with st.sidebar:
    st.header("🕘 Chat History")

    # Create a copy to avoid RuntimeError during iteration
    for title in list(st.session_state.all_chats.keys()):
        col1, col2 = st.columns([0.75, 0.25])
        with col1:
            if st.button(title, key=title):
                st.session_state.messages = st.session_state.all_chats[title]
                st.session_state.current_title = title
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"delete_{title}"):
                del st.session_state.all_chats[title]
                if st.session_state.current_title == title:
                    st.session_state.messages = [
                        {"role": "assistant", "content": "Hi! I'm Ai 🤖 — How can I help you today?"}
                    ]
                    st.session_state.current_title = "Chat 1"
                st.rerun()

    if st.button("➕ New Chat"):
        st.session_state.chat_index += 1
        st.session_state.current_title = f"Chat {st.session_state.chat_index + 1}"
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm Ai 🤖 — How can I help you today?"}
        ]
        st.rerun()

# Show messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div style='color:black'>{msg['content']}</div>", unsafe_allow_html=True)

# Input + reply
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(f"<div style='color:black'>{prompt}</div>", unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner("💭 Chatbot is thinking..."):
            reply = get_gemini_response(prompt)
            message_placeholder = st.empty()
            full_response = ""
            for chunk in reply.split():
                full_response += chunk + " "
                message_placeholder.markdown(
                    f"<div style='color:black'>{full_response}▌</div>",
                    unsafe_allow_html=True
                )
                time.sleep(0.03)
            message_placeholder.markdown(
                f"<div style='color:black'>{full_response}</div>",
                unsafe_allow_html=True
            )

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.all_chats[st.session_state.current_title] = st.session_state.messages.copy()
