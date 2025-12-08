# Intro window

import tkinter as tk
from PIL import ImageTk, Image


# Defining class for the main menu

class ViewMenu(tk.Frame):

    # Method for the view
    # Constructor
    def __init__(self, window, controller):
        super().__init__(window)
        self.controller = controller
        self.configure(bg="black")

        # Creating a frame for the images

        image_frame = tk.Frame(self, bg="black")
        image_frame.pack(expand=True, fill="both", pady=40)

        # Added columns

        image_frame.grid_columnconfigure(0, weight=1)
        image_frame.grid_columnconfigure(1, weight=1)
        image_frame.grid_columnconfigure(2, weight=1)

        # Added row

        image_frame.grid_rowconfigure(0, weight=1)
        image_frame.grid_rowconfigure(1, weight=1)
        image_frame.grid_rowconfigure(2, weight=1)

        # Window Title

        bg_title = tk.Label(image_frame, text="Welcome to the Financial Stock Analyzer💰",
                            font=("Roboto", 30, "bold"), bg="black", fg="gold")

        bg_title.grid(row=0, column=1, pady=20)

        # Adding first image: The left image
        image_left = Image.open("MoneyBagJ.png")
        image_left = image_left.resize((280, 280))
        self.image_left = ImageTk.PhotoImage(image_left)

        tk.Label(image_frame, image=self.image_left, bg="black").grid(row=1, column=0, pady=20)

        # Adding button
        tk.Button(image_frame, text="Access Application",
                  font=("Roboto", 20, "bold"), bg= "dimgray", fg="black",
                  command=self.go_to_app).grid(row=1, column=1, pady=10)

        # Creating the second image
        image_right = Image.open("StockLineJ.png")
        image_right = image_right.resize((280, 280))
        self.image_right = ImageTk.PhotoImage(image_right)

        tk.Label(image_frame, image=self.image_right, bg="black").grid(row=1, column=2, pady=20)

    # This method allows the user to access the main application after the button is clicked

    def go_to_app(self):

        self.controller.go_to_app()