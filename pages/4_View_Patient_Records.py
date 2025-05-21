import streamlit as st
import sqlite3
import pandas as pd

# Connect to database
def get_connection():
    conn = sqlite3.connect("healthcare.db", check_same_thread=False)
    return conn

conn = get_connection()
cursor = conn.cursor()

# Create patients table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    description TEXT,
    status TEXT
)
""")
conn.commit()

st.title("📝 Patient Records")

# Search bar and logout
col1, col2 = st.columns([3, 1])
with col1:
    search_term = st.text_input("Search Patient Records")
with col2:
    st.button("Logout")

# Fetch patient records
if search_term:
    records = pd.read_sql_query("SELECT * FROM patients WHERE description LIKE ?", conn, params=('%'+search_term+'%',))
else:
    records = pd.read_sql_query("SELECT * FROM patients", conn)

# Display table
st.markdown("### Patient Records")
st.dataframe(records)

# Add/Edit/Delete Section
st.markdown("### Add New Record")
with st.form("add_patient"):
    date = st.date_input("Date")
    description = st.text_input("Description")
    status = st.selectbox("Status", ["Pending", "Completed", "Follow-up"])
    submitted = st.form_submit_button("Add Record")

    if submitted:
        cursor.execute("INSERT INTO patients (date, description, status) VALUES (?, ?, ?)", (str(date), description, status))
        conn.commit()
        st.success("Record added successfully.")

# Edit and Delete buttons (advanced: could link with dropdowns or selection)
st.markdown("### Edit/Delete (Coming Soon)")

# Close connection
conn.close()
