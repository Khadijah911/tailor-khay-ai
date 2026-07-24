import pandas as pd
import sqlite3

# Read the Excel file
df = pd.read_excel("Tailor_khay_measurement_db.xlsx")

# Connect to the database
connection = sqlite3.connect("tailor_khay.db")
cursor = connection.cursor()

# Loop through each customer
for _, row in df.iterrows():

    cursor.execute("""
    INSERT INTO measurements (
        customer_name,
        phone_number,
        bust,
        waist,
        hip,
        full_length,
        half_length,
        blouse_length,
        shoulder,
        sleeve_length,
        round_sleeve,
        nipple_to_nipple,
        shoulder_to_underbust,
        waist_to_hip,
        trouser_length,
        lap,
        upper_cleavage,
        lower_cleavage
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        row["customer_name"],
        row["phone_number"],
        row["bust"],
        row["waist"],
        row["hip"],
        row["full_length"],
        row["half_length"],
        row["blouse_length"],
        row["shoulder"],
        row["sleeve_length"],
        row["round_sleeve"],
        row["nipple_to_nipple"],
        row["shoulder_to_underbust"],
        row["waist_to_hip"],
        row["trouser_length"],
        row["lap"],
        row["upper_cleavage"],
        row["lower_cleavage"],
    ))

connection.commit()
connection.close()

print("Measurements imported successfully!")