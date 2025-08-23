import pandas as pd
from tabula import read_pdf

# Define the file path
pdf_path = r"C:\Users\dump_\Downloads\Data Bloc Personal Account 7665"

# Output CSV file path
csv_output_path = r"D:\Eight Leaf\Clients\DataBlock_TCH\Databloc Statements\2024 Statements\Data Bloc Personal Account 7665\statement.csv"

# Extract tables from the PDF
try:
    print("Extracting tables from PDF...")
    tables = read_pdf(pdf_path, pages="all", multiple_tables=True)

    # Combine all tables into one DataFrame
    combined_df = pd.concat(tables, ignore_index=True)

    # Clean the data as needed
    combined_df = combined_df.dropna(how="all")  # Remove rows where all elements are NaN

    # Save the DataFrame to CSV
    combined_df.to_csv(csv_output_path, index=False)
    print(f"Data successfully saved to {csv_output_path}")

except Exception as e:
    print(f"An error occurred: {e}")
