import configparser
from datetime import datetime
import importlib.util
import os
import pandas as pd
import shutil
import threading
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import sys

import docx
from PIL import Image, ImageTk
import piexif
import folium
import folium.plugins as plugins
from tkinter import filedialog

### Initialize Pathways ###

if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_base_path():
    if getattr(sys, 'frozen', False):  # If bundled by PyInstaller
        return sys._MEIPASS  # Temporary folder where PyInstaller unpacks the files
    else:
        return os.path.dirname(os.path.abspath(__file__))
base_dir = get_base_path()

config_module_path = os.path.join(base_dir, 'dev', 'config.py')
document_module_path = os.path.join(base_dir, 'dev', 'document.py')
helpers_module_path = os.path.join(base_dir, 'dev', 'helpers.py')
image_processing_module_path = os.path.join(base_dir, 'dev', 'image_processing.py')
map_module_path = os.path.join(base_dir, 'dev', 'map.py')
popupbox_module_path = os.path.join(base_dir, 'dev', 'popupbox.py')
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

popupbox_setup = importlib.util.spec_from_file_location("popupbox", popupbox_module_path)
popupbox = importlib.util.module_from_spec(popupbox_setup)
popupbox_setup.loader.exec_module(popupbox)

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

### Functions to Call in Application ###

def on_double_click(event):
    try:
        # Identify row and column under the click
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = tree.identify_row(event.y)
        column = tree.identify_column(event.x)

        x, y, width, height = tree.bbox(row_id, column)

        # Get current value
        item = tree.item(row_id)
        col_index = int(column[1:]) - 1
        current_value = item["values"][col_index]

        # Create entry widget
        entry = tk.Entry(tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, current_value)
        entry.focus()

        def save_edit(event):
            new_value = entry.get()
            values = list(tree.item(row_id)["values"])
            values[col_index] = new_value
            tree.item(row_id, values=values)
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    except Exception as e:
        popupbox.error_message(e)
        root.destroy()
        sys.exit()

def create_image_GPS_table():
    """
    Function to create a table of image GPS data.
    """

    try:
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
    
    except Exception as e:
        popupbox.error_message(e)
        root.destroy()
        sys.exit()

def open_file_dialog():
    """
    Function to open a file dialog for selecting the output report location.
    """

    try:
        global output_file_path

        output_file_path = helpers.select_output_report_location_from_filedialog()
        
        if output_file_path:
            file_path_entry.config(state = 'normal')
            file_path_entry.delete(0, tk.END)
            file_path_entry.insert(0, output_file_path)
            file_path_entry.config(state = 'readonly')

    except Exception as e:
        popupbox.error_message(e)
        root.destroy()
        sys.exit()

def generate_report():
    """
    Function to generate a report from the image GPS data.
    """

    try:

        ## Select Output File Location ##

        #output_file_path = helpers.select_output_report_location_from_filedialog()

        ## Update Data Frame ##

        global df
        updated_data = []
        for item in tree.get_children():
            updated_data.append(tree.item(item, "values"))

        df = pd.DataFrame(updated_data, columns=columns)

        ## Create Temporary Locations for Images ##
        
        temp_image_folder_path = os.path.join(App.workspace_path, "temp/images")

        os.makedirs(
            temp_image_folder_path,
            exist_ok = True
            )

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

        ## Edit Input Images ##

        photoNumber = 0
        for index, row in df.iterrows():
            photoNumber += 1
            image_processing.add_border(
                input_path = image_files[photoNumber - 1], 
                output_path = os.path.join(temp_image_folder_path, os.path.basename(image_files[photoNumber - 1]))
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

        map.generate_individual_map(
            df = df,
            output_folder = temp_imagery_folder_path,
            no_img_path = os.path.join(App.workspace_path, Config.individual_no_image_path),
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

        map.generate_individual_map(
            df = df,
            output_folder = temp_terrain_folder_path,
            no_img_path = os.path.join(App.workspace_path, Config.individual_no_image_path),
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
            filename_field = Config.table_field_names_file_name,
            output_file_path = output_file_path,
            photographer = photographer_entry.get(),
            facility = facility_entry.get(),
            inspection_date = inspection_date_entry.get_date().strftime('%Y-%m-%d'),
            image_files = image_files,
            overview_title = Config.document_overview_title,
            overview_text = helpers.read_text_file(os.path.join(App.workspace_path, Config.document_overview_text_rel_path)),
            overview_img_width_in = int(Config.document_overview_img_width_in),
            overview_img_folder_path = temp_overview_folder_path,
            individual_photo_folder_path = temp_image_folder_path,
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

        ## Close Progress Window ##

        progress_bar.stop()
        progress_win.destroy()

        ## Open Popup Notifying Results ##

        complete_win = tk.Toplevel(root)
        complete_win.title(Config.completion_window_title)
        complete_win.geometry(Config.completion_window_geometry)
        complete_win.resizable(
            Config.completion_window_resize_x, 
            Config.completion_window_resize_y
            )

        tk.Label(
            complete_win, 
            text = Config.completion_window_label_text).pack(
                pady = Config.completion_window_label_pady
                )

        # OK button to close the window
        tk.Button(
            complete_win, 
            text = Config.completion_window_button_text, 
            command = complete_win.destroy).pack()

    except Exception as e:
        popupbox.error_message(e)
        root.destroy()
        sys.exit()

def show_progress_window():
    try:
        global progress_win
        global progress_bar

        progress_win = tk.Toplevel(root)
        progress_win.title(Config.progress_window_title)
        progress_win.geometry(Config.progress_window_geometry)
        progress_win.resizable(Config.progress_window_resizable_x, Config.progress_window_resizable_y)
        progress_win.iconphoto(False, icon_img)

        progress_win.transient(root)
        progress_win.grab_set()

        tk.Label(
            progress_win, 
            text = Config.progress_window_label_text).pack(
                pady = Config.progress_window_label_pady
                )

        progress_bar = ttk.Progressbar(
            progress_win, 
            mode = Config.progress_window_bar_mode, 
            length = Config.progress_window_bar_width
            )
        progress_bar.pack(
            pady = Config.progress_window_bar_pady
            )
        progress_bar.start()

        threading.Thread(
            target = generate_report, 
            daemon = True).start()

    except Exception as e:
        popupbox.error_message(e)
        root.destroy()
        sys.exit()

### Create Main Window ###

root = tk.Tk()
root.title(Config.main_window_title)
root.geometry(Config.main_window_geometry)
root.resizable(
    width = Config.main_window_resizable_width, 
    height = Config.main_window_resizable_height
)
icon_img = tk.PhotoImage(file=os.path.join(App.workspace_path, Config.app_icon_main_path))
root.iconphoto(False, icon_img)

### Create Title ###

tk.Label(
    root, 
    text = Config.title_text, 
    font = (
        Config.main_window_font_type, 
        Config.title_font_size, 
        Config.label_font_style
        )
    ).pack(pady=(Config.title_pady_top, Config.title_pady_bottom))

### Create Text Entry Prompts ###

tk.Label(
    root, 
    text = Config.label_photographer_text,
    font = (
        Config.main_window_font_type, 
        Config.label_font_size, 
        Config.label_font_style
        )
    ).pack(pady = (Config.label_pady_top, Config.label_pady_bottom))
photographer_entry = tk.Entry(
    root, 
    width = Config.text_entry_width
    )
photographer_entry.pack(pady = (Config.text_entry_pady_top, Config.text_entry_pady_bottom))

tk.Label(
    root, 
    text = Config.label_facility_text,
    font = (
        Config.main_window_font_type, 
        Config.label_font_size, 
        Config.label_font_style
        )
    ).pack(pady = (Config.label_pady_top, Config.label_pady_bottom))
facility_entry = tk.Entry(
    root, 
    width = Config.text_entry_width
    )
facility_entry.pack(pady = (Config.text_entry_pady_top, Config.text_entry_pady_bottom))

tk.Label(
    root, 
    text = Config.label_inspection_date_text,
    font=(
        Config.main_window_font_type, 
        Config.label_font_size, 
        Config.label_font_style
        )
    ).pack(pady = (Config.label_pady_top, Config.label_pady_bottom))

inspection_date_entry = DateEntry(
    root,
    width = str(int(Config.text_entry_width) - 2),
    background = Config.date_entry_background_color,
    foreground = Config.date_entry_foreground_color,
    borderwidth = Config.date_entry_border_width,
    date_pattern = Config.date_entry_date_pattern
)
inspection_date_entry.pack(pady=(Config.text_entry_pady_top, Config.text_entry_pady_bottom))

### Create Table ###

tk.Label(
    root, 
    text = Config.label_table_text,
    font = (
        Config.main_window_font_type, 
        Config.label_font_size, 
        Config.label_font_style
        )
    ).pack(pady = (Config.label_pady_top, Config.label_pady_bottom))

columns = [
    Config.table_field_names_file_name, 
    Config.table_field_names_latitude,
    Config.table_field_names_longitude,
    Config.table_field_names_bearing
]

frame = ttk.Frame(root, width = 400)
frame.pack(pady = (Config.table_pady_top, Config.table_pady_bottom)) #.pack(fill="both", expand=True)

tree = ttk.Treeview(
    frame, 
    columns = columns, 
    show = "headings", 
    height = Config.table_row_display_count
    )

for col in columns:
    tree.heading(col, text = col)
    tree.column(col, width = Config.table_column_width)

#tree.pack(pady = (Config.table_pady_top, Config.table_pady_bottom))
tree.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame, orient="vertical", command = tree.yview, width=20)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand = scrollbar.set)

tree.bind("<Double-1>", on_double_click)

### Create Select Button ###

select_button = tk.Button(
    root, 
    text = Config.select_button_text,
    width = Config.select_button_width,
    command = create_image_GPS_table
)
select_button.pack(
    pady = (Config.select_button_pady, 15)
)

### Create File Output Selection Button ###

tk.Label(
    root, 
    text = Config.label_output_file_text,
    font = (
        Config.main_window_font_type, 
        Config.label_font_size, 
        Config.label_font_style
        )
    ).pack(pady = (Config.label_pady_top, Config.label_pady_bottom))

file_selection_frame = tk.Frame(root)
file_selection_frame.pack(pady=(3, 15))

folder_icon_path = os.path.join(App.workspace_path, Config.app_icon_folder_path)
folder_icon = Image.open(folder_icon_path)
folder_icon = folder_icon.resize((14, 14))
folder_icon = ImageTk.PhotoImage(folder_icon)

open_button = tk.Button(file_selection_frame, image=folder_icon, command=open_file_dialog, width=15, height=15)
open_button.pack(
    side="left",
    padx=(0, 5)#,
    #pady = 5
)

file_path_entry = tk.Entry(file_selection_frame, width=37, font=("Verdana", 11), state='readonly')
file_path_entry.pack(
    side="left",
    #pady = 5
)

### Create Generate Report Button ###

generate_button = tk.Button(
    root, 
    text = Config.generate_report_button_text, 
    width = Config.generate_report_button_width,
    font = (
        Config.main_window_font_type,
        Config.generate_report_button_font_size,
        Config.generate_report_button_font_style
        ),
    command = show_progress_window
)
generate_button.pack(
    pady = (Config.generate_report_button_pady_top, Config.generate_report_button_pady_bottom)
)

### Launch Application ###
root.mainloop()
