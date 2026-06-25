import streamlit as st
from datetime import date
from utils.file_db import load, save, next_id

st.set_page_config(page_title="Study Planner", page_icon="🗓️", layout="wide")

st.title("🗓️ Study Planner")

# ➕ ADD TASK
with st.expander("➕ Add new task", expanded=True):
    with st.form("add_task"):
        c1, c2 = st.columns(2)

        title = c1.text_input("Task title")
        subject = c2.text_input("Subject")

        c3, c4 = st.columns(2)
        deadline = c3.date_input("Deadline", value=date.today())
        priority = c4.selectbox("Priority", ["High", "Medium", "Low"], index=1)

        if st.form_submit_button("Add task"):
            if not title.strip():
                st.error("Title required.")
            else:
                tasks = load("tasks")

                tasks.append({
                    "id": next_id(tasks),
                    "title": title.strip(),
                    "subject": subject.strip(),
                    "deadline": deadline.isoformat(),
                    "priority": priority,
                    "done": False
                })

                save("tasks", tasks)
                st.success("Task added.")
                st.rerun()

# 📋 LOAD TASKS (NO USER FILTER)
tasks = load("tasks")

# 🔍 FILTERS
f1, f2 = st.columns(2)
subj_filter = f1.text_input("Filter by subject")
status_filter = f2.selectbox("Status", ["All", "Pending", "Completed"])

view = tasks

if subj_filter:
    view = [
        t for t in view
        if subj_filter.lower() in (t.get("subject") or "").lower()
    ]

if status_filter == "Pending":
    view = [t for t in view if not t.get("done")]
elif status_filter == "Completed":
    view = [t for t in view if t.get("done")]

# 📊 PROGRESS BAR
if tasks:
    pct = sum(1 for t in tasks if t.get("done")) / len(tasks)
    st.progress(pct, text=f"Progress: {pct*100:.0f}%")

# 📌 SHOW TASKS
st.subheader("Your tasks")

if not view:
    st.info("No tasks match.")

for t in view:
    cols = st.columns([0.06, 0.5, 0.18, 0.12, 0.07, 0.07])

    new_done = cols[0].checkbox(
        "Done",
        value=t.get("done", False),
        key=f"d{t['id']}",
        label_visibility="collapsed"
    )

    cols[1].markdown(f"**{t['title']}**  \n_{t.get('subject','')}_")
    cols[2].write(t.get("deadline", ""))
    cols[3].write(t.get("priority", ""))

    if cols[4].button("✏️", key=f"e{t['id']}"):
        st.session_state["edit_task"] = t["id"]

    delete = cols[5].button("🗑️", key=f"x{t['id']}")

    # ✅ UPDATE DONE STATUS
    if new_done != t.get("done"):
        all_tasks = load("tasks")
        for x in all_tasks:
            if x["id"] == t["id"]:
                x["done"] = new_done
        save("tasks", all_tasks)
        st.rerun()

    # ❌ DELETE TASK
    if delete:
        save("tasks", [x for x in load("tasks") if x["id"] != t["id"]])
        st.rerun()

# ✏️ EDIT TASK
if st.session_state.get("edit_task"):
    tid = st.session_state["edit_task"]
    cur = next((x for x in load("tasks") if x["id"] == tid), None)

    if cur:
        with st.form("edit_form"):
            st.subheader(f"Edit task #{tid}")

            title = st.text_input("Title", cur["title"])
            subject = st.text_input("Subject", cur.get("subject", ""))

            priority = st.selectbox(
                "Priority",
                ["High", "Medium", "Low"],
                index=["High", "Medium", "Low"].index(cur.get("priority", "Medium"))
            )

            if st.form_submit_button("Save"):
                all_tasks = load("tasks")

                for x in all_tasks:
                    if x["id"] == tid:
                        x.update({
                            "title": title,
                            "subject": subject,
                            "priority": priority
                        })

                save("tasks", all_tasks)
                del st.session_state["edit_task"]
                st.rerun()
