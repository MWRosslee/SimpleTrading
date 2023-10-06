import yfinance as yf
import talib as ta
import matplotlib.pyplot as plt
import pandas as pd

# Load data
ticker = input("Enter ticker: ")
data = yf.download(ticker, period='1y')

# Calculate MA
period = int(input("Enter period: "))
ma_type = input("Enter MA type: ")

if ma_type == 'SMA':
    ma = ta.SMA(data['Close'], timeperiod=period)
elif ma_type == 'EMA':
    ma = ta.EMA(data['Close'], timeperiod=period)

# Calculate ratio
ratio = (data['Close'] - ma) / ma * 100

# Define thresholds
buy_threshold = 2
sell_threshold = -2

# Generate signals
data['Buy Signal'] = 0
data['Sell Signal'] = 0
data.loc[ratio > buy_threshold, 'Buy Signal'] = 1
data.loc[ratio < sell_threshold, 'Sell Signal'] = -1

# Identify triggers
buy_signals = data[data['Buy Signal'] == 1]
sell_signals = data[data['Sell Signal'] == -1]

# Plot triggers
fig, ax = plt.subplots()
buy_signals['Close'].plot(ax=ax, marker='^', color='g')
sell_signals['Close'].plot(ax=ax, marker='v', color='r')

# Export to CSV
signals = pd.concat([buy_signals, sell_signals])
signals = signals.reset_index()[['Date','Close','Buy Signal','Sell Signal']]
signals['Ticker'] = ticker
signals['MA Type'] = ma_type
signals.to_csv("signals.csv", index=False)

plt.show()