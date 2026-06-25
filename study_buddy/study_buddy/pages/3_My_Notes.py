import streamlit as st
from pathlib import Path
from utils.file_db import load, save, next_id, UPLOADS

st.set_page_config(page_title="My Notes", page_icon="📝", layout="wide")

st.title("📝 My Notes")

# ➕ NEW NOTE
with st.expander("➕ New note", expanded=True):
    with st.form("new_note"):
        title = st.text_input("Title")
        subject = st.text_input("Subject")
        content = st.text_area("Content", height=160)
        upload = st.file_uploader("Attach file (optional)", type=None)

        if st.form_submit_button("Save note"):
            if not title.strip():
                st.error("Title required.")
            else:
                file_path = None

                if upload is not None:
                    UPLOADS.mkdir(exist_ok=True, parents=True)
                    file_path = str(UPLOADS / f"{next_id(load('notes'))}_{upload.name}")
                    Path(file_path).write_bytes(upload.getbuffer())

                notes = load("notes")

                notes.append({
                    "id": next_id(notes),
                    "title": title.strip(),
                    "subject": subject.strip(),
                    "content": content,
                    "file": file_path
                })

                save("notes", notes)
                st.success("Note saved.")
                st.rerun()

# 🔎 SEARCH NOTES
q = st.text_input("🔎 Search notes")

notes = load("notes")

if q:
    ql = q.lower()
    notes = [
        n for n in notes
        if ql in n.get("title", "").lower()
        or ql in n.get("subject", "").lower()
        or ql in n.get("content", "").lower()
    ]

# 📌 DISPLAY
if not notes:
    st.info("No notes yet.")

for n in notes:
    with st.expander(f"📄 {n['title']}  —  {n.get('subject','')}"):
        st.write(n.get("content") or "_(empty)_")

        if n.get("file"):
            st.caption(f"Attachment: {n['file']}")

        c1, c2 = st.columns(2)

        new_content = c1.text_area(
            "Edit content",
            n.get("content", ""),
            key=f"c{n['id']}"
        )

        if c1.button("Save changes", key=f"s{n['id']}"):
            all_n = load("notes")

            for x in all_n:
                if x["id"] == n["id"]:
                    x["content"] = new_content

            save("notes", all_n)
            st.success("Updated.")
            st.rerun()

        if c2.button("🗑️ Delete", key=f"d{n['id']}"):
            save("notes", [x for x in load("notes") if x["id"] != n["id"]])
            st.rerun()
