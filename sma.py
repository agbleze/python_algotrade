


## fundamanetal technical analysis for trading signals ####

# Simple Moving Avergae (SMA)
## Averaging price of an instrument over time window

#%% implement SMA
import statistics as stats
from pandas_datareader import data
import yfinance as yfin
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


yfin.pdr_override()

start_date = '2014-01-01'
end_date = '2018-01-01'
SRC_DATA_FILENAME = 'goog_data.pkl'


try:
    goog_data2 = pd.read_pickle(SRC_DATA_FILENAME)
    print('File data not found... reading GOOG data')
except FileNotFoundError:
    print('File not found... downloading from GOOG data')
    goog_data2 = data.DataReader('GOOG', start_date, end_date
                                 )
    goog_data2.to_pickle(SRC_DATA_FILENAME)
    
goog_data = goog_data2.tail(620)
close = goog_data['Close']

#lows=goog_data['Low']
#highs=goog_data['High']

#%%
time_period = 20
history = []
sma_values = []

for close_price in close:
    history.append(close_price)
    if len(history) > time_period:
        del (history[0])
    sma_values.append(stats.mean(history))

goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(Simple20DayMovingAverage=pd.Series(sma_values, index=goog_data.index))
close_price = goog_data['ClosePrice']
sma = goog_data['Simple20DayMovingAverage']

import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel="Goog price in $")
close_price.plot(ax=ax1, color='g', lw=2, legend=True)
sma.plot(ax=ax1, color='r', lw=2, legend=True)
plt.show()








# %%
