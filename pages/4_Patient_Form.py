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

# Session state for refresh triggers
if 'data_changed' not in st.session_state:
    st.session_state.data_changed = False

# Sidebar for Add/Edit
st.sidebar.title("🔧 Patient Actions")
action = st.sidebar.radio("Choose Action", ["Add New", "Edit Existing"])

# --- ADD NEW ---
if action == "Add New":
    with st.sidebar.form("add_form", clear_on_submit=True):
        patient = st.text_input("Patient Name")
        date = st.date_input("Date")
        desc = st.text_area("Description")
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
        submit = st.form_submit_button("Save")
        if submit:
            cursor.execute(
                "INSERT INTO patient_status (patient_name, date, description, status) VALUES (?, ?, ?, ?)",
                (patient, date.isoformat(), desc, status))
            conn.commit()
            st.session_state.data_changed = True
            st.sidebar.success("✅ Patient status added.")

# --- EDIT EXISTING ---
elif action == "Edit Existing":
    search_edit = st.sidebar.text_input("Search by patient name")
    if search_edit:
        df_edit = pd.read_sql(
            "SELECT * FROM patient_status WHERE patient_name LIKE ?",
            conn,
            params=(f"%{search_edit}%",)
        )

        if df_edit.empty:
            st.sidebar.info("No matching records.")
        else:
            selected_id = st.sidebar.selectbox(
                "Select Record ID to Edit",
                df_edit["id"],
                format_func=lambda x: f"{df_edit[df_edit['id'] == x]['patient_name'].values[0]} (ID {x})"
            )
            record = df_edit[df_edit['id'] == selected_id].iloc[0]

            with st.sidebar.form("edit_form"):
                patient = st.text_input("Patient Name", record['patient_name'])
                date = st.date_input("Date", pd.to_datetime(record['date']))
                desc = st.text_area("Description", record['description'])
                status = st.selectbox(
                    "Status", ["Pending", "In Progress", "Completed"],
                    index=["Pending", "In Progress", "Completed"].index(record['status'])
                )
                submit_edit = st.form_submit_button("Update")
                if submit_edit:
                    cursor.execute("""
                        UPDATE patient_status 
                        SET patient_name = ?, date = ?, description = ?, status = ?
                        WHERE id = ?
                    """, (patient, date.isoformat(), desc, status, selected_id))
                    conn.commit()
                    st.session_state.data_changed = True
                    st.sidebar.success("✅ Patient status updated.")

# --- MAIN DISPLAY ---
st.title("📋 Patient Status Board")

# Refresh data if changed
if st.session_state.data_changed:
    st.session_state.data_changed = False

# Search bar
search = st.text_input("Search by patient name")
query = "SELECT * FROM patient_status"
params = ()
if search:
    query += " WHERE patient_name LIKE ?"
    params = (f"%{search}%",)

df = pd.read_sql(query, conn, params=params)

# Display results
if not df.empty:
    st.dataframe(df[['date', 'description', 'status']])
    selected = st.selectbox("Select a record for details", df['id'])
    selected_record = df[df['id'] == selected].iloc[0]

    st.subheader("📌 Detail")
    st.write(f"**Patient:** {selected_record['patient_name']}")
    st.write(f"**Date:** {selected_record['date']}")
    st.write(f"**Description:** {selected_record['description']}")
    st.write(f"**Status:** {selected_record['status']}")

    # Delete confirmation
    if st.button("🗑️ Delete this record"):
        if st.checkbox("Confirm delete?"):
            cursor.execute("DELETE FROM patient_status WHERE id = ?", (selected,))
            conn.commit()
            st.session_state.data_changed = True
            st.success("✅ Record deleted.")
else:
    st.info("No records found.")

# Simulated logout
st.sidebar.markdown("---")
st.sidebar.button("🔒 Logout")
