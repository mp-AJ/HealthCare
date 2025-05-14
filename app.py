import streamlit as st
from auth import login, logout
from db import init_db

init_db()

st.set_page_config(page_title="Healthcare App", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

if not st.session_state.logged_in:
    login()
else:
    st.sidebar.success("Logged in as: " + st.session_state.get("username", ""))
    if st.sidebar.button("Logout"):
        logout()
    st.title("🏥 Welcome to the Healthcare Streamlit App")
    st.write("Use the sidebar to navigate to different sections.")
