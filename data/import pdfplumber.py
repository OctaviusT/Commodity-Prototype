import pdfplumber
import pandas as pd

# Correct file path to the actual PDF
pdf_path = r"C:\Users\dump_\Downloads\Data Bloc Personal Account 7665\statement.pdf"

# Open the PDF and extract tables
with pdfplumber.open(pdf_path) as pdf:
    data = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            data.extend(table)

# Convert extracted data to DataFrame and save as CSV
df = pd.DataFrame(data)
csv_output_path = r"C:\Users\dump_\Downloads\May_24.csv"
df.to_csv(csv_output_path, index=False)
print(f"Extraction completed. CSV saved at {csv_output_path}")
