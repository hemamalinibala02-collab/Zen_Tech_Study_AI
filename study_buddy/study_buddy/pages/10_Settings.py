import streamlit as st
from utils.file_db import load, save
from utils.export_utils import export_notes_txt, export_tasks_csv, export_report_pdf
from utils.prediction_utils import compute

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

st.title("⚙️ Settings & Export")

# -------------------------
# PROFILE (GLOBAL - no users)
# -------------------------
st.subheader("Profile (Global)")

st.info("Login system removed → profile is now global for app demo purposes.")

users = load("users")

if users:
    me = users[0]  # take first user as default placeholder
else:
    me = {"name": "User", "theme": "Light"}

new_name = st.text_input("Display name", me.get("name", "User"))

theme = st.selectbox(
    "Theme preference",
    ["Light", "Dark", "System"],
    index=["Light", "Dark", "System"].index(me.get("theme", "Light"))
)

if st.button("Save profile"):
    if users:
        users[0]["name"] = new_name
        users[0]["theme"] = theme
        save("users", users)

    st.success("Profile updated (global mode).")

st.divider()

# -------------------------
# EXPORT SECTION (GLOBAL)
# -------------------------
st.subheader("Export (All Data)")

c1, c2, c3 = st.columns(3)

if c1.button("📄 Notes (.txt)"):
    p = export_notes_txt()   # removed user_id
    st.success(f"Saved: {p}")
    st.download_button("Download notes", p.read_bytes(), file_name=p.name)

if c2.button("📊 Tasks (.csv)"):
    p = export_tasks_csv()
    st.success(f"Saved: {p}")
    st.download_button("Download tasks", p.read_bytes(), file_name=p.name)

if c3.button("🧾 Full report"):
    r = compute()   # removed user_id

    summary = {
        "Task completion %": f"{r['task_pct']:.0f}",
        "Quiz average %": f"{r['quiz_avg']:.0f}",
        "Revision done %": f"{r['rev_pct']:.0f}",
        "Composite": f"{r['score']:.0f}",
        "Prediction": r["label"]
    }

    p = export_report_pdf("User", "User", summary)

    st.success(f"Saved: {p}")
    st.download_button("Download report", p.read_bytes(), file_name=p.name)

st.divider()

# -------------------------
# DANGER ZONE (GLOBAL RESET)
# -------------------------
st.subheader("Danger zone")

if st.checkbox("I understand this will erase ALL data (global mode)."):
    if st.button("🧹 Clear all data"):
        for key in ("tasks", "notes", "quiz_history", "revision"):
            save(key, [])   # clear everything globally

        st.success("All data cleared successfully.")
