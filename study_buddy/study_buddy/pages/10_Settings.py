import streamlit as st
from utils.auth import require_login, current_user
from utils.file_db import load, save
from utils.export_utils import export_notes_txt, export_tasks_csv, export_report_pdf
from utils.prediction_utils import compute

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")


st.title("⚙️ Settings & Export")

st.subheader("Profile")
users = load("users")
me = next(x for x in users if x["id"] == u["id"])
new_name = st.text_input("Display name", me["name"])
theme = st.selectbox("Theme preference", ["Light", "Dark", "System"],
                     index=["Light","Dark","System"].index(me.get("theme", "Light")))
if st.button("Save profile"):
    me["name"] = new_name; me["theme"] = theme
    save("users", users)
    st.session_state["user"]["name"] = new_name
    st.success("Profile updated.")

st.divider()
st.subheader("Export")
c1, c2, c3 = st.columns(3)
if c1.button("📄 Notes (.txt)"):
    p = export_notes_txt(u["id"]); st.success(f"Saved: {p}")
    st.download_button("Download notes", p.read_bytes(), file_name=p.name)
if c2.button("📊 Tasks (.csv)"):
    p = export_tasks_csv(u["id"]); st.success(f"Saved: {p}")
    st.download_button("Download tasks", p.read_bytes(), file_name=p.name)
if c3.button("🧾 Full report"):
    r = compute(u["id"])
    summary = {"Task completion %": f"{r['task_pct']:.0f}",
               "Quiz average %": f"{r['quiz_avg']:.0f}",
               "Revision done %": f"{r['rev_pct']:.0f}",
               "Composite": f"{r['score']:.0f}",
               "Prediction": r["label"]}
    p = export_report_pdf(u["id"], u["name"], summary)
    st.success(f"Saved: {p}")
    st.download_button("Download report", p.read_bytes(), file_name=p.name)

st.divider()
st.subheader("Danger zone")
if st.checkbox("I understand this will erase my tasks, notes, quizzes, revisions."):
    if st.button("🧹 Clear my personal data"):
        for key in ("tasks", "notes", "quiz_history", "revision"):
            data = load(key)
            save(key, [x for x in data if x.get("user_id") != u["id"]])
        st.success("Personal data cleared.")
