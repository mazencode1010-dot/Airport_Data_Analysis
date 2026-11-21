"""Airport Experience Analysis — run locally in Visual Studio Code.

Install packages first:
    pip install pandas plotly openpyxl

Then run:
    python airport_analysis_vs_code.py

Select the airport Excel workbook when prompted.
"""

import pandas as pd
import plotly.express as px
from tkinter import Tk, filedialog


# 1. Choose the Excel file on your computer.
root = Tk()
root.withdraw()
root.attributes("-topmost", True)
file_path = filedialog.askopenfilename(
    title="Select Airport Excel File",
    filetypes=[("Excel files", "*.xlsx *.xls")],
)
root.destroy()

if not file_path:
    raise SystemExit("No file selected.")

# 2. Read all sheets.
data = pd.read_excel(file_path, sheet_name=None)

# 3. Display a quick summary of every sheet.
for name, df in data.items():
    print(f"\n{name}: {df.shape[0]} Rows, {df.shape[1]} Columns")
    print(df.head().to_string(index=False))

# 4. Passengers by gender.
px.pie(
    data["Passenger"],
    names="gender",
    title="Passengers by Gender",
).show()

# 5. Passengers by age group.
px.histogram(
    data["Passenger"],
    x="age_group",
    title="Passengers by Age Group",
).show()

# 6. Types of flights.
px.histogram(
    data["Travel"],
    x="flight_type",
    title="Flight Types",
).show()

# 7. Reasons for traveling.
px.histogram(
    data["Travel"],
    x="trip_purpose",
    title="Travel Purposes",
).show()

# 8. Monthly travel distribution.
px.histogram(
    data["Travel"],
    x="month",
    title="Monthly Travel Distribution",
).show()

# 9. Average service ratings (only valid scores from 1 to 5).
scores = {}

for label, sheet, column in [
    ("Check-in", "checkin", "checkin_process.1"),
    ("Security", "SIC", "security_screening_process.1"),
    ("Baggage", "Bagggage", "Baggage_claim_process.1"),
]:
    values = pd.to_numeric(data[sheet][column], errors="coerce")
    scores[label] = values[values.between(1, 5)].mean()

px.bar(
    x=list(scores),
    y=list(scores.values()),
    range_y=[0, 5],
    labels={"x": "Service", "y": "Average Rating"},
    title="Average Airport Service Ratings",
).show()

print("\nAverage Airport Service Ratings:")
for service, score in scores.items():
    print(f"{service}: {score:.2f}" if pd.notna(score) else f"{service}: No valid ratings")
