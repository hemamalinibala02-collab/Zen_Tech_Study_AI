"""Auth helpers using passlib bcrypt + JSON storage."""
from passlib.hash import bcrypt
import streamlit as st
from .file_db import load, save, next_id


def register(name, email, password):
    email = email.strip().lower()
    if not name or not email or not password:
        return False, "All fields are required."
    users = load("users")
    if any(u["email"] == email for u in users):
        return False, "Email already registered."
    users.append({
        "id": next_id(users),
        "name": name.strip(),
        "email": email,
        "password": bcrypt.hash(password),
        "theme": "Light",
    })
    save("users", users)
    return True, "Account created. Please log in."


def login(email, password):
    email = email.strip().lower()
    users = load("users")
    for u in users:
        if u["email"] == email:
            try:
                if bcrypt.verify(password, u["password"]):
                    st.session_state["user"] = {"id": u["id"], "name": u["name"], "email": u["email"]}
                    return True, "Welcome back!"
            except Exception:
                return False, "Invalid credentials."
    return False, "Invalid email or password."


def logout():
    st.session_state.pop("user", None)


def current_user():
    return st.session_state.get("user")


def require_login():
    if not current_user():
        st.warning("Please log in from the home page to continue.")
        st.stop()
