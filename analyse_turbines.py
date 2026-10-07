# =============================================================
# AeroGrid Turbine Anomaly Detection Script
# Author: Data Engineer
# Description: Reads telemetry_data.csv and identifies turbines
#              that require urgent maintenance based on anomaly rules.
# =============================================================

# We import pandas - a Python library for reading and analysing data files
import pandas as pd

# =============================================================
# STEP 1: LOAD THE DATA
# =============================================================
# Read the CSV file into a "dataframe" (think of it like a spreadsheet in Python)
df = pd.read_csv('telemetry_data.csv')

print("Data loaded successfully!")
print(f"Total readings found: {len(df)}")
print(f"Turbines monitored: {df['turbine_id'].nunique()}")
print("-" * 50)

# =============================================================
# STEP 2: CALCULATE STATS PER TURBINE
# =============================================================
# For each turbine, calculate:
#   - The AVERAGE temperature across all readings
#   - The MAXIMUM vibration spike recorded
stats = df.groupby('turbine_id').agg(
    avg_temperature=('temperature_c', 'mean'),
    max_vibration=('vibration_mm_s', 'max')
).round(2)

print("\nSummary stats per turbine:")
print(stats)
print("-" * 50)

# =============================================================
# STEP 3: DEFINE ANOMALY RULES
# =============================================================
# A turbine requires URGENT MAINTENANCE if:
#   Rule 1: Average temperature exceeds 85.0 degrees Celsius
#   Rule 2: Vibration levels spike above 15.0 mm/s

TEMP_LIMIT = 85.0     # degrees Celsius
VIBRATION_LIMIT = 15.0  # mm/s

# =============================================================
# STEP 4: APPLY THE RULES AND FIND FAILING TURBINES
# =============================================================
# Filter turbines that break either rule
failing_turbines = stats[
    (stats['avg_temperature'] > TEMP_LIMIT) |
    (stats['max_vibration'] > VIBRATION_LIMIT)
]

# =============================================================
# STEP 5: OUTPUT THE RESULTS
# =============================================================
print("\n========================================")
print("  TURBINES REQUIRING URGENT MAINTENANCE")
print("========================================")

if failing_turbines.empty:
    print("No turbines currently failing anomaly rules.")
else:
    for turbine_id, row in failing_turbines.iterrows():
        print(f"\nTurbine ID: {turbine_id}")

        # Check which rule(s) it is failing
        if row['avg_temperature'] > TEMP_LIMIT:
            print(f"  [ALERT] HIGH TEMPERATURE: Average = {row['avg_temperature']}°C (Limit: {TEMP_LIMIT}°C)")

        if row['max_vibration'] > VIBRATION_LIMIT:
            print(f"  [ALERT] HIGH VIBRATION: Max spike = {row['max_vibration']} mm/s (Limit: {VIBRATION_LIMIT} mm/s)")

print("\n========================================")
print(f"Total turbines flagged: {len(failing_turbines)}")
print("========================================")

# =============================================================
# HOW TO RUN THIS SCRIPT:
# =============================================================
# 1. Make sure you have Python installed on your computer
# 2. Install the pandas library by opening a terminal and typing:
#       pip install pandas
# 3. Place this script in the same folder as telemetry_data.csv
# 4. Run the script by typing in the terminal:
#       python analyse_turbines.py
# =============================================================
