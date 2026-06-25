import requests
import streamlit as st

API_URL = "https://YOUR-RENDER-URL.onrender.com"


def register(name, email, password):
    try:
        res = requests.post(
            f"{API_URL}/auth/register",
            json={
                "email": email,
                "username": name,
                "password": password
            }
        )

        if res.status_code == 200:
            return True, "Account created successfully"

        return False, res.json().get("detail", "Registration failed")

    except Exception as e:
        return False, str(e)


def login(email, password):
    try:
        res = requests.post(
            f"{API_URL}/auth/login",
            data={
                "username": email,
                "password": password
            }
        )

        if res.status_code == 200:
            token = res.json()["access_token"]
            st.session_state["token"] = token
            st.session_state["user"] = email
            return True, "Login successful"

        return False, res.json().get("detail", "Invalid credentials")

    except Exception as e:
        return False, str(e)


def logout():
    st.session_state.clear()


def current_user():
    return st.session_state.get("user")
