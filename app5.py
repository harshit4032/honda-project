import streamlit as st
import pandas as pd

csv_file = "honda_tests.csv"

# Load and save functions
def load_data(file_path):
    return pd.read_csv(file_path)

def save_data(df, file_path):
    df.to_csv(file_path, index=False)

df = load_data(csv_file)

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Track Tests", "Manage Tests"])

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
            st.dataframe(df_filtered[["Model","Part","Test Name","Duration (min)","Status"]], use_container_width=True)

            if st.button("Save Status to CSV"):
                save_data(df, csv_file)
                st.success(f"✅ CSV file '{csv_file}' updated successfully!")

# ------------------- Page 2: Manage Tests -------------------
elif menu == "Manage Tests":
    st.title("➕➖ Add or Remove Vehicle Tests")

    sub_menu = st.radio("Select Action", ["Add Tests", "Remove Test"])

    # ---------------- Add Tests ----------------
    if sub_menu == "Add Tests":
        new_model = st.text_input("Model Name")
        new_part = st.text_input("Part / Component")
        new_tests_input = st.text_area("Enter Test Names (comma-separated)")
        new_duration = st.number_input("Duration (min)", min_value=1)
        new_status = st.checkbox("Mark as Done", value=False)

        if st.button("Add Tests to CSV"):
            if new_model and new_part and new_tests_input:
                test_list = [t.strip() for t in new_tests_input.split(",") if t.strip()]
                new_rows = []
                for test_name in test_list:
                    new_rows.append({
                        "Model": new_model,
                        "Part": new_part,
                        "Test Name": test_name,
                        "Duration (min)": new_duration,
                        "Status": new_status
                    })
                df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
                save_data(df, csv_file)
                st.success(f"✅ {len(test_list)} tests added for {new_model} - {new_part}!")
            else:
                st.error("⚠️ Please fill at least Model, Part, and Test Names")

    # ---------------- Remove Test ----------------
    elif sub_menu == "Remove Test":
        models = df["Model"].unique()
        remove_model = st.selectbox("Select Model", ["--Select--"] + list(models))
        if remove_model != "--Select--":
            parts = df[df["Model"] == remove_model]["Part"].unique()
            remove_part = st.selectbox("Select Part", ["--Select--"] + list(parts))
            if remove_part != "--Select--":
                tests = df[(df["Model"] == remove_model) & (df["Part"] == remove_part)]["Test Name"].unique()
                remove_test = st.selectbox("Select Test to Remove", ["--Select--"] + list(tests))
                if remove_test != "--Select--":
                    if st.button("Remove Test"):
                        df = df[~((df["Model"]==remove_model) & (df["Part"]==remove_part) & (df["Test Name"]==remove_test))]
                        save_data(df, csv_file)
                        st.success(f"✅ Test '{remove_test}' removed from {remove_model} - {remove_part}!")
