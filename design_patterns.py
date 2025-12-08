# Design Patterns Module
# This module implements the Strategy Pattern for ML models
# and the Factory Pattern for data processors and graph creation

from abc import ABC, abstractmethod # For abstract classes
# Allow building ML pipelines
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Importing the StockDataProcessor concrete class (Factory nuevo)
from financial_filtering import StockDataProcessor

import networkx as nx # For graph creation
import pandas as pd # Used for graph feature DataFrame

#==================================#
# Strategy Design Pattern          #
#==================================#

# Strategy Interface
class MLStrategy(ABC):

    # Abstract method that is overridden by each concrete strategy and returns a Pipeline object
    @abstractmethod
    def build_pipeline(self):
        pass

# Concrete Strategy 1: Linear Regression
class LinearRegressionStrategy (MLStrategy):

    # Define a pipeline that applies scaling and uses Linear Regression
    def build_pipeline(self):
        # This pipeline always has a scaler followed by the chosen model
        return Pipeline([
            ("scaler", StandardScaler()), # Normalize feature ranges
            ("model", LinearRegression()) # Actual ML algorithm
         ])

# Concrete Strategy 2: Random Forest
class RandomForestStrategy (MLStrategy):

    # Another concrete strategy that allows switching the ML model to Random Forest
    # without changing other code
    def build_pipeline(self):
        return Pipeline([
            ("scaler", StandardScaler()),
            ("model", RandomForestRegressor())
        ])


#==========================================#
# Factory Pattern - Data Processor         #
#==========================================#

# Factory responsible for creating data processor object correctly
class FinancialFactory:

    # Method for returning the correct processor based on the type of data
    @staticmethod
    def build_processor(type_data, file_path):

        if type_data == "stocks":
            # Creates a StockDataProcessor for handling dara from the csv
            return StockDataProcessor(file_path)

        # If an unknown type, it raises the exception
        raise ValueError("Invalid type_data")


#==========================================#
# Factory Pattern - Graph Processor        #
#==========================================#

# Factory responsible for building NetworkX graph structures based on
# a selected graph type
class GraphFactory:

    # Entry point for creating graphs
    @staticmethod
    def build_graph(graph_type, df):

        # Determine what kind of graph should be built
        if graph_type == "correlation":
            # Delegate graph creation to private helper method
            return GraphFactory._build_correlation_graph(df)

        # If an unknown type, it raises the exception
        else:
            raise ValueError("Invalid graph type")

    # Build a correlation-based graph
    # Each node = a stock ticker
    # An edge exists if correlation between tickers > 0.6
    @staticmethod
    def _build_correlation_graph(df):

        graph = nx.Graph()

        # Add one node for each unique stock ticker
        tickers = df["Ticker"].unique()
        for ticker in tickers:
            graph.add_node(ticker)

        # Pivot table: each column becomes a ticker, aligned by date
        pivot = df.pivot(index="Date", columns="Ticker", values="Close")

        # Correlation matrix between tickers
        correlated = pivot.corr()

        # Add edges between strongly correlated tickers
        for i in correlated.columns:
            for j in correlated.columns:
                if i != j and correlated.loc[i, j] > 0.6:
                    # Edge weight = correlation value
                    graph.add_edge(i, j, weight=float(correlated.loc[i, j]))

        return graph

    # Compute graph features using Networkx: degree centrality, closeness, between, clustering
    @staticmethod
    def extract_features(graph):

        # Number of strong connections
        degree = nx.degree_centrality(graph)

        # influence based on distance
        closeness = nx.closeness_centrality(graph)

        # Bridge importance
        betweenness = nx.betweenness_centrality(graph)

        # Local connectivity density
        clustering = nx.clustering(graph)

        # Create dataFrame where each row corresponds to one ticker
        return pd.DataFrame({
            "Ticker": list(graph.nodes),
            "degree": [degree[t] for t in graph.nodes],
            "closeness": [closeness[t] for t in graph.nodes],
            "betweenness": [betweenness[t] for t in graph.nodes],
            "clustering": [clustering[t] for t in graph.nodes],
        })