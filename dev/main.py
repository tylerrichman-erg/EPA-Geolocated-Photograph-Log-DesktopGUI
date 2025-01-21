######### main.py #########

"""
File Name: main.py
Developer(s): Tyler Richman (tyler.richman@erg.com), Mark Fowler (mark.fowler@erg.com)
Last Update: 01/21/2025
Description: 
"""

### Import Libraries ###

import configparser
import importlib.util
import os
import tkinter as tk #conda install anaconda::tk

### Initialize Pathways ###

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
setup_module_path = os.path.join(base_dir, 'setup.py')

### Load Python Modules ###

spec_setup = importlib.util.spec_from_file_location("setup", setup_module_path)
setup = importlib.util.module_from_spec(spec_setup)
spec_setup.loader.exec_module(setup)

#!! Add code that loads helpers.py here.

### Initialize Application ###

App = setup.App()
App.workspace_path = base_dir
App.config_file_path = os.path.join(App.workspace_path, 'config.ini')

### Load Configuration ###

config = setup.configparser.ConfigParser()
config.read(App.config_file_path)
Config = setup.Config(config)

### Create Main Window ###

root = tk.Tk()
root.title(Config.main_window_title)
root.geometry(Config.main_window_geometry)

#!! Add GUI and function calls needed to run the application here.

### Launch Application ###

root.mainloop()