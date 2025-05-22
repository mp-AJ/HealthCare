import streamlit as st
import sqlite3
import pandas as pd

# DB Connection
conn = sqlite3.connect("healthcare.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    contact TEXT,
    date TEXT,
    description TEXT,
    status TEXT
)
""")
conn.commit()

st.title("🗂️ Patient Records")

# Logout Button (simulate session)
if st.button("🔒 Logout"):
    st.success("Logged out (simulated)")

# Search bar
search_query = st.text_input("🔍 Search Patient by Name")

# Query DB
query = "SELECT * FROM patients"
if search_query:
    query += f" WHERE name LIKE '%{search_query}%'"
df = pd.read_sql(query, conn)

# Patient Table
if not df.empty:
    st.write("### Patient Records")
    selected_row = st.radio("Select a patient record:", df['id'], format_func=lambda x: df[df['id'] == x]['name'].values[0])

    st.dataframe(df[['date', 'description', 'status']])

    if selected_row:
        patient = df[df['id'] == selected_row].iloc[0]
        st.write("### 📄 Patient Details")
        st.markdown(f"""
        - **Name:** {patient['name']}
        - **Age:** {patient['age']}
        - **Gender:** {patient['gender']}
        - **Contact:** {patient['contact']}
        - **Status:** {patient['status']}
        """)
        if st.button("📝 Edit Record"):
            st.warning("Edit logic to be implemented.")
        if st.button("🗑️ Delete Record"):
            cursor.execute("DELETE FROM patients WHERE id = ?", (selected_row,))
            conn.commit()
            st.success("Record deleted.")
            st.experimental_rerun()
else:
    st.info("No patient records found.")

# Add new record button
if st.button("➕ Add New Patient"):
    with st.form("new_patient_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        contact = st.text_input("Contact")
        date = st.date_input("Date")
        description = st.text_area("Description")
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
        submit = st.form_submit_button("Save")
        if submit:
            cursor.execute("""
            INSERT INTO patients (name, age, gender, contact, date, description, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (name, age, gender, contact, date.isoformat(), description, status))
            conn.commit()
            st.success("✅ Patient added successfully!")
            st.experimental_rerun()
