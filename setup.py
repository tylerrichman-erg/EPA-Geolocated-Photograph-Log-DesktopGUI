import configparser
import os
import shutil
import subprocess

class App:
    def __init__(self):
        self.workspace_path = r""
        self.config_file_path = r""

class Config:
    def __init__(self, config):
        ### Map Window Properties ###
        self.main_window_title = config['Main Window Properties']['title']
        self.main_window_geometry = config['Main Window Properties']['geometry']
        self.main_window_resizable_width = config['Main Window Properties']['resizable_width']
        self.main_window_resizable_height = config['Main Window Properties']['resizable_height']

        ### Image Properties ###
        self.img_width = config['Image Properties']['width']
        self.img_height = config['Image Properties']['height']

        ### Map Properties ###
        self.map_control_scale = config['Map Properties']['control_scale']
        self.map_zoom_control = config['Map Properties']['zoom_control']
        self.map_dragging = config['Map Properties']['dragging']

        ### Icon Properties ###
        self.icon_name = config['Icon Properties']['name']
        self.icon_size = config['Icon Properties']['size']
        self.icon_shape = config['Icon Properties']['shape']
        self.icon_border_color = config['Icon Properties']['border_color']
        self.icon_border_width = config['Icon Properties']['border_width']
        self.icon_background_color = config['Icon Properties']['background_color']
        self.icon_text_color = config['Icon Properties']['text_color']

if __name__ == "__main__":
    App = App()

    config = configparser.ConfigParser()
    config.read(App.config_file_path)
    Config = Config(config)

    main_exe_folder_location = os.path.join(App.workspace_folder, r"exe")
    activate_venv_command = os.path.join(App.workspace_folder, r"python-env\Scripts\activate.bat")
    python_exe_location = os.path.join(App.workspace_folder, r"python-env\Scripts\python.exe")
    pip_exe_location = os.path.join(App.workspace_folder, r"python-env\Scripts\pip.exe")
    pyinstaller_exe_location = os.path.join(App.workspace_folder, r"python-env\Scripts\pyinstaller.exe")
    main_py_location = os.path.join(App.workspace_folder, r"dev\main.py")
    icon_location = os.path.join(App.workspace_folder, r"dev\icons\icons8-f-67.png") #! Change with path of new icon.
    output_exe_location = os.path.join(App.workspace_folder, r"exe\dist\main.exe")
    final_exe_location = os.path.join(App.workspace_folder, r"EPA Geolocated Photograph Log.exe")

    if os.path.exists(os.path.join(App.workspace_folder, "python-env")):
        shutil.rmtree(os.path.join(App.workspace_folder, "python-env"))

    if os.path.exists(main_exe_folder_location):
        shutil.rmtree(main_exe_folder_location)

    if not os.path.exists(main_exe_folder_location):
        os.makedirs(main_exe_folder_location)

    subprocess.run(['python', '-m', 'venv', os.path.join(App.workspace_folder, "python-env")], check=True)

    ### All Python libraries used in tool need to be included below ###
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "geopandas=1.0.1"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "tk"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "folium"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "pillow"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "selenium"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "pyinstaller"], check=True)

    subprocess.run([activate_venv_command, "&&", "CD", main_exe_folder_location, "&&", pyinstaller_exe_location, "--onefile", f"--icon={icon_location}",main_py_location], check=True)

    shutil.copy(
        output_exe_location,
        final_exe_location
        )
