import databento as db
import pandas as pd

# Function to get historical data from Databento API
def get_bentodata(api_key, dataset, symbols, start, end):
    client = db.Historical(api_key)  # Create a Historical client instance
    data = client.timeseries.get_range(
        dataset=dataset,
        symbols=symbols,
        schema="ohlcv-1s",  # Change to your preferred schema if necessary
        start=start,
        end=end,
    )
    
    return data  # Returns the data directly

# Example usage to get data for RTY (Russell 2000) futures
if __name__ == "__main__":
    api_key = 'db-wQqDcQq3e47xNBqMRi3MGbR4cK4qh'  # Replace with your actual API key
    dataset = "GLBX.MDP3"  # Use the appropriate dataset for RTY
    symbols = ["RTYZ4"]  # Russell 2000 Futures symbol (modify as necessary)
    start = "2024-09-01T00:00:00"  # Start date in ISO 8601 format
    end = "2024-09-30T23:59:59"    # End date in ISO 8601 format

    # Get historical data
    data = get_bentodata(api_key, dataset, symbols, start, end)

    # Replay the data to see output
    data.replay(print)

    # Convert data to DataFrame (if necessary)
    df = pd.DataFrame(data)  # This will depend on the format of the data returned
    df.to_csv('rty_data.csv', index=False)
    print("Data saved to rty_data.csv.")
