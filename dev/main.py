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
image_processing_module_path = os.path.join(base_dir, 'dev', 'image_processing.py')
document_module_path = os.path.join(base_dir, 'dev', 'document.py')

### Load Python Modules ###

spec_setup = importlib.util.spec_from_file_location("setup", setup_module_path)
setup = importlib.util.module_from_spec(spec_setup)
spec_setup.loader.exec_module(setup)

helpers_setup = importlib.util.spec_from_file_location("helpers", helpers_module_path)
helpers = importlib.util.module_from_spec(helpers_setup)
helpers_setup.loader.exec_module(helpers)

image_processing_setup = importlib.util.spec_from_file_location("image_processing", image_processing_module_path)
image_processing = importlib.util.module_from_spec(image_processing_setup)
image_processing_setup.loader.exec_module(image_processing)

document_setup = importlib.util.spec_from_file_location("document", document_module_path)
document = importlib.util.module_from_spec(document_setup)
document_setup.loader.exec_module(document)

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

### Create Text Entry Prompts ###

tk.Label(root, text="Photographer").pack(pady=0)
photographer_entry = tk.Entry(root)
photographer_entry.pack(pady=0)

tk.Label(root, text="Facility").pack(pady=0)
facility_entry = tk.Entry(root)
facility_entry.pack(pady=0)

tk.Label(root, text="Inspection Date").pack(pady=0)
inspection_date_entry = tk.Entry(root)
inspection_date_entry.pack(pady=0)

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

    global image_files
    image_files = helpers.select_images_from_filedialog()
    global df
    df = pd.DataFrame(columns=columns)

    for image_file in image_files:
        image_file_GPS_data = image_processing.extract_GPS_data_from_image(image_file)
        image_file_cleaned_GPS_data = image_processing.extract_coordinates_and_bearing_from_GPS_data(image_file_GPS_data)
        df.loc[len(df)] = [
            os.path.basename(image_file),
            image_file_cleaned_GPS_data[0],
            image_file_cleaned_GPS_data[1],
            image_file_cleaned_GPS_data[2]
        ]
    
    for i in tree.get_children():
        tree.delete(i)  # Clear previous data
    
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

### Function to Generate Report ###

def generate_report():

    output_file_path = helpers.select_output_report_location_from_filedialog()

    global df
    updated_data = []
    for item in tree.get_children():
        updated_data.append(tree.item(item, "values"))

    df = pd.DataFrame(updated_data, columns=columns)

    document.generate_report(
        df = df,
        output_file_path = output_file_path,
        photographer = photographer_entry.get(),
        facility = facility_entry.get(),
        inspection_date = inspection_date_entry.get(),
        image_files = image_files,
        overview_title = Config.document_overview_title,
        overview_text = helpers.read_text_file(os.path.join(App.workspace_path, Config.document_overview_text_rel_path)),
        overview_img_path = r"C:\Users\trichman\Tyler\Tools\Development\EPA Geolocated Photograph Log Desktop GUI\Placeholder Images\Yellow0.jpg",
        overview_img_width_in = int(Config.document_overview_img_width_in)
        )

### Create Buttons ###

select_button = tk.Button(
    root, 
    text = Config.select_button_text, 
    command = create_image_GPS_table
)
select_button.pack(
    pady = Config.select_button_pady
)

generate_button = tk.Button(
    root, 
    text = Config.generate_report_button_text, 
    command = generate_report
)
generate_button.pack(
    pady = Config.generate_report_button_pady
)

### Launch Application ###

root.mainloop()
