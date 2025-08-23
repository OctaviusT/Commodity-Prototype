import pandas as pd
import re
import databento  # Assuming the Databento API is installed
from datetime import datetime
from databento.common.enums import Dataset

# Replace with your Databento API key
API_KEY = "db-wQqDcQq3e47xNBqMRi3MGbR4cK4qh"

# Function to clean and extract OHLCV data with timestamp conversion
def extract_ohlcv_with_timestamp(row):
    ohlcv_msg = row[0]  # Access the first column directly
    pattern = r'open: (\d+\.\d+), high: (\d+\.\d+), low: (\d+\.\d+), close: (\d+\.\d+), volume: (\d+)'
    
    # Extract ts_event from the text
    ts_event_pattern = r'ts_event: (\d+)'
    ts_event_match = re.search(ts_event_pattern, ohlcv_msg)
    if ts_event_match:
        ts_event = int(ts_event_match.group(1))  # Extract and convert to int
    else:
        return None  # Return None if ts_event is not found

    match = re.search(pattern, ohlcv_msg)
    if match:
        # Convert ts_event to a readable timestamp
        timestamp = pd.to_datetime(ts_event, unit='ns')  # Assuming ts_event is in nanoseconds
        return {
            'timestamp': timestamp,
            'open': float(match.group(1)),
            'high': float(match.group(2)),
            'low': float(match.group(3)),
            'close': float(match.group(4)),
            'volume': int(match.group(5))
        }
    return None

# Function to pull and clean data for a specific month
def pull_and_clean_data(start_date, end_date, month_str):
    # Initialize Databento client
    client = databento.Historical(API_KEY)

    # Pull data using the API for the specified date range
    print(f"Downloading data for {month_str}...")
    data = client.timeseries.get_range(
        dataset=Dataset.GLBX.MDP3,  # Example dataset
        symbols=["RTY"],
        start_date=start_date,
        end_date=end_date,
        encoding="csv"
    )

    # Convert the raw data to a DataFrame
    df = pd.read_csv(data.decode('utf-8'), header=None)

    # Apply the extraction function to clean the data
    print(f"Cleaning data for {month_str}...")
    df_cleaned = df.apply(extract_ohlcv_with_timestamp, axis=1).dropna()

    # Convert to DataFrame and save to CSV
    df_cleaned = pd.DataFrame(df_cleaned.tolist())
    output_file = f'RTY_{month_str}_OHLCV.csv'
    df_cleaned.to_csv(output_file, index=False)

    print(f"Cleaned data for {month_str} saved to {output_file}")

# Define start and end dates for each month from January to September 2024
month_ranges = [
    ("2024-01-01", "2024-01-31", "January"),
    ("2024-02-01", "2024-02-29", "February"),
    ("2024-03-01", "2024-03-31", "March"),
    ("2024-04-01", "2024-04-30", "April"),
    ("2024-05-01", "2024-05-31", "May"),
    ("2024-06-01", "2024-06-30", "June"),
    ("2024-07-01", "2024-07-31", "July"),
    ("2024-08-01", "2024-08-31", "August"),
    ("2024-09-01", "2024-09-30", "September"),
]

# Loop through the months and apply the pulling and cleaning process sequentially
for start_date, end_date, month_str in month_ranges:
    pull_and_clean_data(start_date, end_date, month_str)
