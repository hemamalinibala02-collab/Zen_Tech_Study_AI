import streamlit as st
from utils.file_db import load
from utils.quiz_utils import generate_quiz, grade

st.set_page_config(page_title="Quiz", page_icon="🧠", layout="wide")

st.title("🧠 Quiz Generator")

# 📚 LOAD ALL NOTES (NO USER FILTER)
notes = load("notes")

note_titles = ["(none)"] + [f"{n['id']} – {n['title']}" for n in notes]

c1, c2 = st.columns(2)

topic = c1.text_input("Topic")
chosen = c2.selectbox("…or pick from notes", note_titles)

n_q = st.slider("Number of questions", 3, 10, 5)

# 🚀 GENERATE QUIZ
if st.button("Generate quiz"):
    src = topic

    if chosen != "(none)":
        nid = int(chosen.split(" – ")[0])
        n = next((x for x in notes if x["id"] == nid), None)

        if n:
            src = f"{n['title']}: {n.get('content','')[:500]}"

    if not src.strip():
        st.error("Enter a topic or pick a note.")
    else:
        st.session_state.quiz = generate_quiz(src, n_q)
        st.session_state.quiz_topic = topic or chosen
        st.session_state.answers = [None] * len(st.session_state.quiz)

# 🧠 SHOW QUIZ
if st.session_state.get("quiz"):
    st.subheader("Answer the questions")

    for i, q in enumerate(st.session_state.quiz):
        st.markdown(f"**Q{i+1}. {q['q']}**")

        if q["type"] == "mcq":
            opts = q.get("options", [])
            sel = st.radio("Choose", opts, key=f"a{i}", index=None)
            st.session_state.answers[i] = opts.index(sel) if sel in opts else None

        elif q["type"] == "tf":
            sel = st.radio("True or False", ["True", "False"], key=f"a{i}", index=None)
            st.session_state.answers[i] = (sel == "True") if sel else None

        else:
            st.session_state.answers[i] = st.text_input("Your answer", key=f"a{i}")

    # 📊 SUBMIT QUIZ
    if st.button("Submit quiz"):
        score, details = grade(
            st.session_state.quiz,
            st.session_state.answers
        )

        total = len(st.session_state.quiz)
        pct = score / total * 100

        st.success(f"Score: {score}/{total} ({pct:.0f}%)")

        for d in details:
            ico = "✅" if d["ok"] else "❌"
            st.write(f"{ico} **{d['q']}** — correct: `{d['correct']}`, you: `{d['your']}`")

        # 🧾 SAVE HISTORY (GLOBAL)
        hist = load("quiz_history")

        hist.append({
            "topic": st.session_state.get("quiz_topic", "Quiz"),
            "score": score,
            "total": total,
            "pct": pct
        })

        st.success("Quiz saved to history!")
        st.session_state.quiz = None
