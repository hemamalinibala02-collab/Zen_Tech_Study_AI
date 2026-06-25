import streamlit as st
from datetime import date
from utils.file_db import load

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")


tasks = [t for t in load("tasks") if t.get("user_id") == u["id"]]
notes = [n for n in load("notes") if n.get("user_id") == u["id"]]
quizzes = [q for q in load("quiz_history") if q.get("user_id") == u["id"]]
revs = [r for r in load("revision") if r.get("user_id") == u["id"]]

today = date.today().isoformat()
due_revs = [r for r in revs if r.get("next_date", "") <= today and r.get("status") != "completed"]

st.title(f"🏠 Welcome, {u['name']}")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Tasks", len(tasks))
c2.metric("Completed", sum(1 for t in tasks if t.get("done")))
c3.metric("Pending", sum(1 for t in tasks if not t.get("done")))
c4.metric("Due Revisions", len(due_revs))

st.divider()
st.subheader("Recent quiz scores")
if quizzes:
    for q in quizzes[-5:][::-1]:
        st.write(f"**{q.get('topic','?')}** — {q.get('score')}/{q.get('total')} ({q.get('pct',0):.0f}%)")
else:
    st.info("No quizzes taken yet.")

st.subheader("Quick actions")
a, b, c, d = st.columns(4)
a.page_link("pages/2_Study_Planner.py", label="➕ Add Task")
b.page_link("pages/3_My_Notes.py", label="📝 New Note")
c.page_link("pages/5_AI_Tutor.py", label="🤖 Ask Tutor")
d.page_link("pages/6_Quiz.py", label="🧠 Take Quiz")
