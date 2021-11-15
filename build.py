import os
from shutil import copy

cwd = os.getcwd()
os.system('pyinstaller -i download.ico ValorantCustomHomeScreen.pyw')
copy(f"{cwd}\\CHANGELOG.txt", f"{cwd}\\dist\\ValorantCustomHomeScreen\\CHANGELOG.txt")
copy(f"{cwd}\\ABOUT.txt", f"{cwd}\\dist\\ValorantCustomHomeScreen\\ABOUT.txt")
copy(f"{cwd}\\LICENSE.txt", f"{cwd}\\dist\\ValorantCustomHomeScreen\\LICENSE.txt")
