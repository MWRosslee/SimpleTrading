import talib as ta
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Constants
LOOKBACK = 10


# Functions
def fetch_data(ticker_symbol, start_date, end_date):
    return yf.download(ticker_symbol, start=start_date, end=end_date)


def prepare_data(data):
    # Add technical indicators as features
    data['RSI'] = ta.RSI(data['Close'])
    data['Momentum'] = data['Close'] - data['Close'].shift(4)
    data['Stochastic'] = ta.STOCH(data['High'], data['Low'], data['Close'])[1]

    # Define labels: buy (1), sell (-1), hold (0)
    data['Label'] = 0
    data['Label'] = data['Label'].where(data['Close'].shift(-1) <= data['Close'], 1)
    data['Label'] = data['Label'].where(data['Close'].shift(-1) >= data['Close'], -1)

    # Drop NaN rows (because of technical indicators)
    data = data.dropna()

    return data[['RSI', 'Momentum', 'Stochastic', 'Label']]


def main():
    ticker_symbol = input("Enter the ticker symbol (e.g. 'AAPL'): ")
    start_date = input("Enter the start date (format: YYYY-MM-DD): ")
    end_date = input("Enter the end date (format: YYYY-MM-DD): ")

    data = fetch_data(ticker_symbol, start_date, end_date)
    df = prepare_data(data)

    # Splitting data into train and test datasets
    X = df[['RSI', 'Momentum', 'Stochastic']]
    y = df['Label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate the model
    predictions = clf.predict(X_test)
    print(classification_report(y_test, predictions))

    # Trading strategy
    transactions = []
    buy_dates, sell_dates, buy_prices, sell_prices = [], [], [], []

    predictions_df = data[['RSI', 'Momentum', 'Stochastic']].dropna()
    predictions_df['Predictions'] = clf.predict(predictions_df)
    data = data.merge(predictions_df['Predictions'], left_index=True, right_index=True, how='left')

    cash = 10000000
    position = 0
    for i, row in data.iterrows():
        if row['Predictions'] == 1 and cash * 0.5 >= row['Close']:
            # Use only 100% of available cash for buying
            position = (cash * 1.0) // row['Close']
            cash -= position * row['Close']
            transactions.append({
                'Date': i,
                'Action': 'Buy',
                'Price': row['Close'],
                'Quantity': position,
                'Cash': cash
            })
            buy_dates.append(i)
            buy_prices.append(row['Close'])
        elif row['Predictions'] == -1 and position > 0:
            cash += position * row['Close']
            transactions.append({
                'Date': i,
                'Action': 'Sell',
                'Price': row['Close'],
                'Quantity': position,
                'Cash': cash
            })
            sell_dates.append(i)
            sell_prices.append(row['Close'])
            position = 0


    # Save transactions to CSV
    transactions_df = pd.DataFrame(transactions)
    transactions_df.to_csv(f"{ticker_symbol}_transactions.csv", index=False)

    # Plot trades on share price
    plt.figure(figsize=(15, 7))
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')
    plt.scatter(buy_dates, buy_prices, marker='^', color='g', label='Buy', alpha=1)
    plt.scatter(sell_dates, sell_prices, marker='v', color='r', label='Sell', alpha=1)
    plt.title(f"Trades on {ticker_symbol}")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()