import streamlit as st
from utils.auth import require_login, current_user
from utils.prediction_utils import compute

st.set_page_config(page_title="Prediction", page_icon="🔮", layout="wide")
require_login()
u = current_user()

st.title("🔮 Performance Prediction")
r = compute(u["id"])

c1, c2, c3 = st.columns(3)
c1.metric("Task completion", f"{r['task_pct']:.0f}%")
c2.metric("Quiz average", f"{r['quiz_avg']:.0f}%")
c3.metric("Revision done", f"{r['rev_pct']:.0f}%")

st.progress(min(r["score"]/100, 1.0), text=f"Composite score: {r['score']:.0f}/100")

label = r["label"]
color = {"Excellent": "🟢", "Good": "🔵", "Average": "🟡", "Needs Improvement": "🔴"}[label]
st.subheader(f"{color} Prediction: **{label}**")

tips = {
    "Excellent": "Keep up the great rhythm — try teaching a friend to deepen mastery.",
    "Good": "Solid! Add one extra revision session per week.",
    "Average": "Aim to complete pending tasks and take 2 quizzes this week.",
    "Needs Improvement": "Start small: pick 3 tasks, finish them today, then take a quick quiz.",
}
st.info(tips[label])
