import os
from shutil import copy

cwd = os.getcwd()
os.system('pyinstaller -i download.ico ValorantCustomHomeScreen.py')
copy(f"{cwd}\\LICENSE.txt", f"{cwd}\\dist\\ValorantCustomHomeScreen\\LICENSE.txt")
