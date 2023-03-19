### turtle strategy
# we are going to create a long signal when 
# the price reaches the highest price for the last window_size days
# We will create a short signal when the price reaches its lowest point. 
# We will get out of a position by having the price crossing 
# the moving average of the last window_size days

#%%
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data

def load_financial_data(start_date, end_date, output_file):
    try:
        df = pd.read_pickle(output_file)
        print('File data found...reading GOOG data')
    except FileNotFoundError:
        print('File not found...downloading the GOOG data')
        df = data.DataReader('GOOG', 'yahoo', start_date, end_date)
        df.to_pickle(output_file)
    return df


goog_data=load_financial_data(start_date='2001-01-01',
                            end_date = '2018-01-01',
                            output_file='goog_data.pkl'
                            )

def turtle_trading(financial_data, window_size):
    signals = pd.DataFrame(index=financial_data.index)
    signals['orders'] = 0
    signals['high'] = financial_data['Adj Close'].shift(1).rolling(window=window_size).max()
    signals['low'] = financial_data['Adj Close'].shift(1).rolling(window=window_size).min()
    signals['avg'] = financial_data['Adj Close'].shift(1).rolling(window=window_size).mean()
    
    signals['long_entry'] = financial_data['Adj Close'] > signals.high
    signals['short_entry'] = financial_data['Adj Close'] < signals.low
    
    signals['long_exit'] = financial_data['Adj Close'] < signals.avg
    signals['short_exit'] = financial_data['Adj Close'] > signals.avg
    
    init = True
    position = 0
    for k in range(len(signals)):
        if signals['long_entry'][k] and position==0:
            signals.orders.values[k] = 1
            position = 1
        elif signals['short_entry'][k] and position==0:
            signals.orders.values[k] = -1
            position = -1
        elif signals['short_exit'][k] and position>0:
            signals.orders.values[k] = -1
            position = 0
        elif signals['long_exit'][k] and position < 0:
            signals.orders.values[k] = 1
            position = 0
        else:
            signals.orders.values[k] = 0
    return signals

ts=turtle_trading(goog_data, 50)

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Google price in $')
goog_data['Adj Close'].plot(ax=ax1, color='g', lw=.5)
ts['high'].plot(ax=ax1, color='g', lw=.5)
ts['low'].plot(ax=ax1, color='r', lw=.5)
ts['avg'].plot(ax=ax1, color='b', lw=.5)


ax1.plot(ts.loc[ts.orders==1.0].index,
         goog_data['Adj Close'][ts.orders==1.0],
         '^', markersize=7, color='k'
         )

ax1.plot(ts.loc[ts.orders==-1.0].index,
         goog_data['Adj Close'][ts.orders==-1.0],
         'v', markersize=7, color='k'
         )

plt.legend(['Price', 'Highs', 'Lows', 'Average', 'Buy', 'Sell'])
plt.title('Turtle Trading Strategy')
plt.show()


#%%
## initial amount of money
initial_capital = float(10000.0)

# create df for positions
positions = pd.DataFrame(index=signals.index).fillna(0)

# buy 10 shares of MSFT when signal is 1
# sell 10 shares of MSFT when signal is -1
# assign values to MSFT

positions['MSFT'] = 10 * signals['signals']

portfolio = positions.multiply(financial_data['Adj Close'], axis=0)

portfolio['holdings'] = (positions.multiply(financial_data['Adj Close'], axis=0)).sum(axis=1)

pos_diff = positions.diff()

portfolio['cash'] = initial_capital - (pos_diff.multiply(financial_data['Adj Close'], axis=0)).sum(axis=1).cumsum()

portfolio['total'] = portfolio['cash'] + portfolio['holdings']

portfolio['returns'] = portfolio['total'].pct_change()

print(portfolio)


