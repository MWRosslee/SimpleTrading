import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Download data from Yahoo Finance
def fetch_data(ticker_symbol, start_date, end_date):
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    return stock_data['Adj Close'].tolist()

# Define your ticker and relevant index
# For example, for Apple (AAPL) on NASDAQ, the relevant index might be NASDAQ Composite (^IXIC)
ticker = 'GFI.J'
index = '^J200.JO'
start_date = '2020-01-01'
end_date = '2023-08-15'

stock_data = fetch_data(ticker, start_date, end_date)

# Check if data retrieval was successful
if not stock_data:
    raise ValueError(f"Data for {ticker} is unavailable. The ticker might be delisted or there's an issue accessing its data.")

index_data = fetch_data(index, start_date, end_date)
if not index_data:
    raise ValueError(f"Data for {index} is unavailable. The index might be delisted or there's an issue accessing its data.")

# You might need to adjust the length of stock_returns and index_returns in case they are of different lengths
min_length = min(len(stock_returns), len(index_returns))
stock_returns = stock_returns[:min_length]
index_returns = index_returns[:min_length]

# Before calculating moving average, check for sufficient data
if len(stock_returns) < window_size:
    raise ValueError(f"Not enough data for calculating moving average. Need at least {window_size} days of returns, but got {len(stock_returns)} days.")

# Calculate moving average returns over a window of 5 days for the stock
moving_avg_returns = [np.mean(stock_returns[i:i+window_size]) for i in range(len(stock_returns) - window_size + 1)]


# Calculate moving average returns over a window of 5 days for the stock
window_size = 5
moving_avg_returns = [np.mean(stock_returns[i:i+window_size]) for i in range(len(stock_returns) - window_size + 1)]

def mcmc_forecast(returns, days=10, num_simulations=1000):
    forecasts = []
    for _ in range(num_simulations):
        price_path = [1]
        for _ in range(days):
            random_return = np.random.choice(returns)
            price_path.append(price_path[-1] * (1 + random_return))
        forecasts.append(price_path[-1])
    return forecasts

forecast_days = 10
forecasts = mcmc_forecast(moving_avg_returns, forecast_days)

plt.hist(forecasts, bins=50, alpha=0.75)
plt.title(f'MCMC Forecasted Price Distribution for {ticker} after {forecast_days} days (Using Moving Average Returns)')
plt.xlabel('Price (Normalized)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

forecasted_prices = [stock_data[-1] * f for f in forecasts]
print("Mean forecasted price after 10 days:", np.mean(forecasted_prices))
print("Standard deviation of forecast:", np.std(forecasted_prices))
