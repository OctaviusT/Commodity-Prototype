import pandas as pd
import matplotlib.pyplot as plt

#Load excel file for data
intraday_data = pd.read_excel("RTYfuture_data.xlsx", index_col=0, parse_dates=True)

#Plot the OHLC and moving averages
plt.figure(figsize=(12, 6))
plt.plot(intraday_data.index, intraday_data['Open'], label='Open Price', color='black')
plt.plot(intraday_data.index, intraday_data['High'], label='Highest Price', color='green')
plt.plot(intraday_data.index, intraday_data['Low'], label='Lowest Price', color='orange')
plt.plot(intraday_data.index, intraday_data['Close'], label='Close Price', color='blue')
plt.plot(intraday_data.index, intraday_data['Sma_50'], label='50-period MA', color='yellow')
plt.plot(intraday_data.index, intraday_data['Sma_105'], label='105-period MA', color='red')
plt.title('RTY=F OHLC w/ Moving Averages')
plt.xlabel('Date')
plt.ylabel ('Price')
plt.legend()
plt.grid(True)

#Save the plot as a PNG file
plt.savefig("RTY_intraday_line_chart.png")

#Show the plot
plt.show()