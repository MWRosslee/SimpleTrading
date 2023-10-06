import pandas as pd
import talib as ta
import yfinance as yf


def fetch_data(ticker_symbol, start_date, end_date):
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    return stock_data


def bollinger_rsi_macd_strategy(data):
    # Bollinger Bands Calculation
    data['basis'] = ta.trend.sma_indicator(data['Close'], window=34)
    data['dev'] = data['Close'].rolling(window=34).std()
    data['dev2'] = 2.0 * data['dev']

    data['upper1'] = data['basis'] + data['dev']
    data['lower1'] = data['basis'] - data['dev']
    data['upper2'] = data['basis'] + data['dev2']
    data['lower2'] = data['basis'] - data['dev2']

    # RSI Calculation
    data['rsi'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()

    # MACD Calculation
    macd = ta.trend.MACD(data['Close'], window_slow=26, window_fast=12, window_sign=9)
    data['macd'] = macd.macd()
    data['macd_signal'] = macd.macd_signal()

    # Trading Signals
    data['long_entry'] = (data['Close'].shift(1) < data['upper1'].shift(1)) & (data['Close'] > data['upper1'])
    data['short_entry'] = (data['Close'].shift(1) > data['lower1'].shift(1)) & (data['Close'] < data['lower1'])

    data['rsi_long'] = data['rsi'] > 70
    data['rsi_short'] = data['rsi'] < 30

    data['macd_long'] = data['macd'] > data['macd_signal']
    data['macd_short'] = data['macd'] < data['macd_signal']

    # Combining signals
    data['combined_long_entry'] = data['long_entry'] & data['rsi_long'] & data['macd_long']
    data['combined_short_entry'] = data['short_entry'] & data['rsi_short'] & data['macd_short']

    data['combined_long_exit'] = data['macd_short'] | (data['rsi'] < 50) | (data['Close'] < data['basis'])
    data['combined_short_exit'] = data['macd_long'] | (data['rsi'] > 50) | (data['Close'] > data['basis'])

    return data


ticker = input("Enter the ticker symbol (e.g. 'AAPL'): ")
start_date = input("Enter the start date (format: YYYY-MM-DD): ")
end_date = input("Enter the end date (format: YYYY-MM-DD): ")

data = fetch_data(ticker, start_date, end_date)
results = bollinger_rsi_macd_strategy(data)

print(results.tail())
