"""ZenTech AI – AI Powered Study Buddy (entry point)."""
import streamlit as st
from dotenv import load_dotenv
import os
from utils.ai_utils import ask_ai, has_api_key
from utils.file_db import ensure_storage
from utils.auth import login, register, logout, current_user


load_dotenv()
st.set_page_config(page_title="ZenTech AI – Study Buddy", page_icon="📚", layout="wide")
ensure_storage()

st.write("DEBUG KEY:", os.getenv("OPENAI_API_KEY"))


st.title("📚 ZenTech AI")
st.caption("Your AI-powered study buddy")



if not has_api_key():
    st.warning("API key not configured, running in demo mode.")

user = current_user()
with st.sidebar:
    st.header("Account")
    if user:
        st.success(f"Signed in as {user['name']}")
        if st.button("Logout", use_container_width="stretch"):
            logout(); st.rerun()
    else:
        st.info("Log in or register to begin.")

if user:
    st.subheader(f"Hi {user['name']} 👋")
    st.write("Use the **sidebar** to open Dashboard, Planner, Notes, OCR, AI Tutor, Quiz, Revision, Analytics, Prediction, and Settings.")
    st.page_link("pages/1_Dashboard.py", label="➡️ Go to Dashboard")
else:
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Log in", use_container_width=True):
                ok, msg = login(email, pw)
                (st.success if ok else st.error)(msg)
                if ok: st.rerun()
    with tab2:
        with st.form("reg_form"):
            name = st.text_input("Name")
            email = st.text_input("Email ")
            pw = st.text_input("Password ", type="password")
            if st.form_submit_button("Create account", use_container_width=True):
                ok, msg = register(name, email, pw)
                (st.success if ok else st.error)(msg)
