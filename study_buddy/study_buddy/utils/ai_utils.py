"""OpenRouter AI wrapper (Streamlit Cloud safe)."""

import os
import streamlit as st
from openai import OpenAI


# -------------------------
# GET API KEY (LOCAL + CLOUD)
# -------------------------
def _get_key():
    return st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")


def has_api_key():
    return bool(_get_key())


# -------------------------
# DEMO MODE
# -------------------------
def _demo(prompt: str) -> str:
    return (
        f"**Demo response (No API key)**\n\n"
        f"Topic: {prompt[:200]}\n\n"
        "- Break the topic into small parts\n"
        "- Learn step by step\n"
        "- Practice with examples\n"
    )


# -------------------------
# MAIN AI FUNCTION
# -------------------------
def ask_ai(prompt: str, system: str = "You are a friendly study tutor.") -> str:
    key = _get_key()

    if not key:
        return _demo(prompt)

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=key,
        )

        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            extra_headers={
                "HTTP-Referer": "https://streamlit.io",
                "X-Title": "ZenTech Study AI"
            }
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"
