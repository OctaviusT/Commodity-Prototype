import pandas as pd

#Load the data from Excel file
df = pd.read_excel('RTYfuture_data.xlsx', sheet_name='Sheet1', parse_dates=['Date'])
df.sort_values('Date', inplace=True)

# Ensure 'Close' column exists and calculate previous close
if 'Close' in df.columns:
    df['Prev_Close'] = df['Close'].shift(1)
    df['Prev_Close_Diff'] = (df['Close'] - df['Prev_Close']).abs()
else:
    print("Error: 'Close' column not found in the data.")
    exit()

#Calculate best days to trade based on volume
best_days_by_volume = df.nlargest(100, 'Volume')

#Calulate biggest changes in the previous day's low's and high's
df['High_Low_Diff'] = df['High'] - df['Low']
biggest_high_low_changes = df.nlargest(100, 'High_Low_Diff')

#Calculate biggest difference in previous close by day
df['Previous_Close'] = df['Close'].shift(1)
df['Prev_Close_Diff'] = (df['Close'] - df['Prev_Close']).abs()
biggest_close_changes = df.nlargest(100, 'Prev_Close_Diff')

# Calculate biggest differences in SMA 50 and SMA 105 by day
df['SMA_Diff'] = (df['Sma_50'] - df['Sma_105']).abs()
biggest_sma_diff = df.nlargest(100, 'SMA_Diff')

#Save the results to an Excel file
with pd.ExcelWriter('RTYanalysis_results.xlsx') as writer:
    best_days_by_volume.to_excel(writer, sheet_name='Best Days by Volume', index=False)
    biggest_high_low_changes.to_excel(writer, sheet_name='High-Low Changes', index=False)
    biggest_close_changes.to_excel(writer, sheet_name='Prev Close Chages', index=False)
    biggest_sma_diff.to_excel(writer, sheet_name='SMA Differences', index=False)

print("Results have been saved to 'RTYanalysis_results.xlsx")