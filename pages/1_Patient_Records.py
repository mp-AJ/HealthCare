import streamlit as st
from db import get_connection

def load_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, age, gender, diagnosis FROM patients")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_patient(name, age, gender, diagnosis):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients (name, age, gender, diagnosis) VALUES (?, ?, ?, ?)",
                   (name, age, gender, diagnosis))
    conn.commit()
    conn.close()

with st.sidebar:
    "[![Open in GitHub Codespaces](https://github.com/codespaces/tree.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"



st.title("🧾 Patient Records")

with st.form("Add Patient"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    diagnosis = st.text_input("Diagnosis")
    if st.form_submit_button("Add"):
        add_patient(name, age, gender, diagnosis)
        st.success("Patient added.")

st.subheader("📋 All Patients")
data = load_patients()
st.table(data)
