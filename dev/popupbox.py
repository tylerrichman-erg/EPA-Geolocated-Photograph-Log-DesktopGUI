import tkinter as tk
from tkinter import messagebox

def error_message(e):

    #root = tk.Tk()
    #root.withdraw()  # Hide the root window
    error_type = type(e).__name__
    error_msg = f"{error_type}: {e}"
    messagebox.showerror("Error", error_msg)
   