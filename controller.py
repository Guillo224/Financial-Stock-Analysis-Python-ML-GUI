# controller/controller.py

# Importing the main view class

from main_view import MainView
from design_patterns import LinearRegressionStrategy, FinancialFactory, GraphFactory

from ml_model import MLModelWithGraph

# Class that connects the tkinter GUI and the ML model training
class Controller:

    def __init__(self, parent):
        self.parent = parent
        self.view = None

        # Factory pattern implementation
        self.processor = FinancialFactory.build_processor("stocks", "stocks_data_2020_2025.csv")

        # Default ML model strategy (Linear Regression)
        self.current_strategy = LinearRegressionStrategy()
        self.ml_model = MLModelWithGraph(self.current_strategy)

        # The dataframes
        self.df = None
        self.graph_features_df = None


    # Method to initialize the app
    def initialize(self):

        # Load data
        self.df = self.processor.data_load()

        # Load tickers into the GUI
        tickers = self.processor.tickers()
        self.view.set_tickers(tickers)

        # Build the graph from the entire dataset
        graph = GraphFactory.build_graph("correlation", self.df)

        # Extract graph features using Factory Pattern
        self.graph_features_df = GraphFactory.extract_features(graph)

        # Train initial model
        self.ml_model.train_model(self.df, self.graph_features_df)

    # Method for the first and main view of the app
    def go_to_app(self):

        if self.view:
            # Destroy the first view window
            self.view.destroy()

        # from main_view import MainView
        self.view = MainView(self.parent, self)

        # Show the Main View
        self.view.pack(expand=True, fill="both")

        # Initialize the project logic once access the main view
        self.initialize()

    # Method that handles the prediction for each ticker
    def handle_prediction(self, ticker):

        df_ticker = self.processor.filtered_tickers(ticker)

        # To obtain the prediction results
        dates, real_values, predicted_values, mae = self.ml_model.predict_2025(df_ticker, self.graph_features_df)

        # Send data to GUI for plotting
        self.view.display_prediction_graph(
            ticker, dates, real_values, predicted_values, mae)
