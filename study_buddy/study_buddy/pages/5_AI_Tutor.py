import streamlit as st
from utils.ai_utils import ask_ai, has_api_key

st.set_page_config(page_title="AI Tutor", page_icon="🤖", layout="wide")


st.title("🤖 AI Tutor")
if not has_api_key():
    st.info("Demo mode: responses are sample text. Set OPENROUTER_API_KEY to enable real AI.")

if "chat" not in st.session_state:
    st.session_state.chat = []

c1, c2, c3 = st.columns(3)
quick = None
if c1.button("Explain simply"): quick = "Explain simply: "
if c2.button("Summarize"): quick = "Summarize this: "
if c3.button("Ask quiz from topic"): quick = "Make 3 quiz questions about: "

for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask anything about your studies…")
if quick and not prompt:
    prompt = st.text_input("Topic", key="qk") and (quick + st.session_state["qk"])

if prompt:
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            ans = ask_ai(prompt)
        st.markdown(ans)
    st.session_state.chat.append({"role": "assistant", "content": ans})

if st.button("Clear chat"):
    st.session_state.chat = []; st.rerun()
