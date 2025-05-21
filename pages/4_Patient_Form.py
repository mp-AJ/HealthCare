import streamlit as st
import sqlite3

st.title("📝 Add Detailed Patient Form")

# Connect to database
conn = sqlite3.connect('healthcare.db', check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS detailed_patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    address TEXT,
    phone TEXT,
    complaint TEXT,
    diagnosis TEXT,
    treatment TEXT
)
""")
conn.commit()

with st.form("patient_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        gender = st.radio("Gender", ["Male", "Female", "Other"])

    with col2:
        address = st.text_area("Address")
        phone = st.text_input("Phone Number")

    complaint = st.text_area("Chief Complaint")
    diagnosis = st.text_area("Diagnosis")
    treatment = st.text_area("Treatment Plan")

    submitted = st.form_submit_button("Submit")

    if submitted:
        cursor.execute("""
            INSERT INTO detailed_patients (name, age, gender, address, phone, complaint, diagnosis, treatment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, age, gender, address, phone, complaint, diagnosis, treatment))
        conn.commit()
        st.success("✅ Patient record added successfully.")

conn.close()
