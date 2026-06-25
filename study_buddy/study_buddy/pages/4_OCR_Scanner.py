import streamlit as st
from utils.ocr_utils import extract_text
from utils.file_db import load, save, next_id

st.set_page_config(page_title="OCR Scanner", page_icon="🔍", layout="wide")


st.title("🔍 OCR Notes Scanner")
st.caption("Upload a photo of handwritten or printed notes to extract text.")

img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
if img:
    st.image(img, use_container_width=True)
    text = extract_text(img)
    st.subheader("Extracted text")
    edited = st.text_area("Result", text, height=240)
    title = st.text_input("Save as note titled", value="Scanned note")
    subject = st.text_input("Subject", value="")
    if st.button("💾 Save as note"):
        notes = load("notes")
        notes.append({"id": next_id(notes), "user_id": u["id"],
                      "title": title, "subject": subject, "content": edited, "file": None})
        save("notes", notes)
        st.success("Saved to your notes.")
