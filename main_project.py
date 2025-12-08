# main_project.py

import tkinter as tk
from first_view import ViewMenu
from controller import Controller


def main():

    window = tk.Tk()
    window.title("Stock Analysis App") # Title
    window.geometry("600x300")
    window.configure(bg="black")

    w_image = tk.PhotoImage(file="BagJ.png")
    window.iconphoto(True, w_image)

    # Instance of the controller class
    controller = Controller(window)

    view = ViewMenu(window, controller)

    # Assign command to controller
    controller.view = view

    # Show view
    view.pack(expand=True, fill="both")

    # Runs application
    window.mainloop()

if __name__ == "__main__":
    main()