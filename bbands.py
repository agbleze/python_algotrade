#%% Bollinger Band (BBANDS) 
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
import statistics as stats
import math

start_date = "2014-01-01"
end_date = "2018-01-01"

SRC_DATA_FILENAME = "goog_data.pkl"

try:
    goog_data2 = pd.read_pickle(SRC_DATA_FILENAME)
except FileNotFoundError:
    goog_data2 = data.DataReader('GOOG', start_date, end_date)
    goog_data2.to_pickle(SRC_DATA_FILENAME)
    
goog_data = goog_data2.tail(620)

close = goog_data['Close']

time_period = 20
stdev_factor = 2
history = []
sma_values = []
upper_band = []
lower_band = []

for close_price in close:
    history.append(close_price)
    if len(history) > time_period:
        del (history[0])
        
    sma = stats.mean(history)
    sma_values.append(sma)
    variance = 0
    for hist_price in history:
        variance = variance + ((hist_price - sma) ** 2)
        
    stdev = math.sqrt(variance / len(history))
    upper_band.append(sma + stdev_factor * stdev)
    lower_band.append(sma - stdev_factor * stdev)
    
goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(MiddleBollingerBand20DaySMA=pd.Series(sma_values, index=goog_data.index))
goog_data = goog_data.assign(UpperBollingerBand20DaySMA2StdevFactor=pd.Series(upper_band, index=goog_data.index))
goog_data = goog_data.assign(LowerBollingerBand20DaySMA2StdevFactor=pd.Series(lower_band, index=goog_data.index))

close_price = goog_data['ClosePrice']
mband = goog_data['MiddleBollingerBand20DaySMA']
uband = goog_data['UpperBollingerBand20DaySMA2StdevFactor']
lband = goog_data['LowerBollingerBand20DaySMA2StdevFactor']

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Google price in $')
close_price.plot(ax=ax1, color='y', lw=2, legend=True)
mband.plot(ax=ax1, color='b', lw=2, legend=True)
uband.plot(ax=ax1, color='g', lw=2, legend=True)
lband.plot(ax=ax1, color='r', lw=2, legend=True)
plt.show()










# %%
