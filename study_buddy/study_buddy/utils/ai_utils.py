"""OpenAI wrapper with safe demo-mode fallback."""
import os
from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI
import os


def _get_key():
    return os.getenv("OPENROUTER_API_KEY")


def has_api_key():
    return bool(_get_key())

def ask_ai(prompt: str, system: str = "You are a friendly study tutor for students.") -> str:
    key = _get_key()

    if not key:
        return "No API key configured"

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key,
    )

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",  # you can change model here
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            extra_headers={
                "HTTP-Referer": "http://localhost",  # required by OpenRouter
                "X-Title": "ZenTech AI"
            }
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"


def _demo(prompt: str) -> str:
    return (
        f"**Demo response** (API key not configured)\n\n"
        f"Here is a sample explanation for: _{prompt[:200]}_\n\n"
        "- Key idea 1: break the topic into small parts.\n"
        "- Key idea 2: connect it to something you already know.\n"
        "- Key idea 3: practice with a quick example.\n\n"
        "Set OPENAI_API_KEY in your .env to enable real AI answers."
    )


def ask_ai(prompt: str, system: str = "You are a friendly study tutor for students.") -> str:
    key = _get_key()
    if not key:
        return _demo(prompt)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        resp = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt}],
            temperature=0.5,
        )
        return resp.choices[0].message.content or _demo(prompt)
    except Exception as e:
        return f"REAL ERROR:\n{str(e)}"
