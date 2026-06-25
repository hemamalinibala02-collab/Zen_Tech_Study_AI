"""Rule-based performance predictor (global mode)."""
from .file_db import load


def compute():
    tasks = load("tasks")
    quizzes = load("quiz_history")
    revs = load("revision")

    task_pct = (
        sum(1 for t in tasks if t.get("done")) / len(tasks) * 100
        if tasks else 0
    )

    quiz_avg = (
        sum(q.get("pct", 0) for q in quizzes) / len(quizzes)
        if quizzes else 0
    )

    rev_pct = (
        sum(1 for r in revs if r.get("status") == "completed") / len(revs) * 100
        if revs else 0
    )

    score = task_pct * 0.4 + quiz_avg * 0.4 + rev_pct * 0.2

    if score >= 80:
        label = "Excellent"
    elif score >= 60:
        label = "Good"
    elif score >= 40:
        label = "Average"
    else:
        label = "Needs Improvement"

    return {
        "task_pct": task_pct,
        "quiz_avg": quiz_avg,
        "rev_pct": rev_pct,
        "score": score,
        "label": label
    }
