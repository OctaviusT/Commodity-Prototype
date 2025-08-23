import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

#Download futures data
futures_data = yf.download("RTY=F", start="2020-01-01", end="2024-07-27")

#Convert the index to datetime
futures_data.index= pd.to_datetime(futures_data.index)

#Print sample data
print(futures_data)

#Write the data to an Excel file
futures_data.to_excel("RTYfuture_data.xlsx", index=True)