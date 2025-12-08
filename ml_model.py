# model/ml_model.py

# To separate the data to train the model
from sklearn.model_selection import train_test_split

# Metric evaluations
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class MLModelWithGraph:

    # Model Constructor
    def __init__(self, strategy):
        # Store the selected Strategy Pattern
        self.strategy = strategy

        # Build the correct ML pipeline from the strategy
        self.pipeline = self.strategy.build_pipeline()

        # Initialized train metrics
        self.train_mae = None
        self.train_mse = None
        self.train_r2 = None

    # Function use to build graph for correlated companies
    # It implements Networkx to convert the financial data
    # for each company ticker into a graph

    # Function that extracts the structural graph features for each company ticker

    # Function that trains the model with data from: (2020-2024)
    def train_model(self, df, graph_features_df):

        # This variable merges the stock data with the Networkx
        # Graph features
        merged = df.merge(graph_features_df, on="Ticker")

        # Training the data from: (2020–2024)
        train_data = merged[merged["Date"] < "2025-01-01"]

        # X: Input features
        # Y: Target variable

        # Variable that holds the Networkx feature columns
        feature_columns = ["Open", "High", "Low", "Volume",
                           "degree", "closeness", "betweenness",
                           "clustering"]

        X = train_data[feature_columns]
        y = train_data["Close"]

        # Using train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        # Training the pipeline
        self.pipeline.fit(X_train, y_train)

        # Validation
        y_pred = self.pipeline.predict(X_test)

        # MAE
        self.train_mae = mean_absolute_error(y_test, y_pred)
        # MSE
        self.train_mse = mean_squared_error(y_test, y_pred)
        # r2 score
        self.train_r2 = r2_score(y_test, y_pred)

        # Display the results: Visual only

        print("The train metrics for the years 2020-2024")
        print("MAE Value:", self.train_mae)
        print("MSE Value:", self.train_mse)
        print("R2 Value:", self.train_r2)


    # Function that predicts the early 2025 stock prices
    def predict_2025(self, df, graph_features_df):

        merged = df.merge(graph_features_df, on="Ticker")

        # Date validation

        test_data = merged[
            (merged["Date"] >= "2025-01-01") &
            (merged["Date"] <= "2025-05-31")
        ]

        # Validation of data (just in case)
        if test_data.empty:
            raise ValueError("No data found for this year.")

        X_test = test_data[["Open", "High", "Low", "Volume",
                            "degree", "closeness", "betweenness",
                            "clustering"]]

        y_true = test_data["Close"]
        dates = test_data["Date"]

        # Applying Pipeline
        values_predicted = self.pipeline.predict(X_test)

        # mae: Mean absolute error
        mae = mean_absolute_error(y_true, values_predicted)

        # Returns the values of the variables
        return dates, y_true, values_predicted, mae