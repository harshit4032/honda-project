import streamlit as st
import pandas as pd

# --- Step 1: Load data from Excel ---
excel_file = "honda_tests.xlsx"

@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)

df = load_data(excel_file)

st.title("🏍️ Honda Motorcycle Test Tracker")

# Step 2: Select Model
models = df["Model"].unique()
selected_model = st.selectbox("Select Honda Motorcycle Model", ["--Select--"] + list(models))

if selected_model != "--Select--":
    # Step 3: Select Part
    parts = df[df["Model"] == selected_model]["Part"].unique()
    selected_part = st.selectbox("Select Component / Part", ["--Select--"] + list(parts))
    
    if selected_part != "--Select--":
        # Step 4: Filter tests for model + part
        df_filtered = df[(df["Model"] == selected_model) & (df["Part"] == selected_part)].copy()
        st.subheader(f"🔬 Tests for {selected_part} ({selected_model})")

        # Step 5: Display checkboxes for Status
        for idx in df_filtered.index:
            # Use key to persist checkbox state
            checked = st.checkbox(
                f"{df_filtered.at[idx, 'Test Name']} ({df_filtered.at[idx, 'Duration (min)']} min)",
                value=df_filtered.at[idx, 'Status'],
                key=f"{selected_model}_{selected_part}_{idx}"
            )
            # Update Status in the main dataframe
            df.at[idx, 'Status'] = checked

        # Step 6: Show DataFrame of current status
        st.write("### ✅ Current Test Status")
        st.dataframe(df_filtered, use_container_width=True)

        # Step 7: Save updated status to the original Excel file
        if st.button("Save Status to Excel"):
            df.to_excel(excel_file, index=False)
            st.success(f"✅ Original Excel file '{excel_file}' updated successfully!")
