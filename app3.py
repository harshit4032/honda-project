import streamlit as st
import pandas as pd

# --- Step 1: Load CSV without caching (so updates persist) ---
csv_file = "honda_tests.csv"

def load_data(file_path):
    return pd.read_csv(file_path)

df = load_data(csv_file)

st.title("🏍️ Honda Motorcycle Test Tracker (CSV)")

# Step 2: Select Model
models = df["Model"].unique()
selected_model = st.selectbox("Select Honda Motorcycle Model", ["--Select--"] + list(models))

if selected_model != "--Select--":
    # Step 3: Select Part
    parts = df[df["Model"] == selected_model]["Part"].unique()
    selected_part = st.selectbox("Select Component / Part", ["--Select--"] + list(parts))

    if selected_part != "--Select--":
        # Step 4: Filter tests
        df_filtered = df[(df["Model"] == selected_model) & (df["Part"] == selected_part)].copy()
        st.subheader(f"🔬 Tests for {selected_part} ({selected_model})")

        # Step 5: Display checkboxes and update in main df
        for idx in df_filtered.index:
            checked = st.checkbox(
                f"{df_filtered.at[idx, 'Test Name']} ({df_filtered.at[idx, 'Duration (min)']} min)",
                value=df_filtered.at[idx, 'Status'],
                key=f"{selected_model}_{selected_part}_{idx}"
            )
            df.at[idx, 'Status'] = checked

        st.write("### ✅ Current Test Status")
        st.dataframe(df_filtered, use_container_width=True)

        # Step 6: Save updates immediately when button is pressed
        if st.button("Save Status to CSV"):
            df.to_csv(csv_file, index=False)
            st.success(f"✅ CSV file '{csv_file}' updated successfully!")
