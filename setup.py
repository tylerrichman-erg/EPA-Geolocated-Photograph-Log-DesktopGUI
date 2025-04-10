#import configparser
import os
import shutil
import subprocess

class App:
    def __init__(self):
        self.workspace_path = r""

if __name__ == "__main__":
    App = App()

    App.workspace_path = os.path.abspath(os.path.dirname(__file__))
    
    main_exe_folder_location = os.path.join(App.workspace_path, r"exe")
    activate_venv_command = os.path.join(App.workspace_path, r"python-env\Scripts\activate.bat")
    python_exe_location = os.path.join(App.workspace_path, r"python-env\Scripts\python.exe")
    pip_exe_location = os.path.join(App.workspace_path, r"python-env\Scripts\pip.exe")
    pyinstaller_exe_location = os.path.join(App.workspace_path, r"python-env\Scripts\pyinstaller.exe")
    main_py_location = os.path.join(App.workspace_path, r"dev\main.py")
    icon_location = os.path.join(App.workspace_path, r"misc\icon.png") #! Change with path of new icon.
    output_exe_location = os.path.join(App.workspace_path, r"exe\dist\main.exe")
    final_exe_location = os.path.join(App.workspace_path, r"EPA-Geolocated-Photograph-Log-DesktopGUI_0_0_1.exe")

    if os.path.exists(os.path.join(App.workspace_path, "python-env")):
        shutil.rmtree(os.path.join(App.workspace_path, "python-env"))

    if os.path.exists(main_exe_folder_location):
        shutil.rmtree(main_exe_folder_location)

    if not os.path.exists(main_exe_folder_location):
        os.makedirs(main_exe_folder_location)

    subprocess.run(['python', '-m', 'venv', os.path.join(App.workspace_path, "python-env")], check=True)

    ### All Python libraries used in tool need to be included below ###
    #subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "tk==8.6.14"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "tkcalendar"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "folium"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "pillow"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "selenium"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "pandas"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "python-docx"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "piexif"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "pyinstaller"], check=True)

    subprocess.run([activate_venv_command, "&&", "CD", main_exe_folder_location, "&&", pyinstaller_exe_location, "--onefile", f"--icon={icon_location}", main_py_location], check=True)

    shutil.copy(
        output_exe_location,
        final_exe_location
        )