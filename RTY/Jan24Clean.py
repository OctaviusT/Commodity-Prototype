import pandas as pd
import re

# Load the CSV file with no header
df = pd.read_csv('rty_data_jan_2024.csv', header=None)

# Function to extract OHLCV and include the timestamp conversion
def extract_ohlcv_with_timestamp(row):
    # The data is assumed to be in the first column (index 0)
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

# Apply the extraction to each row in the DataFrame
df_cleaned = df.apply(extract_ohlcv_with_timestamp, axis=1).dropna()

# Convert the result to a DataFrame
df_cleaned = pd.DataFrame(df_cleaned.tolist())

# Save the cleaned data to a new CSV file
output_file = 'RTY_Jan24_OHLCV.csv'
df_cleaned.to_csv(output_file, index=False)

print(f"Cleaned data saved to {output_file}")
