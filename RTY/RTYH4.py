import databento as db
import pandas as pd

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

# Example usage to get data for RTY (Russell 2000) futures
if __name__ == "__main__":
    api_key = 'db-wQqDcQq3e47xNBqMRi3MGbR4cK4qh'  # Replace with your actual API key
    dataset = "GLBX.MDP3"  # Use the appropriate dataset for RTY
    symbols = ["RTYH4"]  # Russell 2000 Futures symbol for January 2024
    start = "2024-01-01T00:00:00"  # Start date in ISO 8601 format
    end = "2024-01-31T23:59:59"    # End date in ISO 8601 format

    # Get historical data
    data = get_bentodata(api_key, dataset, symbols, start, end)

    # Replay the data to see output
    data.replay(print)

    # Convert data to DataFrame (if necessary)
    df = pd.DataFrame(data)  # This will depend on the format of the data returned
    df.to_csv('rty_data_jan_2024.csv', index=False)  # Save to a new CSV file
    print("Data saved to rty_data_jan_2024.csv.")
