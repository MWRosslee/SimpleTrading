
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

# Download data from Yahoo Finance
def fetch_data(ticker_symbol, start_date, end_date):
    try:
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
        return stock_data['Adj Close'].tolist()
    except Exception as e:
        raise ValueError(f"Error fetching data for {ticker_symbol}: {e}")

# Define your ticker and relevant date range
ticker = 'SHG.L'
start_date = '2022-01-01'
end_date = '2023-08-15'

stock_data = fetch_data(ticker, start_date, end_date)

# Compute daily returns for stock
stock_returns = [stock_data[i+1]/stock_data[i] - 1 for i in range(len(stock_data)-1)]

# Calculate moving average returns over a window of 5 days for the stock
window_size = 5
moving_avg_returns = [np.mean(stock_returns[i:i+window_size]) for i in range(len(stock_data) - window_size + 1)]

def mcmc_forecast(returns, days=60, num_simulations=1000):
    forecasts = []
    for _ in range(num_simulations):
        price_path = [stock_data[-1]]
        for _ in range(days):
            random_return = np.random.choice(returns)
            price_path.append(price_path[-1] * (1 + random_return))
        forecasts.append(price_path)
    return forecasts

forecast_days = 60
forecast_paths = mcmc_forecast(moving_avg_returns, forecast_days)

# Transpose forecast_paths for easier percentile calculation
forecast_matrix = np.array(forecast_paths).T
upper_bound = np.percentile(forecast_matrix, 95, axis=1)
lower_bound = np.percentile(forecast_matrix, 5, axis=1)
mean_forecast = np.mean(forecast_matrix, axis=1)

# Compute Fibonacci retracement levels based on the past 180 days
past_180_days = stock_data[-180:]
low_180 = min(past_180_days)
high_180 = max(past_180_days)
fibonacci_levels = [0.236, 0.382, 0.5, 0.618, 0.764]
fibonacci_prices = [(high_180 - low_180) * level + low_180 for level in fibonacci_levels]

plt.figure(figsize=(12, 7))
plt.plot(range(180), past_180_days, color='black', label='Past 180 days')
plt.plot(range(180, 180+forecast_days+1), mean_forecast, label="Mean Forecast", color='blue')
plt.fill_between(range(180, 180+forecast_days+1), lower_bound, upper_bound, color='gray', alpha=0.4, label="5th-95th Percentile")
for price, level in zip(fibonacci_prices, fibonacci_levels):
    plt.axhline(price, color='red', linestyle='--', alpha=0.7, label=f'Fibonacci {int(level * 100)}%')
plt.title(f'60-Day Price Forecast with Fibonacci Retracement for {ticker}')
plt.xlabel('Days from Now')
plt.ylabel('Price')
plt.legend(loc='best')
plt.grid(True)
plt.show()

# Save the projections to a CSV
forecast_df = pd.DataFrame({
    'Day': range(forecast_days+1),
    'Mean_Price': mean_forecast,
    'Upper_Bound': upper_bound,
    'Lower_Bound': lower_bound
})
csv_path = f"{ticker}_60day_forecast_with_fibonacci.csv"
forecast_df.to_csv(csv_path, index=False)

csv_path
