"""Rule-based performance predictor."""
from .file_db import load


def compute(user_id):
    tasks = [t for t in load("tasks") if t.get("user_id") == user_id]
    quizzes = [q for q in load("quiz_history") if q.get("user_id") == user_id]
    revs = [r for r in load("revision") if r.get("user_id") == user_id]

    task_pct = (sum(1 for t in tasks if t.get("done")) / len(tasks) * 100) if tasks else 0
    quiz_avg = (sum(q.get("pct", 0) for q in quizzes) / len(quizzes)) if quizzes else 0
    rev_pct = (sum(1 for r in revs if r.get("status") == "completed") / len(revs) * 100) if revs else 0

    score = task_pct * 0.4 + quiz_avg * 0.4 + rev_pct * 0.2
    if score >= 80: label = "Excellent"
    elif score >= 60: label = "Good"
    elif score >= 40: label = "Average"
    else: label = "Needs Improvement"
    return {"task_pct": task_pct, "quiz_avg": quiz_avg, "rev_pct": rev_pct,
            "score": score, "label": label}
