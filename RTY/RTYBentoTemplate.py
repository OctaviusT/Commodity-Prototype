import databento as db
import pandas as pd
import re

# Function to get historical data from Databento API
def get_bentodata(api_key, dataset, symbols, start, end):
    client = db.Historical(api_key)  # Create a Historical client instance
    data = client.timeseries.get_range(
        dataset=dataset,
        symbols=symbols,
        schema="ohlcv-1m",  # Schema set to ohlcv-1m for 1-minute data
        start=start,
        end=end,
    )
    
    return data  # Returns the data directly

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

# Example usage to get data for RTY (Russell 2000) futures for February 2024
if __name__ == "__main__":
    api_key = 'db-wQqDcQq3e47xNBqMRi3MGbR4cK4qh'  # Replace with your actual API key
    dataset = "GLBX.MDP3"  # Use the appropriate dataset for RTY
    symbols = ["RTY"]  # Russell 2000 Futures symbol for February 2024
    start = "2024-02-01T00:00:00"  # Start date in ISO 8601 format
    end = "2024-02-29T23:59:59"    # End date in ISO 8601 format

    # Get historical data
    data = get_bentodata(api_key, dataset, symbols, start, end)

    # Replay the data to see output
    data.replay(print)

    # Convert data to DataFrame (if necessary)
    df = pd.DataFrame(data)  # This will depend on the format of the data returned
    df.to_csv('rty_data_mon_2024.csv', index=False)  # Save to a new CSV file
    print("Data saved to rty_data_feb_2024.csv.")

    # Load the saved CSV file with no header
    df_loaded = pd.read_csv('rty_data_month_2024.csv', header=None)

    # Apply the extraction to each row in the DataFrame
    df_cleaned = df_loaded.apply(extract_ohlcv_with_timestamp, axis=1).dropna()

    # Convert the result to a DataFrame
    df_cleaned = pd.DataFrame(df_cleaned.tolist())

    # Save the cleaned data to a new CSV file
    output_file = 'RTY_MONTH_OHLCV.csv'
    df_cleaned.to_csv(output_file, index=False)

    print(f"Cleaned data saved to {output_file}")
