import streamlit as st
from db import get_connection

def load_appointments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT patient_name as Name, date as Date, doctor as Doctor FROM appointments")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_appointment(patient_name, date, doctor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO appointments (patient_name, date, doctor) VALUES (?, ?, ?)",
                   (patient_name, date, doctor))
    conn.commit()
    conn.close()

st.title("📅 Appointments")

with st.form("Schedule Appointment"):
    patient_name = st.text_input("Patient Name")
    date = st.date_input("Date")
    doctor = st.text_input("Doctor")
    if st.form_submit_button("Schedule"):
        add_appointment(patient_name, str(date), doctor)
        st.success("Appointment scheduled.")

st.subheader("📋 Scheduled Appointments")
data = load_appointments()
st.table(data)
