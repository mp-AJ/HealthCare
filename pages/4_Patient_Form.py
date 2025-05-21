import streamlit as st
import sqlite3
import pandas as pd

# Connect to DB
conn = sqlite3.connect('healthcare.db', check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS patient_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT,
    date TEXT,
    description TEXT,
    status TEXT
)
""")
conn.commit()

# Sidebar for Add/Edit
st.sidebar.title("🔧 Patient Actions")
action = st.sidebar.radio("Choose Action", ["Add New", "Edit Existing"])

if action == "Add New":
    with st.sidebar.form("add_form"):
        patient = st.text_input("Patient Name")
        date = st.date_input("Date")
        desc = st.text_area("Description")
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
        submit = st.form_submit_button("Save")
        if submit:
            cursor.execute("INSERT INTO patient_status (patient_name, date, description, status) VALUES (?, ?, ?, ?)",
                           (patient, date.isoformat(), desc, status))
            conn.commit()
            st.success("✅ Patient status added.")

# Main Layout
st.title("📋 Patient Status Board")

# Search
search = st.text_input("Search by patient name")

query = "SELECT * FROM patient_status"
if search:
    query += f" WHERE patient_name LIKE '%{search}%'"
df = pd.read_sql(query, conn)

# Display table and details
if not df.empty:
    st.dataframe(df[['date', 'description', 'status']])
    selected = st.selectbox("Select a record for details", df['id'])
    selected_record = df[df['id'] == selected].iloc[0]

    st.subheader("📌 Detail")
    st.write(f"**Patient:** {selected_record['patient_name']}")
    st.write(f"**Date:** {selected_record['date']}")
    st.write(f"**Description:** {selected_record['description']}")
    st.write(f"**Status:** {selected_record['status']}")

    # Delete button
    if st.button("🗑️ Delete this record"):
        cursor.execute("DELETE FROM patient_status WHERE id = ?", (selected,))
        conn.commit()
        st.success("Record deleted successfully!")
        st.experimental_rerun()  # Refresh the app to update the data shown
else:
    st.info("No records found.")

# Right-aligned Logout (simulate)
st.sidebar.markdown("---")
st.sidebar.button("🔒 Logout")
