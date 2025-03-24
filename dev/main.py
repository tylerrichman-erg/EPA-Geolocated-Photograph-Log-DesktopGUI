import configparser
import importlib.util
import os
import pandas as pd
import shutil
import tkinter as tk  # conda install anaconda::tk
from tkinter import ttk

### Initialize Pathways ###

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_module_path = os.path.join(base_dir, 'dev', 'config.py')
document_module_path = os.path.join(base_dir, 'dev', 'document.py')
helpers_module_path = os.path.join(base_dir, 'dev', 'helpers.py')
image_processing_module_path = os.path.join(base_dir, 'dev', 'image_processing.py')
map_module_path = os.path.join(base_dir, 'dev', 'map.py')
setup_module_path = os.path.join(base_dir, 'setup.py')


### Load Python Modules ###

config_setup = importlib.util.spec_from_file_location("config", config_module_path)
config = importlib.util.module_from_spec(config_setup)
config_setup.loader.exec_module(config)

document_setup = importlib.util.spec_from_file_location("document", document_module_path)
document = importlib.util.module_from_spec(document_setup)
document_setup.loader.exec_module(document)

helpers_setup = importlib.util.spec_from_file_location("helpers", helpers_module_path)
helpers = importlib.util.module_from_spec(helpers_setup)
helpers_setup.loader.exec_module(helpers)

image_processing_setup = importlib.util.spec_from_file_location("image_processing", image_processing_module_path)
image_processing = importlib.util.module_from_spec(image_processing_setup)
image_processing_setup.loader.exec_module(image_processing)

map_setup = importlib.util.spec_from_file_location("map", map_module_path)
map = importlib.util.module_from_spec(map_setup)
map_setup.loader.exec_module(map)

spec_setup = importlib.util.spec_from_file_location("setup", setup_module_path)
setup = importlib.util.module_from_spec(spec_setup)
spec_setup.loader.exec_module(setup)

### Initialize Application ###

App = setup.App()
App.workspace_path = base_dir
App.config_file_path = os.path.join(App.workspace_path, 'config.ini')

### Load Configuration ###

c = configparser.ConfigParser()
c.read(App.config_file_path)
Config = config.Config(c)

### Create Main Window ###

root = tk.Tk()
root.title(Config.main_window_title)
root.geometry(Config.main_window_geometry)
root.resizable(
    width=Config.main_window_resizable_width, 
    height=Config.main_window_resizable_height
)

### Create Title ###

tk.Label(
    root, 
    text = "EPA Geolocated Photograph Log", 
    font = ("Helvetica", 16, "bold")
    ).pack(pady=(10, 20))

### Create Text Entry Prompts ###

tk.Label(
    root, 
    text = "Photographer",
    font = ("Helvetica", 11, "bold")
    ).pack(pady = (0, 0))
photographer_entry = tk.Entry(
    root, 
    width=40
    )
photographer_entry.pack(pady = (3, 15))

tk.Label(
    root, 
    text = "Facility",
    font = ("Helvetica", 11, "bold")
    ).pack(pady = (0, 0))
facility_entry = tk.Entry(
    root, 
    width=40
    )
facility_entry.pack(pady = (3, 15))

tk.Label(
    root, 
    text="Inspection Date",
    font=("Helvetica", 11, "bold")
    ).pack(pady = (0, 0))
inspection_date_entry = tk.Entry(
    root, 
    width=40
    )
inspection_date_entry.pack(pady = (3, 15))

### Create Table ###

tk.Label(
    root, 
    text="Photographs and GPS Data",
    font=("Helvetica", 11, "bold")
    ).pack(pady = (0, 0))

columns = [
    Config.table_field_names_file_name, 
    Config.table_field_names_latitude,
    Config.table_field_names_longitude,
    Config.table_field_names_bearing
]

tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(pady = (3, 5))

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

    ## Select Output File Location ##

    output_file_path = helpers.select_output_report_location_from_filedialog()

    ## Update Data Frame ##

    global df
    updated_data = []
    for item in tree.get_children():
        updated_data.append(tree.item(item, "values"))

    df = pd.DataFrame(updated_data, columns=columns)

    ## Create Temporary Locations for Images ##

    temp_overview_folder_path = os.path.join(App.workspace_path, "temp/overview")

    os.makedirs(
        temp_overview_folder_path, 
        exist_ok = True
        )

    temp_imagery_folder_path = os.path.join(App.workspace_path, "temp/imagery_base")

    os.makedirs(
        temp_imagery_folder_path, 
        exist_ok = True
        )

    temp_terrain_folder_path = os.path.join(App.workspace_path, "temp/terrain_base")

    os.makedirs(
        temp_terrain_folder_path, 
        exist_ok = True
        )

    ## Create Overview Map ##

    map.generate_overview_map(
        df = df,
        output_folder = temp_overview_folder_path,
        filename_field = Config.table_field_names_file_name, 
        latitude_field = Config.table_field_names_latitude, 
        longitude_field = Config.table_field_names_longitude, 
        bearing_field = Config.table_field_names_bearing, 
        tiles = Config.overview_map_basemap,
        zoom = Config.overview_map_zoom, 
        img_width = Config.overview_map_width, 
        img_height = Config.overview_map_height, 
        map_control_scale = Config.map_control_scale, 
        map_zoom_control = Config.map_zoom_control, 
        map_dragging = Config.map_dragging, 
        icon_name = Config.icon_name, 
        icon_size = Config.icon_size, 
        icon_shape = Config.icon_shape, 
        icon_border_color = Config.icon_border_color, 
        icon_border_width = Config.icon_border_width, 
        icon_background_color = Config.icon_background_color, 
        icon_text_color = Config.icon_text_color
        )

    ## Create Individual Picture Maps ##

    map.generate_individual_maps(
        df = df,
        output_folder = temp_imagery_folder_path,
        filename_field = Config.table_field_names_file_name, 
        latitude_field = Config.table_field_names_latitude, 
        longitude_field = Config.table_field_names_longitude, 
        bearing_field = Config.table_field_names_bearing, 
        tiles = Config.individual_map_imagery_basemap,
        zoom = Config.individual_map_zoom, 
        img_width = Config.individual_map_width, 
        img_height = Config.individual_map_height, 
        map_control_scale = Config.map_control_scale, 
        map_zoom_control = Config.map_zoom_control, 
        map_dragging = Config.map_dragging, 
        icon_name = Config.icon_name, 
        icon_size = Config.icon_size, 
        icon_shape = Config.icon_shape, 
        icon_border_color = Config.icon_border_color, 
        icon_border_width = Config.icon_border_width, 
        icon_background_color = Config.icon_background_color, 
        icon_text_color = Config.icon_text_color
        )

    map.generate_individual_maps(
        df = df,
        output_folder = temp_terrain_folder_path,
        filename_field = Config.table_field_names_file_name, 
        latitude_field = Config.table_field_names_latitude, 
        longitude_field = Config.table_field_names_longitude, 
        bearing_field = Config.table_field_names_bearing, 
        tiles = Config.individual_map_terrain_basemap,
        zoom = Config.individual_map_zoom, 
        img_width = Config.individual_map_width, 
        img_height = Config.individual_map_height, 
        map_control_scale = Config.map_control_scale, 
        map_zoom_control = Config.map_zoom_control, 
        map_dragging = Config.map_dragging, 
        icon_name = Config.icon_name, 
        icon_size = Config.icon_size, 
        icon_shape = Config.icon_shape, 
        icon_border_color = Config.icon_border_color, 
        icon_border_width = Config.icon_border_width, 
        icon_background_color = Config.icon_background_color, 
        icon_text_color = Config.icon_text_color
        )

    ## Generate Report ##

    document.generate_report(
        df = df,
        output_file_path = output_file_path,
        photographer = photographer_entry.get(),
        facility = facility_entry.get(),
        inspection_date = inspection_date_entry.get(),
        image_files = image_files,
        overview_title = Config.document_overview_title,
        overview_text = helpers.read_text_file(os.path.join(App.workspace_path, Config.document_overview_text_rel_path)),
        overview_img_width_in = int(Config.document_overview_img_width_in),
        overview_img_folder_path = temp_overview_folder_path,
        individual_photo_img_width_in = int(Config.document_photo_img_width_in),
        individual_imagery_folder_path = temp_imagery_folder_path,
        individual_imagery_img_width_in = int(Config.document_imagery_img_width_in),
        individual_terrain_folder_path = temp_terrain_folder_path,
        individual_terrain_img_width_in = int(Config.document_terrain_img_width_in),
        individual_header_end_text = Config.document_header_end_text,
        individual_footer_beginning_text = Config.document_footer_beginning_text
        )

    ## Remove Temporate Image Folder ##

    shutil.rmtree(os.path.join(App.workspace_path, "temp"))

### Create Select Button ###

select_button = tk.Button(
    root, 
    text = Config.select_button_text,
    width = 56,
    command = create_image_GPS_table
)
select_button.pack(
    pady = (0, 0)
)

### Create Generate Report Button ###

generate_button = tk.Button(
    root, 
    text = Config.generate_report_button_text, 
    width = 20,
    font=("Helvetica", 14, "bold"),
    command = generate_report
)
generate_button.pack(
    pady = (20, 0)
)

### Launch Application ###

root.mainloop()
