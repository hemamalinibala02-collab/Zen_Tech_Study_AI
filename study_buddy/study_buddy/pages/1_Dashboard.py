import streamlit as st
from datetime import date
from utils.file_db import load

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")

# Load data (no user filtering)
tasks = load("tasks")
notes = load("notes")
quizzes = load("quiz_history")
revs = load("revision")

today = date.today().isoformat()
due_revs = [
    r for r in revs
    if r.get("next_date", "") <= today and r.get("status") != "completed"
]

st.title("🏠 Welcome to ZenTech AI Dashboard")

# Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Tasks", len(tasks))
c2.metric("Completed", sum(1 for t in tasks if t.get("done")))
c3.metric("Pending", sum(1 for t in tasks if not t.get("done")))
c4.metric("Due Revisions", len(due_revs))

st.divider()

# Quiz section
st.subheader("📊 Recent quiz scores")
if quizzes:
    for q in quizzes[-5:][::-1]:
        st.write(f"**{q.get('topic','?')}** — {q.get('score')}/{q.get('total')} ({q.get('pct',0):.0f}%)")
else:
    st.info("No quizzes taken yet.")

st.subheader("⚡ Quick actions")

a, b, c, d = st.columns(4)
a.page_link("pages/2_Study_Planner.py", label="➕ Add Task")
b.page_link("pages/3_My_Notes.py", label="📝 New Note")
c.page_link("pages/5_AI_Tutor.py", label="🤖 Ask Tutor")
d.page_link("pages/6_Quiz.py", label="🧠 Take Quiz")
