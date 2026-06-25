import streamlit as st
import pandas as pd
import plotly.express as px
from utils.file_db import load

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

st.title("📊 Analytics")

# 📦 LOAD DATA (GLOBAL)
tasks = load("tasks")
quizzes = load("quiz_history")
revs = load("revision")

c1, c2 = st.columns(2)

# 📊 TASK ANALYTICS
if tasks:
    df = pd.DataFrame(tasks)

    pie = df["done"].map({True: "Completed", False: "Pending"}).value_counts().reset_index()
    pie.columns = ["status", "count"]

    c1.plotly_chart(
        px.pie(pie, names="status", values="count", title="Tasks status"),
        use_container_width=True
    )

    subj = df.groupby(df["subject"].fillna("Unknown")).size().reset_index(name="count")

    c2.plotly_chart(
        px.bar(subj, x="subject", y="count", title="Tasks by subject"),
        use_container_width=True
    )

else:
    st.info("Add tasks to see analytics.")

# 📈 QUIZ ANALYTICS
if quizzes:
    df = pd.DataFrame(quizzes)

    if "at" not in df.columns:
        df["at"] = range(len(df))  # fallback if timestamp missing

    st.plotly_chart(
        px.line(df, x="at", y="pct", markers=True, title="Quiz score trend (%)"),
        use_container_width=True
    )

# 🔁 REVISION ANALYTICS
if revs:
    df = pd.DataFrame(revs)

    rs = df["status"].value_counts().reset_index()
    rs.columns = ["status", "count"]

    st.plotly_chart(
        px.bar(rs, x="status", y="count", title="Revision status"),
        use_container_width=True
    )
