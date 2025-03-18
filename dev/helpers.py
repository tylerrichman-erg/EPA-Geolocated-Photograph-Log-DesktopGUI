######### helpers.py #########

"""
File Name: helpers.py
Developer(s): Tyler Richman (tyler.richman@erg.com), Mark Fowler (mark.fowler@erg.com)
Last Update: 01/21/2025
Description: 
"""

import tkinter as tk #conda install anaconda::tk
from tkinter import filedialog

def select_images_from_filedialog():
    return filedialog.askopenfilenames()

def select_output_report_location_from_filedialog():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".docx",
        filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
    )
    return file_path

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content