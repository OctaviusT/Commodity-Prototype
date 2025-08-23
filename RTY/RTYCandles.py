import pandas as pd 
import plotly.graph_objs as go
import plotly.io as pio

#Load the excel file
intraday_data = pd.read_excel("RTYfuture_data.xlsx", index_col=0, parse_dates=True)

# Create a candlestick chart
candlestick = go.Candlestick(
    x=intraday_data.index,
    open=intraday_data['Open'],
    high=intraday_data['High'],
    low=intraday_data['Low'],
    close=intraday_data['Close'],
    name='Candlestick',
    increasing_line_color='green', #Bullish
    decreasing_line_color='red'   #Bearish 
)

# Add moving averages as line plots
ma_50 = go.Scatter(
    x=intraday_data.index,
    y=intraday_data['Sma_50'],
    mode='lines',
    name='50-period MA',
    line=dict(color='orange', width=1.5)
)

ma_105 = go.Scatter(
    x=intraday_data.index,
    y=intraday_data['Sma_105'],
    mode='lines',
    name='105-period MA',
    line=dict(color='green', width=1.5)
)

#Combine the plots
data = [candlestick, ma_50, ma_105]

#Define the layout
layout = go.Layout(
    title= 'RTY=F Candlestick Chart with Moving Averages',
    xaxis=dict(
        title='Date',
        type='category',  #Set to 'category' to handle date range
        rangeslider=dict(visible=True), #Enable range slider
        showspikes=True  #Show vertical line on hover           
    ),
    yaxis=dict(
        title='Price',
        showspikes=True,    #Show horizontal line on hover
        spikemode='across', #Extend spikes across the chart
        spikecolor='grey',
        spikethickness=1,
    ),
    hovermode='x unified',  #Show hover data together
    showlegend=True,
    legend=dict(x=0, y=1),
    margin=dict(l=50, r=50, t=50, b=50) #Adjust margins
)

#Create the figure
fig = go.Figure(data=[candlestick, ma_50, ma_105], layout=layout)

#Save the plot as an HTML file
pio.write_html(fig, file="RTY_intraday_candlestick_chart.html")

#Show the plot
pio.show(fig)