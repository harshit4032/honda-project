import streamlit as st
import pandas as pd

csv_file = "honda_tests.csv"

# Load data without caching
def load_data(file_path):
    return pd.read_csv(file_path)

def save_data(df, file_path):
    df.to_csv(file_path, index=False)

df = load_data(csv_file)

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Track Tests", "Add New Test"])

# ------------------- Page 1: Track Tests -------------------
if menu == "Track Tests":
    st.title("🏍️ Honda Motorcycle Test Tracker")

    models = df["Model"].unique()
    selected_model = st.selectbox("Select Honda Motorcycle Model", ["--Select--"] + list(models))

    if selected_model != "--Select--":
        parts = df[df["Model"] == selected_model]["Part"].unique()
        selected_part = st.selectbox("Select Component / Part", ["--Select--"] + list(parts))

        if selected_part != "--Select--":
            df_filtered = df[(df["Model"] == selected_model) & (df["Part"] == selected_part)].copy()
            st.subheader(f"🔬 Tests for {selected_part} ({selected_model})")

            for idx in df_filtered.index:
                checked = st.checkbox(
                    f"{df_filtered.at[idx, 'Test Name']} ({df_filtered.at[idx, 'Duration (min)']} min)",
                    value=df_filtered.at[idx, 'Status'],
                    key=f"{selected_model}_{selected_part}_{idx}"
                )
                df.at[idx, 'Status'] = checked

            st.write("### ✅ Current Test Status")
            st.dataframe(df_filtered, use_container_width=True)

            if st.button("Save Status to CSV"):
                save_data(df, csv_file)
                st.success(f"✅ CSV file '{csv_file}' updated successfully!")

# ------------------- Page 2: Add New Test -------------------
elif menu == "Add New Test":
    st.title("➕ Add New Vehicle Test")

    new_model = st.text_input("Model Name")
    new_part = st.text_input("Part / Component")
    new_test_name = st.text_input("Test Name")
    new_description = st.text_area("Description")
    new_duration = st.number_input("Duration (min)", min_value=1)
    new_status = st.checkbox("Mark as Done", value=False)

    if st.button("Add Test to CSV"):
        if new_model and new_part and new_test_name:
            new_row = {
                "Model": new_model,
                "Part": new_part,
                "Test Name": new_test_name,
                "Description": new_description,
                "Duration (min)": new_duration,
                "Status": new_status
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df, csv_file)
            st.success(f"✅ Test '{new_test_name}' added to CSV!")
        else:
            st.error("⚠️ Please fill at least Model, Part, and Test Name")
