import talib as ta
import pandas as pd
from datetime import datetime
import yfinance as yf

# Constants
LOOKBACK = 10
LEVEL1 = 1.618
LEVEL2 = 2.277
LEVEL3 = 3.0
LEVEL4 = 3.618
LEVEL5 = 4.418

# Functions
def get_fib_levels(high, low):
    levels = [LEVEL1, LEVEL2, LEVEL3, LEVEL4, LEVEL5]
    recent_range = high - low
    return [high - recent_range * l for l in levels] + [low + recent_range * l for l in levels]

def fetch_data(ticker_symbol, start_date, end_date):
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    return stock_data

def test_strategy(data):
    cash = 10000
    qty = 0
    buy_price = 0
    sell_price = 0

    for i in range(len(data)):
        if i < LOOKBACK:
            continue

        high = data.iloc[i - LOOKBACK:i]['High'].max()
        low = data.iloc[i - LOOKBACK:i]['Low'].min()
        fib_levels = get_fib_levels(high, low)

        if qty == 0 and data.iloc[i]['Close'] > fib_levels[2]:
            # Buy at level 3
            qty = int(cash / data.iloc[i]['Close'])
            buy_price = data.iloc[i]['Close']
            cash -= qty * buy_price
            print(f"Buy {qty} shares at {buy_price} on {data.iloc[i].name}")

        if qty > 0 and data.iloc[i]['Close'] < fib_levels[1]:
            # Sell at level 2
            sell_price = data.iloc[i]['Close']
            cash += qty * sell_price
            profit = qty * (sell_price - buy_price)
            print(f"Sell {qty} shares at {sell_price} on {data.iloc[i].name} | Profit: {profit}")
            qty = 0

    return cash

def main():
    ticker_symbol = input("Enter the ticker symbol (e.g. 'AAPL'): ")
    start_date = input("Enter the start date (format: YYYY-MM-DD): ")
    end_date = input("Enter the end date (format: YYYY-MM-DD): ")

    data = fetch_data(ticker_symbol, start_date, end_date)

    initial_cash = 10000
    final_cash = test_strategy(data)

    print(f"Starting cash: {initial_cash}")
    print(f"Final cash: {final_cash}")
    print(f"PNL: {final_cash - initial_cash}")

if __name__ == '__main__':
    main()

def main():
    # User inputs
    ticker = input("Enter ticker: ")
    start = input("Enter start date (YYYY-MM-DD): ")
    end = input("Enter end date (YYYY-MM-DD): ")

    # Get data
    data = yf.download(ticker, start=start, end=end)
    # Add any other necessary main logic here...

if __name__ == '__main__':
    main()
