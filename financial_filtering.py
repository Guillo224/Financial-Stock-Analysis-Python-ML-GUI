# This script loads the csv file data, cleans the data using pandas,
# filters the company tickers, and the information by date

# Importing pandas
import pandas as pd

# For abstract classes
from abc import ABC, abstractmethod

# Define abstract class for the data of the structure
class DataProcessor(ABC):

    @abstractmethod
    # To load data from the file
    def data_load(self):
        pass

    @abstractmethod
    # Obtains the company tickers from the file
    def tickers(self):
        pass

    @abstractmethod
    # Use to filter the company tickers in the file
    def filtered_tickers(self, ticker):
        pass

    @abstractmethod
    # Filter the data by between initial date to final date
    # 2020-2025
    def filtered_by_date(self, df, initial_date, end_date):
        pass

# This is the concrete class for the data processor
# Extends the DataProcessor class
class StockDataProcessor(DataProcessor):

    # Constructor
    def __init__(self, path_csv):
        self.path_csv = path_csv # Store path to the csv file
        self.df = None # Hold database

    # Read the file and load the data
    def data_load(self):
        self.df = pd.read_csv(self.path_csv)
        # Converting dates to datetime format
        self.df["Date"] = pd.to_datetime(self.df["Date"])
        self.df = self.df.dropna(subset=["Date"]) # Filtered rows with invalid data
        return self.df # Returns the filtered data

    def tickers(self):

        tickers = list(set(self.df["Ticker"])) # Converts tickers into a list
        tickers.sort() # Sort the tickers
        return tickers # Return the list of sorted tickers

    def filtered_tickers(self, ticker):
        ticker_df = self.df[self.df["Ticker"] == ticker] # Filtered the rows by ticker name
        return ticker_df.sort_values(by=["Date"]) # Sort the results by date

    def filtered_by_date(self, df, initial_date, end_date):

        # Validation of date
        if initial_date > end_date:
            raise ValueError("Initial date cannot be before end date.")

        # Filtering date
        df_filtered = df[(df["Date"] >= initial_date) & (df["Date"] <= end_date)]
        return df_filtered