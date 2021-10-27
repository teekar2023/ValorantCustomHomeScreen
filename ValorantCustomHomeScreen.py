import os
import sys
import random
import time
import sqlite3
from sqlite3 import Error
import tkinter as tk
from shutil import copy
from threading import Thread
from tkinter import filedialog



def start_game():
    os.system('start "" "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Riot Games\\VALORANT"')
    pass


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        return connection
    except Error as e:
        print(f"The error '{e}' occurred while connecting to database.")
        return


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred while executing query: {query}")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred while executing query: {query}")


def setup():
    if not os.path.exists(f"{cwd}\\videos.sqlite"):
        open(f"{cwd}\\videos.sqlite", "w+")
        pass
    else:
        pass
    connection = create_connection(f"{cwd}\\videos.sqlite")
    create_videos_table = """
    CREATE TABLE IF NOT EXISTS videos (
        id integer PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL
    );
    """
    execute_query(connection, create_videos_table)
    print("You must select atleast one video to use as home screen in order to use this program!")
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", ".mp4")], initialdir=user_dir, title="Select A Video To Use:")
        pass
    except Exception:
        connection.close()
        os.remove(f"{cwd}\\videos.sqlite")
        sys.exit(0)
    s = os.path.split(file_path)
    video = s[1]
    target_dir = f'{cwd}\\Videos\\{video}'
    print("Preparing video for use")
    copy(file_path, target_dir)
    print(f"Selected video copied to {target_dir}")
    add_video = f"""
    INSERT INTO
    videos (name)
    VALUES
    ("{video}");
    """
    execute_query(connection, add_video)
    print("Video appended to list_of_videos")
    print("Video prepared for use")
    print("Restart to use again...")
    time.sleep(3)
    sys.exit()


root = tk.Tk()
root.withdraw()
user_dir = os.path.expanduser('~')
cwd = os.getcwd()
if not os.path.exists(f"{cwd}\\Videos\\"):
    os.mkdir(f"{cwd}\\Videos\\")
    pass
else:
    pass
if not os.path.exists(f"{cwd}\\videos.sqlite"):
    setup()
else:
    pass
connection = create_connection(f"{cwd}\\videos.sqlite")
main_input = input("Press 'V' and then 'ENTER' to customize the list of videos or just press 'ENTER' to continue and start VALORANT...")
if main_input.upper() == "V":
    print("1. Add New Video")
    print("2. Remove A Video")
    print("3. Cancel")
    while True:
        try:
            another_input = int(input("Enter the number of the action you would like to perform:"))
            if another_input == 1:
                file_path = filedialog.askopenfilename(filetypes=[("Video Files", ".mp4")], initialdir=user_dir, title="Select A Video To Use:")
                s = os.path.split(file_path)
                video_s = s[1]
                target_dir = f'{cwd}\\Videos\\{video_s}'
                print("Preparing video for use")
                copy(file_path, target_dir)
                print(f"Selected video copied to {target_dir}")
                select_videos = "SELECT * from videos"
                videos = execute_read_query(connection, select_videos)
                list_of_videos = []
                for video in videos:
                    list_of_videos.append(str(video))
                    pass
                print(list_of_videos)
                if video_s in list_of_videos:
                    print("Video already exists in list of videos")
                    pass
                else:
                    add_video = f"""
                    INSERT INTO
                    videos (name)
                    VALUES
                    ("{video_s}");
                    """
                    execute_query(connection, add_video)
                    print("Video appended to list_of_videos")
                    print("Video prepared for use")
                    pass
                break
            if another_input == 2:
                select_videos = "SELECT * from videos"
                videos = execute_read_query(connection, select_videos)
                for video in videos:
                    print(video)
                while True:
                    remove_input = input("Enter the id number of the video you would like to remove or type 'CANCEL' to cancel:")
                    if remove_input.upper() == "CANCEL" or remove_input.upper() == "C":
                        print("Nothing was removed")
                        break
                    else:
                        search_videos = f"SELECT name from videos WHERE id = {remove_input}"
                        videos = execute_read_query(connection, search_videos)
                        for video in videos:
                            delete_vid = str(video).replace("(", "").replace(")", "").replace("'", "").replace(",", "")
                            print(f"Deleting: {delete_vid}")
                            os.remove(f"{cwd}\\Videos\\{delete_vid}")
                        delete_video = f"""DELETE FROM videos where id = {remove_input}"""
                        execute_query(connection, delete_video)
                        print("Video was removed")
                        select_videos = "SELECT * from videos"
                        videos = execute_read_query(connection, select_videos)
                        list_of_videos = []
                        for video in videos:
                            list_of_videos.append(str(video))
                            pass
                        print(str(list_of_videos))
                        if str(list_of_videos) == "[]":
                            connection.close()
                            os.remove(f"{cwd}\\videos.sqlite")
                            print("Deleted database")
                            pass
                        else:
                            pass
                        break
                break
            if another_input == 3:
                break
            else:
                print("Please enter the integer number of the action you would like to perform such as 1, 2, or 3")
                pass
        except Exception as e:
            print(e)
            print("Please enter the integer number of the action you would like to perform such as 1, 2, or 3")
            pass
    print("Restart to use again...")
    time.sleep(3)
    sys.exit()
else:
    pass
select_videos = "SELECT * from videos"
videos = execute_read_query(connection, select_videos)
list_of_videos = []
for video in videos:
    list_of_videos.append(str(video).replace("(", "").replace(")", "").replace("'", "").replace(",", ""))
    pass
print(str(list_of_videos))
print("--------------")
list_of_vids = [video[0] for video in execute_read_query(connection, "SELECT name FROM videos")]
print(list_of_vids)
vid = random.choice(list_of_vids)
print(f"Video Selected: {vid}")
print("Starting VALORANT")
game_thread = Thread(target=start_game)
game_thread.start()
print("VALORANT Started")
os.system('TIMEOUT 20')
print("Injecting video via XCopy")
os.system(f'xcopy "{cwd}\\Videos\\{vid}" "C:\\Riot Games\\VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu" /K /H /Y')
print("XCopy Executed")
print("Video injected")
print("Removing Default Video")
try:
    os.remove(f'C:\\Riot Games\\VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\HomeScreen.mp4')
    print("Default Video Removed")
    pass
except Exception as e:
    print(f'Error: {e}')
    print("Default Video Not Removed")
    pass
print("Renaming Custom Video")
os.rename(f'C:\\Riot Games\\VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\{vid}', 'C:\\Riot Games\\VALORANT\\live\\ShooterGame\\Content\\Movies\\Menu\\HomeScreen.mp4')
print("Video Renamed")
print("Custom Home Screen Injection Successfull")
os.system('PAUSE')
print("Exiting")
sys.exit(0)
