import streamlit as st
from db import get_connection

if st.session_state.get("role") != "admin":
    st.warning("Admin access only.")
    st.stop()

st.title("🔐 Admin Panel")

st.subheader("Registered Users")
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT id, username, role FROM users")
rows = cursor.fetchall()
st.table(rows)

st.subheader("Add New User")
with st.form("Add User"):
    username = st.text_input("Username")
    password = st.text_input("Password")
    role = st.selectbox("Role", ["admin", "user"])
    if st.form_submit_button("Create User"):
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           (username, password, role))
            conn.commit()
            st.success("User added.")
        except Exception as e:
            st.error("Error: " + str(e))
