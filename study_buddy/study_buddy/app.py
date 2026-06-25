import streamlit as st
from dotenv import load_dotenv
import os

from utils.ai_utils import has_api_key
from utils.file_db import ensure_storage

load_dotenv()

st.set_page_config(
    page_title="ZenTech AI – Study Buddy",
    page_icon="📚",
    layout="wide"
)

ensure_storage()

st.title("📚 ZenTech AI")
st.caption("Your AI-powered study buddy")

# API check
if not has_api_key():
    st.warning("API key not configured, running in demo mode.")

st.subheader("👋 Welcome!")
st.write("Start learning using the sidebar (Dashboard, Notes, Quiz, OCR, etc.)")

st.page_link("pages/1_Dashboard.py", label="➡️ Go to Dashboard")
