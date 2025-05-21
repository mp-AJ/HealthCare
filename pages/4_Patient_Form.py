import streamlit as st
import sqlite3
import pandas as pd

# Connect to DB
conn = sqlite3.connect('healthcare.db', check_same_thread=False)
cursor = conn.cursor()

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

# Initialize session state flags and variables
if 'action_status' not in st.session_state:
    st.session_state.action_status = None  # Can be 'added', 'updated', 'deleted'

if 'edit_search' not in st.session_state:
    st.session_state.edit_search = ''

if 'edit_selected_id' not in st.session_state:
    st.session_state.edit_selected_id = None

st.sidebar.title("🔧 Patient Actions")
action = st.sidebar.radio("Choose Action", ["Add New", "Edit Existing"])

# --- ADD NEW ---
if action == "Add New":
    with st.sidebar.form("add_form", clear_on_submit=False):
        patient = st.text_input("Patient Name", key="add_patient")
        date = st.date_input("Date", key="add_date")
        desc = st.text_area("Description", key="add_desc")
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed"], key="add_status")
        save_clicked = st.form_submit_button("Save")

        if save_clicked:
            # Show confirmation modal
            with st.modal("Confirm Save"):
                st.write("Are you sure you want to save this patient status?")
                confirm = st.button("Yes, Save")
                cancel = st.button("Cancel")

                if confirm:
                    cursor.execute(
                        "INSERT INTO patient_status (patient_name, date, description, status) VALUES (?, ?, ?, ?)",
                        (patient, date.isoformat(), desc, status))
                    conn.commit()
                    st.session_state.action_status = 'added'
                    st.sidebar.success("✅ Patient status added.")
                    # Clear form inputs manually
                    st.session_state.add_patient = ""
                    st.session_state.add_desc = ""
                    st.session_state.add_status = "Pending"
                    st.session_state.add_date = pd.to_datetime("today")
                    st.experimental_rerun = False  # no rerun, just disable if you want
                    # close modal by not rendering it again
                if cancel:
                    st.experimental_rerun = False  # just close modal

# --- EDIT EXISTING ---
elif action == "Edit Existing":
    search_edit = st.sidebar.text_input("Search patient by name", key="edit_search", value=st.session_state.edit_search)
    st.session_state.edit_search = search_edit

    if search_edit:
        query_edit = "SELECT * FROM patient_status WHERE patient_name LIKE ?"
        df_edit = pd.read_sql(query_edit, conn, params=(f"%{search_edit}%",))

        if df_edit.empty:
            st.sidebar.info("No matching records found.")
            st.session_state.edit_selected_id = None
        else:
            options = df_edit.apply(lambda r: f"{r['patient_name']} | {r['date']} | ID:{r['id']}", axis=1)
            selected_option = st.sidebar.selectbox("Select record to edit", options, key="edit_select")

            selected_id = int(selected_option.split("ID:")[1])
            st.session_state.edit_selected_id = selected_id

            record = df_edit[df_edit['id'] == selected_id].iloc[0]

            with st.sidebar.form("edit_form"):
                patient = st.text_input("Patient Name", value=record['patient_name'], key="edit_patient")
                date = st.date_input("Date", value=pd.to_datetime(record['date']), key="edit_date")
                desc = st.text_area("Description", value=record['description'], key="edit_desc")
                status = st.selectbox("Status", ["Pending", "In Progress", "Completed"],
                                      index=["Pending", "In Progress", "Completed"].index(record['status']), key="edit_status")
                update_clicked = st.form_submit_button("Update")

                if update_clicked:
                    with st.modal("Confirm Update"):
                        st.write("Are you sure you want to update this patient status?")
                        confirm = st.button("Yes, Update")
                        cancel = st.button("Cancel")

                        if confirm:
                            cursor.execute("""
                                UPDATE patient_status 
                                SET patient_name = ?, date = ?, description = ?, status = ?
                                WHERE id = ?
                            """, (patient, date.isoformat(), desc, status, selected_id))
                            conn.commit()
                            st.session_state.action_status = 'updated'
                            st.sidebar.success("✅ Patient status updated.")
                        if cancel:
                            pass

    else:
        st.sidebar.info("Enter patient name to search for editing.")
        st.session_state.edit_selected_id = None

# --- MAIN LAYOUT ---
st.title("📋 Patient Status Board")

search = st.text_input("Search by patient name", key="main_search")

query = "SELECT * FROM patient_status"
if search:
    query += f" WHERE patient_name LIKE '%{search}%'"
df = pd.read_sql(query, conn)

# Show success messages if any
if st.session_state.action_status == 'added':
    st.success("New patient status added successfully!")
    st.session_state.action_status = None
elif st.session_state.action_status == 'updated':
    st.success("Patient status updated successfully!")
    st.session_state.action_status = None
elif st.session_state.action_status == 'deleted':
    st.success("Record deleted successfully!")
    st.session_state.action_status = None

# Display table and details
if not df.empty:
    st.dataframe(df[['date', 'description', 'status']])
    selected = st.selectbox("Select a record for details", df['id'], key="main_selected")
    selected_record = df[df['id'] == selected].iloc[0]

    st.subheader("📌 Detail")
    st.write(f"**Patient:** {selected_record['patient_name']}")
    st.write(f"**Date:** {selected_record['date']}")
    st.write(f"**Description:** {selected_record['description']}")
    st.write(f"**Status:** {selected_record['status']}")

    # Delete confirmation modal
    if st.button("🗑️ Delete this record"):
        with st.modal("Confirm Delete"):
            st.write("Are you sure you want to delete this record?")
            confirm_del = st.button("Yes, Delete")
            cancel_del = st.button("Cancel")

            if confirm_del:
                cursor.execute("DELETE FROM patient_status WHERE id = ?", (selected,))
                conn.commit()
                st.session_state.action_status = 'deleted'
                st.session_state.main_selected = None
                st.success("Record deleted successfully!")
            if cancel_del:
                pass
else:
    st.info("No records found.")

# Sidebar logout button
st.sidebar.markdown("---")
st.sidebar.button("🔒 Logout")
