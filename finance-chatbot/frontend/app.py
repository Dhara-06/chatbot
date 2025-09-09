import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="Personal Finance Chatbot", page_icon="💰", layout="wide")

# Sidebar content
with st.sidebar:
    st.header("💡 Info")
    st.write("""
    Ask your financial questions and get AI-powered answers instantly.
    """)
    st.markdown("---")
    st.header("⚙ Settings")
    model = st.selectbox("Choose model", ["Default AI", "Advanced AI"])
    st.markdown("Adjust the settings if needed.")

# Main title
st.markdown("<h1 style='text-align: center;'>💰 Personal Finance Chatbot</h1>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat display area
chat_container = st.container()

with chat_container:
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.markdown(f"""
            <div style='text-align: right; background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 70%; float: right; clear: both;'>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='text-align: left; background-color: #F1F0F0; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 70%; float: left; clear: both;'>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

# Input area
with st.form("input_form", clear_on_submit=True):
    prompt = st.text_input("Ask a financial question...", "")
    submit = st.form_submit_button("Send")

if submit and prompt.strip() != "":
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with chat_container:
        st.markdown(f"""
        <div style='text-align: right; background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 70%; float: right; clear: both;'>
            {prompt}
        </div>
        """, unsafe_allow_html=True)

    # Call backend
    with st.spinner("Analyzing with AI..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/generate",
                json={"text": prompt, "model": model}
            )
            if response.status_code == 200:
                result = response.json()
                if "response" in result:
                    bot_reply = result["response"]

                    # Add bot reply
                    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
                    with chat_container:
                        st.markdown(f"""
                        <div style='text-align: left; background-color: #F1F0F0; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 70%; float: left; clear: both;'>
                            {bot_reply}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("No response field returned from backend")
            else:
                st.error(f"Backend error: {response.status_code}")
        except Exception as e:
            st.error(f"Request failed: {e}")
