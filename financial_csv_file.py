import pandas as pd
from yahooquery import Ticker

# List of Tickers to include
tickers = [
    "AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","NFLX","AMD","INTC",
    "IBM","ORCL","WMT","COST","HD","DIS","NKE","MCD","KO","PEP",
    "PG","F","GM","TM","JPM","BAC","WFC","GS","V","MA",
    "PFE","JNJ","MRK","UNH","XOM","CVX","NEE","VZ","T"
]

# Date range
start_date = "2020-01-01"
end_date = "2025-05-01"

# Dataframe
df = pd.DataFrame()

print("Downloading data from Yahoo Finance...\n")

# Iterate tickers and download
for ticker in tickers:
    print("Downloading " + ticker + "...\n")

    try:
        stock = Ticker(ticker)
        history = stock.history(start=start_date, end=end_date)

        history = history.reset_index()

        history["Ticker"] = ticker

        df = pd.concat([df, history], ignore_index=True)

    except Exception as e:
        print(e)

# Rename columns
df = df.rename(columns={
    "date": "Date",
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "adjclose": "Adj Close",
    "volume": "Volume"
})

# Sort by date and ticker
df = df.sort_values(by=["Ticker", "Date"])

# Load CSV master file
csv_file = "stocks_data_2020_2025.csv"
df.to_csv(csv_file, index=False)

print("\nCSV master file created: " + csv_file)