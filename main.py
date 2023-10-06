import yfinance as yf
import talib as ta
import pandas as pd

print("Enter the ticker symbol: ")
ticker = input()

data = yf.download(ticker, period='1y')

print("Enter moving average period (e.g. 20): ")
period = int(input())

print("Select moving average type (SMA, EMA, WMA, HMA): ")
ma_type = input()

if ma_type == 'SMA':
    ma = ta.SMA(data['Close'], timeperiod=period)
elif ma_type == 'EMA':
    ma = ta.EMA(data['Close'], timeperiod=period)
elif ma_type == 'WMA':
    ma = ta.WMA(data['Close'], timeperiod=period)
elif ma_type == 'HMA':
    ma = ta.HMA(data['Close'], timeperiod=period)

ratio = (data['Close'] - ma) / ma * 100

print(ratio.tail())