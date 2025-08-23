import databento as db
import pandas as pd

# Initialize the Databento client
client = db.Historical("db-wQqDcQq3e47xNBqMRi3MGbR4cK4qh")

# Function to pull and clean January 2024 data
def pull_and_clean_january_data():
    dataset = "GLBX.MDP3"
    symbol = "RTYH4"

    # Get data for January 2024
    data = client.timeseries.get_range(
        dataset=dataset,
        symbols=symbol,
        schema="ohlcv-1m",  # Use minute-level OHLCV data
        start="2024-01-01T00:00:00Z",
        end="2024-01-31T23:59:59Z"
    )

    # Extract relevant fields from the raw data
    records = []
    for record in data:
        # Access the necessary fields based on the structure of OhlcvMsg
        ohlcv_data = {
            'ts_event': record.hd.ts_event,
            'open': record.open,
            'high': record.high,
            'low': record.low,
            'close': record.close,
            'volume': record.volume
        }
        records.append(ohlcv_data)

    # Convert extracted records to DataFrame
    df = pd.DataFrame(records)

    # Convert all float columns to string with formatting
    for col in ['ts_event', 'open', 'high', 'low', 'close']:
        df[col] = df[col].apply(lambda x: f'{x:.2f}')

    # Convert volume to int (if needed)
    df['volume'] = df['volume'].astype(int)

    # Save cleaned data to a CSV file
    df.to_csv('RTY_Jan_2024_OHLCV.csv', index=False)
    print("Cleaned January 2024 data saved successfully.")

# Call the function to execute
pull_and_clean_january_data()
