import os
import json
import random
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") 


def generate_quiz(source_text: str, n_q: int = 5):
    source_text = source_text.strip()

    # ---------- DEMO MODE ----------
    # If API key is not set, generate random local quiz
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

        # if not enough words, fill extra random questions
        while len(quiz) < n_q:
            x = random.randint(1, 1000)
            quiz.append({
                "q": f"Sample question {x}?",
                "type": "tf",
                "answer": random.choice([True, False])
            })

        return quiz

    # ---------- OPENAI MODE ----------
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENROUTER_API_KEY)

        prompt = f"""
Create {n_q} UNIQUE quiz questions from the following study content.

Rules:
- Do NOT repeat questions.
- Mix MCQ and True/False.
- Return ONLY valid JSON array.
- Each item must be one of these formats:

MCQ:
{{"q":"question text","type":"mcq","options":["A","B","C","D"],"answer":0}}

True/False:
{{"q":"question text","type":"tf","answer":true}}

Study content:
{source_text[:3000]}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.9,
            messages=[
                {"role": "system", "content": "You create study quizzes."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content.strip()

        # remove markdown ```json if present
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        quiz = json.loads(content)

        # safety: remove duplicate questions
        seen = set()
        unique_quiz = []
        for q in quiz:
            q_text = q.get("q", "").strip().lower()
            if q_text and q_text not in seen:
                seen.add(q_text)
                unique_quiz.append(q)

        return unique_quiz[:n_q]

    except Exception:
        # fallback local random quiz
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

        return quiz


def grade(quiz, answers):
    score = 0
    details = []

    for i, q in enumerate(quiz):
        user_ans = answers[i] if i < len(answers) else None
        correct = q.get("answer")
        ok = user_ans == correct

        if ok:
            score += 1

        if q["type"] == "mcq":
            correct_text = q["options"][correct] if correct is not None and correct < len(q["options"]) else correct
            user_text = q["options"][user_ans] if isinstance(user_ans, int) and user_ans < len(q["options"]) else user_ans
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