import configparser
import importlib.util
import os
import pandas as pd
import tkinter as tk  # conda install anaconda::tk
from tkinter import ttk

### Initialize Pathways ###
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
setup_module_path = os.path.join(base_dir, 'setup.py')
helpers_module_path = os.path.join(base_dir, 'dev', 'helpers.py')

### Load Python Modules ###
spec_setup = importlib.util.spec_from_file_location("setup", setup_module_path)
setup = importlib.util.module_from_spec(spec_setup)
spec_setup.loader.exec_module(setup)

helpers_setup = importlib.util.spec_from_file_location("helpers", helpers_module_path)
helpers = importlib.util.module_from_spec(helpers_setup)
helpers_setup.loader.exec_module(helpers)

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
root.resizable(
    width=Config.main_window_resizable_width, 
    height=Config.main_window_resizable_height
)

### Create Table ###
columns = [
    Config.table_field_names_file_name, 
    Config.table_field_names_latitude,
    Config.table_field_names_longitude,
    Config.table_field_names_bearing
]

tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(pady=0)

### Function to Edit Cell ###
def on_double_click(event):
    selected_item = tree.selection()[0]
    column_id = tree.identify_column(event.x)
    column_index = int(column_id[1:]) - 1
    
    x, y, width, height = tree.bbox(selected_item, column_index)
    entry = tk.Entry(
        root, 
        bg = Config.table_selected_cell_bg
        )
    entry.place(x=x, y=y+tree.winfo_y(), width=width, height=height)
    entry.insert(0, tree.item(selected_item, "values")[column_index])
    
    def save_edit():
        values = list(tree.item(selected_item, "values"))
        values[column_index] = entry.get()
        tree.item(selected_item, values=values)
        entry.destroy()
    
    entry.bind("<Return>", lambda event: save_edit())
    entry.focus()

tree.bind("<Double-1>", on_double_click)

### Function to Populate Table ###
def create_image_GPS_table():
    input_files = helpers.select_images_from_filedialog()
    global df
    df = pd.DataFrame(columns=columns)

    for input_file in input_files:
        input_file_GPS_data = helpers.extract_GPS_data_from_image(input_file)
        input_file_cleaned_GPS_data = helpers.extract_coordinates_and_bearing_from_GPS_data(input_file_GPS_data)
        df.loc[len(df)] = [
            os.path.basename(input_file), 
            input_file_cleaned_GPS_data[0], 
            input_file_cleaned_GPS_data[1], 
            input_file_cleaned_GPS_data[2]
        ]
    
    for i in tree.get_children():
        tree.delete(i)  # Clear previous data
    
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

def generate_report():
    global df
    updated_data = []
    for item in tree.get_children():
        updated_data.append(tree.item(item, "values"))
    
    df = pd.DataFrame(updated_data, columns=columns)
    print(df)  # Replace this with file saving or further processing

### Create Buttons ###
select_button = tk.Button(
    root, 
    text=Config.select_button_text, 
    command=create_image_GPS_table
)
select_button.pack(
    pady=Config.select_button_pady
)

generate_button = tk.Button(
    root, 
    text=Config.generate_report_button_text, 
    command=generate_report
)
generate_button.pack(
    pady=Config.generate_report_button_pady
)

### Launch Application ###
root.mainloop()
