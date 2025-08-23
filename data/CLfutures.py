import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

#Download futures data
futures_data = yf.download("CL=F", start="2020-01-01", end="2024-07-27")

#Convert the index to datetime
futures_data.index= pd.to_datetime(futures_data.index)

#Add in Moving Average 50 Day EMA & 105 Day EMA

ma_50=50

SmaString="Sma_" +str(ma_50)

futures_data[SmaString]=futures_data.iloc[:, 4].rolling(window=ma_50).mean()

ma_105=105

SmaString_2="Sma_" +str(ma_105)

futures_data[SmaString_2]=futures_data.iloc[:, 4].rolling(window=ma_105).mean()

# Print sample data with moving average
print(futures_data[[SmaString, SmaString_2]])

#Write the data to an Excel file
futures_data.to_excel("CLfuture_data.xlsx", index=True)