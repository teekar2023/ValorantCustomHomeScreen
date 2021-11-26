from gettext import install
import os
import sys
import random
import sqlite3
from tokenize import String
import requests
import urllib
import webbrowser
from sqlite3 import Error
import tkinter as tk
from tkinter.messagebox import *
from shutil import copy, rmtree
from threading import Thread
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from tkinter.simpledialog import askstring


def launcher_help():
    help_window = Toplevel(root)
    help_window.geometry("500x600")
    help_window.title("Valorant Custom Home Screen Launcher (HELP)")
    help_text = Text(help_window, bd=0, bg="white", height="8", width="50", font="TrebuchetMS")
    scrollbar = Scrollbar(help_window, command=help_text.yview)
    help_text['yscrollcommand'] = scrollbar.set
    scrollbar.place(x=480, y=0, height=550, width=20)
    help_text.place(x=0, y=0, height=550, width=480)
    help_text.config(font=("TrebuchetMS", 12))
    help_text.insert(END, "Welcome to the Valorant Custom Home Screen Launcher!\n\n")
    help_text.insert(END, "This program is designed to easily help set a custom home screen background in the game Valorant!\n\n")
    help_text.insert(END, "To use this program, you must first start VALORANT from the riot client and then immediately press the start button on the main window of this launcher!\n\n")
    help_text.insert(END, "To Add/Remove videos, press the settings button on the main window and select the corresponding button for what you would like to do!\n\n")
    help_text.insert(END, "To view the videos that are currently registered in the launcher, press the settings button and then press the view videos button!\n\n")
    help_text.insert(END, "And make sure to use the latest version of the launcher to ensure the best possible results and experience!\n\n")
    help_text.insert(END, "Have fun!\n\n")


def update():
    url = "http://github.com/teekar2023/ValorantCustomHomeScreen/releases/latest/"
    r = requests.get(url, allow_redirects=True)
    redirected_url = r.url
    if redirected_url != "https://github.com/teekar2023/ValorantCustomHomeScreen/releases/tag/v2.1.0":
        new_url = str(redirected_url) + "/ValCustomHomeSetup.exe"
        download_url = new_url.replace("tag", "download")
        update_window = Toplevel(root)
        update_window.title("Valorant Custom Home Screen Launcher (UPDATE)")
        update_window.geometry("500x500")
        update_window.resizable(width=False, height=False)
        update_text = Label(update_window,
                            text="There Is A New Update Available! Click The Button Below If You Wish To Download It!")
        update_text.pack()
        int_var = IntVar(update_window)
        update_button = Button(update_window, command=lambda: int_var.set(1), font=("TrebuchetMS", 12, 'bold'),
                               text="Download Update", width="500", height="5",
                               bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
        update_button.pack()
        changelog_text = Text(update_window, bd=0, bg="white", height="25", width="75", font="TrebuchetMS")
        changelog_text.pack()
        try:
            changelog_content = str(
                open(f"{cwd}\\Temp\\changelog.txt", mode="r+", encoding="utf8").read())
            changelog_text.insert(END, changelog_content)
            pass
        except Exception as e:
            changelog_text.insert(END, f"There Was An Error While Trying To Read The Changelog File! Error: {e}")
            pass
        update_button.wait_variable(int_var)
        webbrowser.open(redirected_url)
        webbrowser.open(download_url)
    else:
        showinfo(title="Update", message="You are already using the latest version of the launcher!")


def changelog():
    changelog_window = Toplevel(root)
    changelog_window.title("Valorant Custom Home Screen Launcher (CHANGELOG)")
    changelog_window.geometry("500x500")
    changelog_window.resizable(width=False, height=False)
    changelog_text = Text(changelog_window, bd=0, bg="white", height="25", width="75", font="TrebuchetMS")
    changelog_text.pack()
    try:
        changelog_content = str(
            open(f"{cwd}\\CHANGELOG.txt", mode="r+", encoding="utf8").read())
        changelog_text.insert(END, changelog_content)
        pass
    except Exception as e:
        changelog_text.insert(END, f"There Was An Error While Trying To Read The Changelog File! Error: {e}")
        pass
    check_for_update = Button(changelog_window, command=update, font=("TrebuchetMS", 12, 'bold'),
                              text="Check For Update", width="500", height="5",
                              bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
    check_for_update.pack()


def launcher_license():
    license_window = Toplevel(root)
    license_window.title("Valorant Custom Home Screen Launcher (LICENSE)")
    license_window.geometry("500x500")
    license_window.resizable(width=False, height=False)
    license_text = Text(license_window, bd=0, bg="white", height="35", width="75", font="TrebuchetMS")
    license_text.pack()
    try:
        license_content = str(
            open(f"{cwd}\\LICENSE.txt", mode="r+", encoding="utf8").read())
        license_text.insert(END, license_content)
        pass
    except Exception as e:
        license_text.insert(END, f"There Was An Error While Trying To Read The License File! Error: {e}")
        pass


def about():
    about_window = Toplevel(root)
    about_window.title("Valorant Custom Home Screen Launcher (ABOUT)")
    about_window.geometry("500x500")
    about_window.resizable(width=False, height=False)
    about_text = Text(about_window, bd=0, bg="white", height="25", width="75", font="TrebuchetMS")
    about_text.pack()
    try:
        about_content = str(
            open(f"{cwd}\\ABOUT.txt", mode="r+", encoding="utf8").read())
        about_text.insert(END, about_content)
        pass
    except Exception as e:
        about_text.insert(END, f"There Was An Error While Trying To Read The About File! Error: {e}")
        pass
    license_button = Button(about_window, command=launcher_license, font=("TrebuchetMS", 12, 'bold'),
                            text="License", width="500", height="5",
                            bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff')
    license_button.pack()


def reset():
    reset_confirm = askyesno("Reset", "Are You Sure You Want To Reset The Launcher?")
    if reset_confirm:
        rmtree(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Videos\\")
        connection.close()
        os.remove(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\videos.sqlite")
        os.remove(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Settings\\install_location.txt")
        showinfo("Reset", "The Launcher Has Been Reset! Please Restart To Use Again!")
        restart_confirm = askyesno("Restart", "Would You Like To Restart The Launcher?")
        if restart_confirm:
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        else:
            sys.exit(0)
    else:
        showinfo("Reset", "Reset Cancelled!")


def restart():
    restart_ask = askyesno("Restart", "Would You Like To Restart The Launcher?")
    if restart_ask:
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    else:
        pass


def exit_launcher():
    exit_ask = askyesno("Exit", "Are You Sure You Want To Exit The Launcher?")
    if exit_ask:
        sys.exit(0)
    else:
        pass


def exit_launcher_param(event):
    exit_ask = askyesno("Exit", "Are You Sure You Want To Exit The Launcher?")
    if exit_ask:
        sys.exit(0)
    else:
        pass


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        return connection
    except Error as e:
        showerror(title="Error", message=f"The error '{e}' occurred while connecting to database.")
        return


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        showerror(title="Error", message=f"The error '{e}' occurred while executing query: {query}")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        showerror(title="Error", message=f"The error '{e}' occurred while executing query: {query}")


def setup():
    global start_button
    global settings_button
    try:
        connection.close()  # this may be seen as an error/warning but it is functional
        os.remove(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\videos.sqlite")
        pass
    except Exception:
        pass
    if not os.path.exists(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\videos.sqlite"):
        open(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\videos.sqlite", "w+")
        pass
    else:
        pass
    connection = create_connection(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\videos.sqlite")
    create_videos_table = """
    CREATE TABLE IF NOT EXISTS videos (
        id integer PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL
    );
    """
    execute_query(connection, create_videos_table)
    root.geometry("500x600")
    root.title("Valorant Custom Home Screen Launcher (SETUP)")
    log = Text(root, bd=0, bg="white", height="8", width="50", font="TrebuchetMS")
    scrollbar = Scrollbar(root, command=log.yview)
    log['yscrollcommand'] = scrollbar.set
    scrollbar.place(x=480, y=0, height=550, width=20)
    log.place(x=0, y=0, height=550, width=480)
    log.config(font=("TrebuchetMS", 12))
    log.insert(END, "Welcome to the Valorant Custom Home Screen Launcher!\n\n")
    log.insert(END, f"Current Working Directory: {cwd}\n\n")
    log.insert(END, "You must select atleast one video to use as home screen in order to use this program!\n\n")
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", ".mp4")], initialdir=user_dir, title="Select A Video To Use:")
        pass
    except Exception:
        connection.close()
        os.remove(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\videos.sqlite")
        sys.exit(0)
    s = os.path.split(file_path)
    video = s[1]
    target_dir = f'{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Videos\\{video}'
    log.insert(END, "Preparing Video For Use...\n\n")
    copy(file_path, target_dir)
    log.insert(END, f"Selected Video Copied To {target_dir}\n\n")
    add_video = f"""
    INSERT INTO
    videos (name)
    VALUES
    ("{video}");
    """
    execute_query(connection, add_video)
    log.insert(END, "Video Added To Database...\n\n")
    log.insert(END, "Video Prepared For Use...\n\n")
    if not os.path.exists("C:\\Riot Games\\"):
        install_location = str(askdirectory(title="Select The Location Where The Riot Games Folder Is Installed"))
        if "VALORANT" in install_location.upper() or "RIOT GAMES" not in install_location.upper():
            log.insert(END, "Selected Location Is Not A Valid Valorant Installation Location Please Restart To Use Again\n\n")
            showerror(title="Error", message="Selected Location Is Not A Valid Valorant Installation Location Please Restart To Use Again")
            try:
                connection.close()  # this may be seen as an error/warning but it is functional
                os.remove(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\videos.sqlite")
                pass
            except Exception:
                pass
            pass
        else:
            pass
    else:
        install_location = "C:\\Riot Games\\"
        pass
    log.insert(END, f"Riot Games Location: {install_location}\n\n")
    install_location_file = open(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Settings\\install_location.txt", "w+")
    install_location_file.write(install_location)
    install_location_file.close()
    log.insert(END, "Please Restart This Launcher To Use...")
    restart_ask = askyesno(title="Restart Launcher?", message="Would you like to restart the launcher now?")
    if restart_ask:
        log.insert(END, "Restarting Launcher...\n\n")
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    else:
        sys.exit(0)


def add_video():
    add_video_button.pack_forget()
    remove_video_button.pack_forget()
    view_videos_button.pack_forget()
    other_settings_button.pack_forget()
    root.geometry("500x300")
    start_button.pack()
    settings_button.pack()
    root.title("Valorant Custom Home Screen Launcher")
    add_videos_window = Toplevel(root)
    add_videos_window.title("Valorant Custom Home Screen Launcher (ADD VIDEOS)")
    add_videos_window.geometry("500x600")
    log = Text(add_videos_window, bd=0, bg="white", height="8", width="50", font="TrebuchetMS")
    scrollbar = Scrollbar(add_videos_window, command=log.yview)
    log['yscrollcommand'] = scrollbar.set
    scrollbar.place(x=480, y=0, height=550, width=20)
    log.place(x=0, y=0, height=550, width=480)
    log.config(font=("TrebuchetMS", 12))
    log.insert(END, "Welcome to the Valorant Custom Home Screen Launcher!\n\n")
    log.insert(END, f"Current Working Directory: {cwd}\n\n")
    log.insert(END, "Please select a video to add!\n\n")
    select_videos = "SELECT * from videos"
    videos = execute_read_query(connection, select_videos)
    list_of_videos = []
    for video in videos:
        list_of_videos.append(str(video))
        pass
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", ".mp4")], initialdir=user_dir, title="Select A Video To Use:")
        pass
    except Exception as e:
        showerror(title="Error", message=f"There was an error when you chose the video! Error: {e}")
        add_videos_window.destroy()
    s = os.path.split(file_path)
    video = s[1]
    if video in str(list_of_videos):
        showerror(title="Error", message=f"The video '{video}' is already in use!")
        add_videos_window.destroy()
    else:
        pass
    target_dir = f'{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Videos\\{video}'
    log.insert(END, "Preparing Video For Use...\n\n")
    copy(file_path, target_dir)
    log.insert(END, f"Selected Video Copied To {target_dir}\n\n")
    add_video = f"""
    INSERT INTO
    videos (name)
    VALUES
    ("{video}");
    """
    execute_query(connection, add_video)
    log.insert(END, "Video Added To Database...\n\n")
    log.insert(END, "Video Prepared For Use...\n\n")
    showinfo(title="Video Added", message=f"Video '{video}' has been successfully added!")
    add_videos_window.destroy()


def remove_video():
    add_video_button.pack_forget()
    remove_video_button.pack_forget()
    view_videos_button.pack_forget()
    other_settings_button.pack_forget()
    root.geometry("500x300")
    start_button.pack()
    settings_button.pack()
    root.title("Valorant Custom Home Screen Launcher")
    remove_videos_window = Toplevel(root)
    remove_videos_window.title("Valorant Custom Home Screen Launcher (REMOVE VIDEOS)")
    remove_videos_window.geometry("500x600")
    log = Text(remove_videos_window, bd=0, bg="white", height="8", width="50", font="TrebuchetMS")
    scrollbar = Scrollbar(remove_videos_window, command=log.yview)
    log['yscrollcommand'] = scrollbar.set
    scrollbar.place(x=480, y=0, height=550, width=20)
    log.place(x=0, y=0, height=550, width=480)
    log.config(font=("TrebuchetMS", 12))
    log.insert(END, "Welcome to the Valorant Custom Home Screen Launcher!\n\n")
    log.insert(END, f"Current Working Directory: {cwd}\n\n")
    select_videos = "SELECT * from videos"
    videos = execute_read_query(connection, select_videos)
    log.insert(END, "-----VIDEOS CURRENTLY BEING USED-----\n\n")
    for video in videos:
        log.insert(END, f"{video}\n")
        pass
    try:
        remove_input = askstring(title="Remove Video", prompt="Please select a video to remove from the list on the main window or enter 'CANCEL' to cancel (enter the integer number that appears before the video name):")
        pass
    except Exception as e:
        showerror(title="Error", message=f"Error: {e}")
        remove_videos_window.destroy()
    if remove_input.upper() == "CANCEL" or remove_input.upper() == "C":
        print("Nothing was removed")
        log.insert(END, "Nothing was removed...\n\n")
        showinfo(title="Nothing Removed", message="Nothing was removed!")
        remove_videos_window.destroy()
    else:
        search_videos = f"SELECT name from videos WHERE id = {remove_input}"
        videos = execute_read_query(connection, search_videos)
        for video in videos:
            delete_vid = str(video).replace("(", "").replace(")", "").replace("'", "").replace(",", "")
            log.insert(END, f"Removing Video: {delete_vid}\n\n")
            os.remove(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Videos\\{delete_vid}")
        delete_video = f"""DELETE FROM videos where id = {remove_input}"""
        execute_query(connection, delete_video)
        log.insert(END, "Video Removed From Database...\n\n")
        select_videos = "SELECT * from videos"
        videos = execute_read_query(connection, select_videos)
        list_of_videos = []
        for video in videos:
            list_of_videos.append(str(video))
            pass
        log.insert(END, "-----VIDEOS CURRENTLY BEING USED-----\n\n")
        log.insert(END, f"{list_of_videos}\n\n")
        if str(list_of_videos) == "[]":
            connection.close()
            os.remove(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\videos.sqlite")
            log.insert(END, "Deleted database...")
            restart_ask = askyesno(title="Restart", message="A Restart Is required! Would you like to restart the program?")
            if restart_ask == True:
                os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
            else:
                sys.exit(0)
        else:
            remove_videos_window.destroy()


def view_videos():
    add_video_button.pack_forget()
    remove_video_button.pack_forget()
    view_videos_button.pack_forget()
    other_settings_button.pack_forget()
    root.geometry("500x300")
    start_button.pack()
    settings_button.pack()
    root.title("Valorant Custom Home Screen Launcher")
    view_videos_window = Toplevel(root)
    view_videos_window.title("Valorant Custom Home Screen Launcher (VIEW VIDEOS)")
    view_videos_window.geometry("500x600")
    log = Text(view_videos_window, bd=0, bg="white", height="8", width="50", font="TrebuchetMS")
    scrollbar = Scrollbar(view_videos_window, command=log.yview)
    log['yscrollcommand'] = scrollbar.set
    scrollbar.place(x=480, y=0, height=550, width=20)
    log.place(x=0, y=0, height=550, width=480)
    log.config(font=("TrebuchetMS", 12))
    log.insert(END, "Welcome to the Valorant Custom Home Screen Launcher!\n\n")
    log.insert(END, f"Current Working Directory: {cwd}\n\n")
    select_videos = "SELECT * from videos"
    videos = execute_read_query(connection, select_videos)
    log.insert(END, "-----VIDEOS CURRENTLY BEING USED-----\n\n")
    for video in videos:
        log.insert(END, f"{video}\n")
        pass


def change_install_location():
    install_location == str(askdirectory(title="Change Riot Games Install Location"))
    if "VALORANT" in install_location.upper() or "RIOT GAMES" not in install_location.upper() or "RIOT CLIENT" in install_location.upper():
        showerror(title="Error", message="Invalid Installation Folder!")
        restart_ask = askyesno(title="Restart", message="A Restart Is required! Would you like to restart the program?")
        if restart_ask == True:
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        else:
            sys.exit(0)
    else:
        install_location_file.seek(0)
        install_location_file.truncate(0)
        install_location_file.write(str(install_location))
        install_location_file.close()
        showinfo(title="Success", message="Settings Saved! Please Restart To Use Again!")
        restart_ask = askyesno(title="Restart", message="A Restart Is required! Would you like to restart the program?")
        if restart_ask == True:
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        else:
            sys.exit(0)


def other_settings():
    add_video_button.pack_forget()
    remove_video_button.pack_forget()
    view_videos_button.pack_forget()
    other_settings_button.pack_forget()
    root.geometry("500x300")
    start_button.pack()
    settings_button.pack()
    root.title("Valorant Custom Home Screen Launcher")
    other_settings_window = Toplevel(root)
    other_settings_window.title("Valorant Custom Home Screen Launcher (OTHER SETTINGS)")
    other_settings_window.geometry("500x500")
    other_settings_window.resizable(False, False)
    other_settings_label = Label(other_settings_window, text="Change The Settings You Would Like To And Click The Save Button!")
    other_settings_label.pack()
    install_location_label = Label(other_settings_window, text=f"Current Install Location: {install_location}")
    install_location_label.pack()
    install_location_button = Button(other_settings_window, text="Change Install Location", command=change_install_location)
    install_location_button.pack()


def settings():
    start_button.pack_forget()
    settings_button.pack_forget()
    root.geometry("500x500")
    root.title("Valorant Custom Home Screen Launcher (SETTINGS)")
    add_video_button.pack()
    remove_video_button.pack()
    view_videos_button.pack()
    other_settings_button.pack()
    pass


def main():
    install_location_file = open(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Settings\\install_location.txt", "r")
    install_location = install_location_file.read()
    install_location_file.close()
    select_videos = "SELECT * from videos"
    videos = execute_read_query(connection, select_videos)
    list_of_videos = []
    for video in videos:
        list_of_videos.append(str(video).replace("(", "").replace(")", "").replace("'", "").replace(",", ""))
        pass
    start_button.pack_forget()
    settings_button.pack_forget()
    start_button.pack_forget()
    settings_button.pack_forget()
    root.geometry("500x600")
    root.title("Valorant Custom Home Screen Launcher (RUNNING)")
    log = Text(root, bd=0, bg="white", height="8", width="50", font="TrebuchetMS")
    scrollbar = Scrollbar(root, command=log.yview)
    log['yscrollcommand'] = scrollbar.set
    scrollbar.place(x=480, y=0, height=550, width=20)
    log.place(x=0, y=0, height=550, width=480)
    log.config(font=("TrebuchetMS", 12))
    log.insert(END, "Welcome to the Valorant Custom Home Screen Launcher!\n\n")
    log.insert(END, "WORKING...\n\n")
    log.insert(END, f"Current Working Directory: {cwd}\n\n")
    list_of_vids = [video[0] for video in execute_read_query(connection, "SELECT name FROM videos")]
    log.insert(END, f"Current List Of Registered Videos:{str(list_of_vids)}\n\n")
    vid = random.choice(list_of_vids)
    log.insert(END, f"Video Selected: {vid}\n\n")
    log.insert(END, f"\n\nInjecting Video: {vid}\n\n")
    log.insert(END, "Injecting video via XCopy\n\n")
    os.system(f'xcopy "{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Videos\\{vid}" "{install_location}\\VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu" /K /H /Y')
    log.insert(END, "XCopy Executed!\n\n")
    log.insert(END, "Video Injected!\n\n")
    log.insert(END, "Removing Default Video...\n\n")
    try:
        if os.path.exists(f"{install_location}\\VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\VCT_HomeScreen_Trophy_v4_ZoomedIn.mp4"):
            def_vid = "VCT_HomeScreen_Trophy_v4_ZoomedIn"
            os.remove(f"{install_location}\\VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\VCT_HomeScreen_Trophy_v4_ZoomedIn.mp4")
            log.insert(END, "Default Video Removed!\n\n")
            pass
        else:
            def_vid = "HomeScreen"
            os.remove(f'{install_location}\\VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\HomeScreen.mp4')
            log.insert(END, "Default Video Removed\n\n")
            pass
        pass
    except Exception as e:
        log.insert(END, f'Error: {e}\n')
        log.insert(END, "Default Video Not Removed\n\n")
        showerror(title="Error", message=f"The error '{e}' occurred while removing default video.")
        pass
    log.insert(END, "Renaming Custom Video...\n\n")
    os.rename(f'{install_location}\\VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\{vid}', f'{install_location}\\VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\{def_vid}.mp4')
    log.insert(END, "Custom Video Renamed\n\n")
    log.insert(END, "Custom Home Screen Injection Successfull!\n\n")


root = tk.Tk()
root.title("Valorant Custom Home Screen Launcher")
root.geometry("500x300")
root.resizable(False, False)
user_dir = os.path.expanduser("~")
cwd = os.getcwd()
if not os.path.exists(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\"):
    os.mkdir(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\")
    pass
else:
    pass
if not os.path.exists(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Videos\\"):
    os.mkdir(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Videos\\")
    pass
else:
    pass
if not os.path.exists(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Settings\\"):
    os.mkdir(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Settings\\")
    pass
else:
    pass
if not os.path.exists(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Settings\\install_location.txt"):
    open(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Settings\\install_location.txt", "w+")
    pass
else:
    install_location_file = open(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\Settings\\install_location.txt", "r+")
    install_location = install_location_file.read()
    pass
if not os.path.exists(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\videos.sqlite"):
    showwarning(title="Setup", message="This Launcher Has Not Yet Been Set Up! Please Complete The Following Setup Process To Use This Program!")
    setup()
else:
    connection = create_connection(f"{user_dir}\\Documents\\ValorantCustomHomeScreenLauncher\\videos.sqlite")
    select_videos = "SELECT * from videos"
    videos = execute_read_query(connection, select_videos)
    list_of_videos = []
    for video in videos:
        list_of_videos.append(str(video).replace("(", "").replace(")", "").replace("'", "").replace(",", ""))
        pass
    if "(" not in str(list_of_videos) and ")" not in str(list_of_videos) and "'" not in str(list_of_videos) and "," not in str(list_of_videos):
        showwarning(title="Setup", message="This Launcher Has Not Yet Been Set Up! Please Complete The Following Setup To Use This Program!")
        setup()
    else:
        pass
    pass
menubar = Menu(root)
main_menu = Menu(menubar, tearoff=0)
main_menu.add_command(label="Help", command=launcher_help)
main_menu.add_command(label="Update", command=update)
main_menu.add_command(label="Changelog", command=changelog)
main_menu.add_command(label="About", command=about)
main_menu.add_command(label="Reset", command=reset)
main_menu.add_command(label="Restart", command=restart)
main_menu.add_command(label="Exit", command=exit_launcher)
menubar.add_cascade(label="Menu", menu=main_menu)
root.config(menu=menubar)
root.protocol("WM_DELETE_WINDOW", exit_launcher)
start_button = Button(root, text="Start(Click Imediately After Launching VALORANT)", font=("TrebuchetMS", 12, 'bold'), width="500", height="10", bd=0, bg="#32de97", activebackground="#ffffff", fg='#ffffff', command=main)
settings_button = Button(root, text="Settings(Modify Videos And Customize Program)", font=("TrebuchetMS", 12, 'bold'), width="500", height="10", bd=0, bg="#32de97", activebackground="#ffffff", fg='#ffffff', command=settings)
add_video_button = Button(root, text="Add Video", font=("TrebuchetMS", 12, 'bold'), width="500", height="5", bd=0, bg="#32de97", activebackground="#ffffff", fg='#ffffff', command=add_video)
remove_video_button = Button(root, text="Remove Video", font=("TrebuchetMS", 12, 'bold'), width="500", height="5", bd=0, bg="#32de97", activebackground="#ffffff", fg='#ffffff', command=remove_video)
view_videos_button = Button(root, text="View Videos", font=("TrebuchetMS", 12, 'bold'), width="500", height="5", bd=0, bg="#32de97", activebackground="#ffffff", fg='#ffffff', command=view_videos)
other_settings_button = Button(root, text="Other Settings", font=("TrebuchetMS", 12, 'bold'), width="500", height="5", bd=0, bg="#32de97", activebackground="#ffffff", fg='#ffffff', command=other_settings)
start_button.pack()
settings_button.pack()
try:
    url = "http://github.com/teekar2023/ValorantCustomHomeScreen/releases/latest/"
    r = requests.get(url, allow_redirects=True)
    redirected_url = r.url
    if redirected_url != "https://github.com/teekar2023/ValorantCustomHomeScreen/releases/tag/v2.1.0":
        changelog_url = "https://raw.githubusercontent.com/teekar2023/ValorantCustomHomeScreen/master/CHANGELOG.txt"
        changelog_download = urllib.request.urlopen(changelog_url)
        if not os.path.exists(f"{cwd}\\Temp\\"):
            os.mkdir(f"{cwd}\\Temp\\")
            pass
        else:
            pass
        try:
            open(f"{cwd}\\Temp\\changelog.txt", mode="w+", encoding="utf8").truncate()
        except Exception:
            pass
        changelog_file = open(f"{cwd}\\Temp\\changelog.txt", mode="wb")
        try:
            while True:
                changelog_data = changelog_download.read()
                if not changelog_data:
                    break
                else:
                    changelog_file.write(changelog_data)
                    pass
        except Exception:
            changelog_file.write(str.encode("There Was An Error Downloading Changelog Information!"))
            pass
        changelog_file.close()
        showinfo(title="Update Available", message="There Is An Update Available! Please Install The Update And See What Is New By Clicking The Update Button In The Dropdown Menu!")
        pass
    else:
        pass
except Exception as e:
    showerror(title="Error", message=f"The error '{e}' occurred while checking for updates/downloading changelog.")
    pass
string_var = StringVar()
root.mainloop()
