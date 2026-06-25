"""Export helpers: txt / csv / pdf report."""
import csv, io
from pathlib import Path
from .file_db import EXPORTS, load


def export_notes_txt(user_id) -> Path:
    notes = [n for n in load("notes") if n.get("user_id") == user_id]
    out = EXPORTS / f"notes_user_{user_id}.txt"
    with out.open("w", encoding="utf-8") as f:
        for n in notes:
            f.write(f"# {n.get('title','Untitled')} ({n.get('subject','')})\n")
            f.write((n.get("content") or "") + "\n\n---\n\n")
    return out


def export_tasks_csv(user_id) -> Path:
    tasks = [t for t in load("tasks") if t.get("user_id") == user_id]
    out = EXPORTS / f"tasks_user_{user_id}.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "title", "subject", "deadline", "priority", "done"])
        for t in tasks:
            w.writerow([t.get("id"), t.get("title"), t.get("subject"),
                        t.get("deadline"), t.get("priority"), t.get("done")])
    return out


def export_report_pdf(user_id, name, summary: dict) -> Path:
    out = EXPORTS / f"report_user_{user_id}.pdf"
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(str(out), pagesize=A4)
        w, h = A4
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, h - 60, f"ZenTech AI – Student Report")
        c.setFont("Helvetica", 12)
        c.drawString(50, h - 90, f"Student: {name}")
        y = h - 130
        for k, v in summary.items():
            c.drawString(50, y, f"{k}: {v}")
            y -= 22
        c.showPage(); c.save()
    except Exception:
        out = out.with_suffix(".txt")
        out.write_text(f"ZenTech AI Report\nStudent: {name}\n\n" +
                       "\n".join(f"{k}: {v}" for k, v in summary.items()))
    return out
