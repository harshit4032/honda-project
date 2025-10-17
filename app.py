import streamlit as st
import pandas as pd

# --- Honda Motorcycle Test Data ---
data = {
    "Honda CB Shine": {
        "Engine": [
            {"Test Name": "Engine Performance Test", "Description": "Measures torque, power, and fuel efficiency", "Duration (min)": 60, "Status": False},
            {"Test Name": "Cold Start Test", "Description": "Checks starting capability at low temperatures", "Duration (min)": 15, "Status": False},
            {"Test Name": "Emission Test", "Description": "Measures CO, NOx, HC emissions as per BS6 norms", "Duration (min)": 40, "Status": False}
        ],
        "Brakes": [
            {"Test Name": "Brake Performance Test", "Description": "Measures stopping distance and time from various speeds", "Duration (min)": 20, "Status": False},
            {"Test Name": "Brake Fade Test", "Description": "Evaluates reduction in braking efficiency after repeated use", "Duration (min)": 30, "Status": False},
            {"Test Name": "ABS Function Test", "Description": "Checks anti-lock braking system operation", "Duration (min)": 25, "Status": False}
        ],
        "Electrical": [
            {"Test Name": "Battery Load Test", "Description": "Evaluates charging/discharging cycles under load", "Duration (min)": 20, "Status": False},
            {"Test Name": "Lighting Test", "Description": "Checks headlight, indicators, and tail light operation", "Duration (min)": 15, "Status": False}
        ],
        "Suspension": [
            {"Test Name": "Shock Absorber Test", "Description": "Checks damping and rebound performance", "Duration (min)": 25, "Status": False},
            {"Test Name": "Fork Alignment Test", "Description": "Ensures correct fork alignment", "Duration (min)": 20, "Status": False}
        ]
    },
    
    "Honda Activa 6G": {
        "Engine": [
            {"Test Name": "Fuel Efficiency Test", "Description": "Measures mileage under standard conditions", "Duration (min)": 40, "Status": False},
            {"Test Name": "Oil Consumption Test", "Description": "Monitors engine oil consumption over set mileage", "Duration (hrs)": 5, "Status": False},
            {"Test Name": "Emission Test", "Description": "Measures pollutant gases to comply with BS6 norms", "Duration (min)": 30, "Status": False}
        ],
        "Brakes": [
            {"Test Name": "Brake Pad Wear Test", "Description": "Evaluates brake pad wear over distance", "Duration (min)": 25, "Status": False},
            {"Test Name": "Brake Efficiency Test", "Description": "Measures stopping distance from 40 km/h", "Duration (min)": 20, "Status": False}
        ],
        "Electrical": [
            {"Test Name": "Battery Life Test", "Description": "Checks battery endurance under load", "Duration (min)": 20, "Status": False},
            {"Test Name": "Horn & Lighting Test", "Description": "Verifies horn and lights function properly", "Duration (min)": 15, "Status": False}
        ],
        "Suspension": [
            {"Test Name": "Rear Shock Test", "Description": "Measures damping performance and ride comfort", "Duration (min)": 20, "Status": False},
            {"Test Name": "Front Fork Test", "Description": "Checks fork smoothness and alignment", "Duration (min)": 20, "Status": False}
        ]
    },

    "Honda CB Unicorn": {
        "Engine": [
            {"Test Name": "Engine Power Test", "Description": "Measures torque and RPM power curve", "Duration (min)": 60, "Status": False},
            {"Test Name": "Engine Leak Test", "Description": "Checks for oil and fuel leaks under pressure", "Duration (min)": 30, "Status": False},
            {"Test Name": "Fuel Injection Test", "Description": "Ensures proper fuel delivery and mixture", "Duration (min)": 40, "Status": False}
        ],
        "Brakes": [
            {"Test Name": "Front & Rear Brake Test", "Description": "Measures stopping efficiency at different speeds", "Duration (min)": 25, "Status": False},
            {"Test Name": "ABS Calibration Test", "Description": "Verifies ABS functionality and sensor response", "Duration (min)": 30, "Status": False}
        ],
        "Electrical": [
            {"Test Name": "Battery Test", "Description": "Checks voltage output and charge cycles", "Duration (min)": 20, "Status": False},
            {"Test Name": "Lighting & Indicators Test", "Description": "Verifies headlight, tail light, and indicators", "Duration (min)": 15, "Status": False}
        ],
        "Suspension": [
            {"Test Name": "Fork Oil Test", "Description": "Checks for oil leaks and damping consistency", "Duration (min)": 20, "Status": False},
            {"Test Name": "Rear Shock Test", "Description": "Evaluates ride quality and spring performance", "Duration (min)": 25, "Status": False}
        ]
    }
}

# --- Streamlit UI ---
st.title("🏍️ Honda Motorcycle Test Tracker")

# Step 1: Select Model
models = list(data.keys())
selected_model = st.selectbox("Select Honda Motorcycle Model", ["--Select--"] + models)

if selected_model != "--Select--":
    # Step 2: Select Part
    parts = list(data[selected_model].keys())
    selected_part = st.selectbox("Select Component / Part", ["--Select--"] + parts)
    
    if selected_part != "--Select--":
        # Step 3: Display tests with checkboxes
        st.subheader(f"🔬 Tests for {selected_part} ({selected_model})")
        tests = data[selected_model][selected_part]

        # Display each test with a checkbox
        for i, test in enumerate(tests):
            checked = st.checkbox(f"{test['Test Name']} ({test['Duration (min)']} min)", value=test["Status"], key=f"{selected_model}_{selected_part}_{i}")
            # Update the status in the dictionary
            data[selected_model][selected_part][i]["Status"] = checked

        # Show DataFrame of current status
        st.write("### ✅ Current Test Status")
        df_status = pd.DataFrame(tests)
        st.dataframe(df_status, use_container_width=True)

        # Optional: Save updated status to Excel
        if st.button("Save Status to Excel"):
            all_tests = []
            for model_name, parts_dict in data.items():
                for part_name, test_list in parts_dict.items():
                    for t in test_list:
                        row = {"Model": model_name, "Part": part_name}
                        row.update(t)
                        all_tests.append(row)
            df_save = pd.DataFrame(all_tests)
            df_save.to_excel("honda_test_status.xlsx", index=False)
            st.success("✅ Test status saved to honda_test_status.xlsx")
