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
    icon_location = os.path.join(App.workspace_path, r"img\icon\main.png") #! Change with path of new icon.
    output_exe_location = os.path.join(App.workspace_path, r"exe\dist\main.exe")
    final_exe_location = os.path.join(App.workspace_path, r"EPA-Geolocated-Photograph-Log-DesktopGUI_0_1_0.exe")

    if os.path.exists(os.path.join(App.workspace_path, "python-env")):
        shutil.rmtree(os.path.join(App.workspace_path, "python-env"))

    if os.path.exists(main_exe_folder_location):
        shutil.rmtree(main_exe_folder_location)

    if not os.path.exists(main_exe_folder_location):
        os.makedirs(main_exe_folder_location)

    items = os.listdir(App.workspace_path)
    filtered_items = [x for x in items if x not in [".git", ".gitattributes", "README.md"]]

    for filtered_item in filtered_items:
        if os.path.isdir(filtered_item): # Check if the item is a directory
            shutil.copytree(
                os.path.join(App.workspace_path, filtered_item),
                os.path.join(App.workspace_path, "exe", filtered_item)
            )
        else: # Check if the item is a file
            shutil.copy(
                os.path.join(App.workspace_path, filtered_item),
                os.path.join(App.workspace_path, "exe", filtered_item)
            )

    subprocess.run(['python', '-m', 'venv', os.path.join(App.workspace_path, "python-env")], check=True)

    ### All Python libraries used in tool need to be included below ###
    #subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "tk"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "tkcalendar"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "folium"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "pillow"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "selenium"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "pandas"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "python-docx"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "piexif"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "pyinstaller"], check=True)

    try:
        command = (
            f'"{activate_venv_command}" && '
            f'cd "{main_exe_folder_location}" && '
            f'"{pyinstaller_exe_location}" --onefile --noconsole '
            f'--icon="{icon_location}" '
            f'--add-data=dev;dev '
            f'--add-data=img;img '
            f'--add-data=txt;txt '
            f'--add-data=setup.py;. '
            f'--add-data=config.ini;. '
            f'"{main_py_location}"'
        )
        subprocess.run(command, shell=True, check=True)

    except:
        proc = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(proc.stdout)
        print(proc.stderr)

    shutil.copy(
        output_exe_location,
        final_exe_location
        )