import streamlit as st
from datetime import date, timedelta
from utils.file_db import load, save, next_id

st.set_page_config(page_title="Revision", page_icon="🔁", layout="wide")

st.title("🔁 Revision Tracker")

# ➕ ADD REVISION
with st.expander("➕ Add revision item", expanded=True):
    with st.form("addrev"):
        topic = st.text_input("Topic")
        subject = st.text_input("Subject")
        last = st.date_input("Last studied", value=date.today())
        gap = st.number_input("Days until next revision", 1, 60, 3)

        if st.form_submit_button("Add"):
            if not topic.strip():
                st.error("Topic required.")
            else:
                revs = load("revision")

                revs.append({
                    "id": next_id(revs),
                    "topic": topic,
                    "subject": subject,
                    "last_date": last.isoformat(),
                    "next_date": (last + timedelta(days=int(gap))).isoformat(),
                    "status": "upcoming"
                })

                save("revision", revs)
                st.success("Added.")
                st.rerun()

# 📦 LOAD ALL REVISION DATA (NO USER FILTER)
revs = load("revision")

today = date.today().isoformat()

# 🔁 UPDATE STATUS
for r in revs:
    if r["status"] != "completed":
        r["status"] = "due" if r["next_date"] <= today else "upcoming"

save("revision", revs)

# 📌 DISPLAY
for r in revs:
    cols = st.columns([0.4, 0.2, 0.15, 0.15, 0.1])

    cols[0].markdown(f"**{r['topic']}** _({r.get('subject','')})_")
    cols[1].write(f"Next: {r['next_date']}")
    cols[2].write(r["status"].upper())

    # ✅ MARK DONE
    if cols[3].button("Mark done", key=f"md{r['id']}"):
        all_r = load("revision")

        for x in all_r:
            if x["id"] == r["id"]:
                x["status"] = "completed"

        save("revision", all_r)
        st.rerun()

    # ❌ DELETE
    if cols[4].button("🗑️", key=f"rd{r['id']}"):
        save("revision", [x for x in load("revision") if x["id"] != r["id"]])
        st.rerun()
