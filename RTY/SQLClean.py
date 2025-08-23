import pandas as pd
import re

# Function to clean and convert the data for SQL
def clean_csv_for_sql(input_csv, output_csv):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv)

    # Ensure that all numeric columns are properly formatted for SQL Server
    # List your numeric columns here (replace 'open', 'high', etc., with your actual column names)
    numeric_columns = ['open', 'high', 'low', 'close', 'volume']

    for col in numeric_columns:
        if col in df.columns:
            # Convert to numeric, set errors='coerce' to handle non-numeric data by converting it to NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill in missing numeric values with 0 (you can change this behavior if needed)
    df.fillna(0, inplace=True)

    # Optionally, trim whitespace from string columns (if any)
    str_columns = df.select_dtypes(include=['object']).columns
    for col in str_columns:
        df[col] = df[col].str.strip()

    # Ensure column names are SQL-friendly (no spaces, special characters, etc.)
    df.columns = [re.sub(r'\W+', '_', col).lower() for col in df.columns]

    # Save the cleaned data to a new CSV file
    df.to_csv(output_csv, index=False)

    print(f"Cleaned CSV saved to {output_csv}")

# Example usage
if __name__ == "__main__":
    input_csv = 'RTY_Mar24_OHLCV.csv'  # Replace with your actual input CSV file
    output_csv = 'RTY_Mar_2024_Cleaned.csv'  # Output file name for the cleaned data

    clean_csv_for_sql(input_csv, output_csv)
