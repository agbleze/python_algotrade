import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt

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










