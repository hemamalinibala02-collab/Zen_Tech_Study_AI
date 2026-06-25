import json
import random
import re
import streamlit as st
from openai import OpenAI


# -------------------------
# API KEY (CLOUD SAFE)
# -------------------------
OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")


# -------------------------
# GENERATE QUIZ
# -------------------------
def generate_quiz(source_text: str, n_q: int = 5):
    source_text = source_text.strip()

    # ---------- DEMO MODE ----------
    if not OPENROUTER_API_KEY:
        words = [w.strip(".,!?") for w in source_text.split() if len(w) > 3]
        unique_words = list(set(words))
        random.shuffle(unique_words)

        quiz = []
        count = min(n_q, len(unique_words)) if unique_words else n_q

        for i in range(count):
            word = unique_words[i] if unique_words else f"Topic {i+1}"
            quiz.append({
                "q": f"What is related to '{word}'?",
                "type": "mcq",
                "options": [word, "Option A", "Option B", "Option C"],
                "answer": 0
            })

        while len(quiz) < n_q:
            quiz.append({
                "q": f"Sample question {random.randint(1,1000)}?",
                "type": "tf",
                "answer": random.choice([True, False])
            })

        return quiz

    # ---------- OPENROUTER MODE ----------
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )

        prompt = f"""
Create {n_q} quiz questions.

Return ONLY valid JSON array.

Formats:
MCQ: {{"q":"question","type":"mcq","options":["A","B","C","D"],"answer":0}}
TF: {{"q":"question","type":"tf","answer":true}}

Content:
{source_text[:3000]}
"""

        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",
            messages=[
                {"role": "system", "content": "You create quizzes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        # ---------- SAFE JSON PARSING ----------
        match = re.search(r"\[.*\]", content, re.S)
        if not match:
            return []

        quiz = json.loads(match.group())

        # remove duplicates
        seen = set()
        unique = []
        for q in quiz:
            text = q.get("q", "").lower()
            if text and text not in seen:
                seen.add(text)
                unique.append(q)

        return unique[:n_q]

    except Exception as e:
        return []


# -------------------------
# GRADING (SAFE)
# -------------------------
def grade(quiz, answers):
    score = 0
    details = []

    for i, q in enumerate(quiz):
        user_ans = answers[i] if i < len(answers) else None
        correct = q.get("answer")
        ok = user_ans == correct

        if ok:
            score += 1

        # safe formatting
        if q["type"] == "mcq":
            if isinstance(correct, int) and 0 <= correct < len(q.get("options", [])):
                correct_text = q["options"][correct]
            else:
                correct_text = correct

            if isinstance(user_ans, int) and 0 <= user_ans < len(q.get("options", [])):
                user_text = q["options"][user_ans]
            else:
                user_text = user_ans
        else:
            correct_text = correct
            user_text = user_ans

        details.append({
            "q": q["q"],
            "correct": correct_text,
            "your": user_text,
            "ok": ok
        })

    return score, details
