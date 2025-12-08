# view/main_view.py

import tkinter as tk

from tkinter import ttk

# Use to implement the matplotlib graph into the GUI interface
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Use to create the graphs
import matplotlib.pyplot as plt

# Class for the main GUI Window

class MainView(tk.Frame):

    # Constructor

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.configure(bg="palegreen")

        # Title Window
        tk.Label(self, text= "Financial Market Analyzer",
                  font=("Roboto", 24, "bold"), bg="palegreen", fg="black").pack(pady=10)

        # Ticker Selector
        tk.Label(self, text="Select a Company Ticker:", font=("Roboto", 16, "bold"), bg="palegreen", fg="black").pack(pady=5)

        # This establishes a frame for ticker selection
        ticker_frame = tk.Frame(self, bg="palegreen")
        ticker_frame.pack(pady=0)

        # Added Scrollbar for a more friendly user experience
        scrollbar = tk.Scrollbar(ticker_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Set a listbox with the scrollbar
        self.ticker_listbox = tk.Listbox(ticker_frame, height=5, width=18, yscrollcommand=scrollbar.set,
                                         font = ("Roboto", 14, "bold"), bd=2, relief="solid", activestyle="dotbox")

        self.ticker_listbox.pack(side=tk.LEFT)
        scrollbar.config(command=self.ticker_listbox.yview)

        # GUI Buttons
        tk.Button(self, text="Run Prediction", font=("Roboto", 13, "bold"), command=self.on_run_prediction,
                  bg="#5fafda", fg="#000000", padx=5, pady=5).pack(pady=15)

        # Button to show company legend
        tk.Button(self, text="Show Ticker Legend", font=("Roboto", 11, "bold"), command=self.ticker_legend,
                  bg="springgreen", fg="#000000").pack(pady=10)

        # Frame for Graph
        self.graph_frame = tk.Frame(self, bg="palegreen")
        self.graph_frame.pack(fill="x", pady=10)


    # This method is used for the controller to set the company tickers
    def set_tickers(self, ticker_list):

        # Use to clear the listbox
        self.ticker_listbox.delete(0, tk.END)

        # To add the company tickers one by one
        # Using a for loop

        for ticker in ticker_list:
            self.ticker_listbox.insert(tk.END, ticker)

        # Sets the first ticker as default
        # Set(0) means it stars at 0
        # Validation with an if statement
        if ticker_list:
            self.ticker_listbox.select_set(0)

    # This method allows to read the selected ticker

    def on_run_prediction(self):

        # To get a selection index
        selection = self.ticker_listbox.curselection()

        # Selection validation

        if not selection:
            return None # No selection

        # Get the ticker from the listbox
        ticker = self.ticker_listbox.get(selection[0])

        # Here we call the controller class
        self.controller.handle_prediction(ticker)
        return None

    # This method shows the graph with the predictions
    def display_prediction_graph(self, ticker, dates, real_values, predicted_values, mae):

        # Clear old graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 3))

        # Adding outer and inner background color to the graphs
        fig.patch.set_facecolor("palegreen")
        ax.set_facecolor("azure")

        # Plot real values
        ax.plot(dates, real_values, label="Real Values (2025)", color="crimson")

        # Plot predictions
        ax.plot(dates, predicted_values, label="Predicted", color="mediumblue")

        plt.subplots_adjust(bottom=0.2)

        # Added gridlines
        ax.grid(True, linestyle="--", alpha=0.5, color="black")

        ax.set_title(f"Prediction Results for {ticker}", fontweight="bold")
        ax.set_xlabel("Date", fontsize=12, fontweight="bold")
        ax.set_ylabel("Close Price $", fontsize=12, fontweight="bold")
        ax.legend(facecolor="springgreen", edgecolor="red") # Adds legend

        # Embed graph in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()

        # Avoid stretching of the graph
        canvas_length = canvas.get_tk_widget()
        canvas_length.pack(pady=10)
        canvas_length.configure(width=1100, height=300)

    # Method for enabling a legend to identify each ticker with their respective company
    def ticker_legend(self):

        # Create a popup window
        legend = tk.Toplevel(self)
        legend.title("Ticker Legend")
        legend.geometry("450x280")

        tk.Label(legend, text="Ticker Abbreviations", font=("Roboto", 12, "bold")).pack(pady=5)

        frame = tk.Frame(legend)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        # Treeview
        columns = ("Ticker", "Company")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=20, yscrollcommand=scrollbar.set)

        scrollbar.config(command=tree.yview)

        # Define column headers
        tree.heading("Ticker", text="Ticker", anchor="center")
        tree.heading("Company", text="Company")

        # Column width & alignment
        tree.column("Ticker", width=80, anchor="center")
        tree.column("Company", width=260, anchor="w")

        tree.pack(fill="both", expand=True)

        ticker_dict = {

            # Technology Companies
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation",
            "GOOGL": "Alphabet Inc. (Class A)",
            "AMZN": "Amazon.com, Inc.",
            "NVDA": "NVIDIA Corporation",
            "META": "Meta Platforms, Inc.",
            "TSLA": "Tesla, Inc.",
            "NFLX": "Netflix, Inc.",
            "AMD": "Advanced Micro Devices, Inc.",
            "INTC": "Intel Corporation",
            "IBM": "International Business Machines Corporation",
            "ORCL": "Oracle Corporation",

            # Consumer and Retail Companies
            "WMT": "Walmart Inc.",
            "COST": "Costco Wholesale Corporation",
            "HD": "The Home Depot, Inc.",
            "DIS": "The Walt Disney Company",
            "NKE": "Nike, Inc.",
            "MCD": "McDonald's Corporation",
            "KO": "The Coca-Cola Company",
            "PEP": "PepsiCo, Inc.",
            "PG": "Procter & Gamble Company",

            # Automotive Companies
            "F": "Ford Motor Company",
            "GM": "General Motors Company",
            "TM": "Toyota Motor Corporation",

            # Finance Companies
            "JPM": "JPMorgan Chase & Co.",
            "BAC": "Bank of America Corporation",
            "WFC": "Wells Fargo & Company",
            "GS": "Goldman Sachs Group, Inc.",
            "V": "Visa Inc.",
            "MA": "Mastercard Incorporated",

            # Healthcare/Pharmaceutical Companies
            "PFE": "Pfizer Inc.",
            "JNJ": "Johnson & Johnson",
            "MRK": "Merck & Co., Inc.",
            "UNH": "UnitedHealth Group Incorporated",

            # Energy Companies
            "XOM": "Exxon Mobil Corporation",
            "CVX": "Chevron Corporation",
            "NEE": "NextEra Energy, Inc.",

            # Telecommunication Companies
            "VZ": "Verizon Communications Inc.",
            "T": "AT&T Inc."
        }

        for ticker, company in ticker_dict.items():
            tree.insert("", tk.END, values=(ticker, company))