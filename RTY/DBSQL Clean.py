import databento as db
import pandas as pd
import re

# Function to get historical data from Databento API
def get_bentodata(api_key, dataset, symbols, start, end):
    client = db.Historical(api_key)  # Create a Historical client instance
    data = client.timeseries.get_range(
        dataset=dataset,
        symbols=symbols,
        schema="ohlcv-1m",  # Changed schema to ohlcv-1m
        start=start,
        end=end,
    )
    
    return data  # Returns the data directly

# Function to clean and convert the data for SQL
def clean_and_convert_data(data):
    # Function to extract OHLCV and include the timestamp conversion
    def extract_ohlcv_with_timestamp(row):
        ohlcv_msg = row['value']  # Access the message content
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

    # Apply the extraction to each row in the data
    df_cleaned = data.apply(extract_ohlcv_with_timestamp, axis=1).dropna()

    # Convert the result to a DataFrame
    df_cleaned = pd.DataFrame(df_cleaned.tolist())

    # Ensure that all numeric columns are properly formatted for SQL Server
    df_cleaned['open'] = pd.to_numeric(df_cleaned['open'], errors='coerce')
    df_cleaned['high'] = pd.to_numeric(df_cleaned['high'], errors='coerce')
    df_cleaned['low'] = pd.to_numeric(df_cleaned['low'], errors='coerce')
    df_cleaned['close'] = pd.to_numeric(df_cleaned['close'], errors='coerce')
    df_cleaned['volume'] = pd.to_numeric(df_cleaned['volume'], errors='coerce')

    # Fill in missing values (optional, depends on data requirements)
    df_cleaned.fillna(0, inplace=True)

    return df_cleaned

# Example usage to get data for RTY (Russell 2000) futures
if __name__ == "__main__":
    api_key = 'db-wQqDcQq3e47xNBqMRi3MGbR4cK4qh'  # Replace with your actual API key
    dataset = "GLBX.MDP3"  # Use the appropriate dataset for RTY
    symbols = ["RTYM4"]  # Russell 2000 Futures symbol for January 2024
    start = "2024-04-01T00:00:00"  # Start date in ISO 8601 format
    end = "2024-04-30T23:59:59"    # End date in ISO 8601 format

    # Get historical data
    data = get_bentodata(api_key, dataset, symbols, start, end)

    # Convert data to a clean DataFrame ready for SQL import
    df_cleaned = clean_and_convert_data(data)

    # Save to a CSV file for SQL Server import
    df_cleaned.to_csv('RTY_Apr_2024_Cleaned.csv', index=False)

    print("Cleaned data saved to RTY_Apr_2024_Cleaned.csv.")
