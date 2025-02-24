import json
import time
import os
import sys
import csv
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

DATA_FILE = "study_data.json"
VERSION = "1.0"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def list_subjects():
    data = load_data()
    if not data:
        print(Fore.RED + "No subjects found!")
        return None
    print(Fore.CYAN + "Available subjects:")
    for subject in data.keys():
        print(Fore.YELLOW + f"- {subject}")
    return data

def new_subject():
    name = input(Fore.GREEN + "Enter subject name: ")
    data = load_data()
    if name in data:
        print(Fore.RED + "Subject already exists!")
        return
    data[name] = {"total_time": 0, "sessions": [], "goal": None}
    save_data(data)
    print(Fore.CYAN + f"Subject '{name}' created.")

def delete_subject():
    data = load_data()
    if not data:
        print(Fore.RED + "No subjects available to delete!")
        time.sleep(2)
        return
    
    list_subjects()
    name = input(Fore.GREEN + "Enter subject name to delete: ")
    if name not in data:
        print(Fore.RED + "Subject not found!")
        time.sleep(2)
        return
    
    del data[name]
    save_data(data)
    print(Fore.YELLOW + f"Subject '{name}' deleted successfully.")
    time.sleep(2)

def edit_sessions():
    data = load_data()
    if not data:
        print(Fore.RED + "No subjects available!")
        time.sleep(2)
        return
    
    list_subjects()
    name = input(Fore.GREEN + "Enter subject name: ")
    if name not in data:
        print(Fore.RED + "Subject not found!")
        time.sleep(2)
        return
    
    subject = data[name]
    if not subject["sessions"]:
        print(Fore.RED + "No sessions available for this subject!")
        time.sleep(2)
        return
    
    print(Fore.MAGENTA + "Sessions:")
    for i, session in enumerate(subject["sessions"]):
        print(Fore.LIGHTWHITE_EX + f"[{i}] {session['timestamp']} → {session['duration']} minutes")
    
    index = int(input(Fore.GREEN + "Enter session index to delete: "))
    if 0 <= index < len(subject["sessions"]):
        del subject["sessions"][index]
        save_data(data)
        print(Fore.YELLOW + "Session deleted successfully.")
        time.sleep(2)
    else:
        print(Fore.RED + "Invalid index!")
        time.sleep(2)

def export_data():
    data = load_data()
    if not data:
        print(Fore.RED + "No data available to export!")
        time.sleep(2)
        return
    
    filename = "study_data_export.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Subject", "Timestamp", "Duration (minutes)"])
        for subject, details in data.items():
            for session in details["sessions"]:
                writer.writerow([subject, session["timestamp"], session["duration"]])
    print(Fore.GREEN + f"Data exported successfully to {filename}")
    time.sleep(2)

def start_timer(subject_name):
    data = load_data()
    print(Fore.GREEN + f"Timer started for {subject_name}. Press Ctrl+C to stop.")
    start_time = time.time()
    try:
        while True:
            elapsed = int(time.time() - start_time)
            print(Fore.YELLOW + f"Elapsed Time: {elapsed} seconds", end="\r")
            time.sleep(1)
    except KeyboardInterrupt:
        duration = int(time.time() - start_time) // 60
        print(Fore.RED + "\nTimer stopped.")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data[subject_name]["sessions"].append({"timestamp": timestamp, "duration": duration})
        data[subject_name]["total_time"] += duration
        save_data(data)
        print(Fore.CYAN + f"Session added: {duration} minutes")
        time.sleep(2)

def load_subject():
    data = load_data()
    if not data:
        print(Fore.RED + "No subjects available!")
        time.sleep(2)
        return
    
    list_subjects()
    name = input(Fore.GREEN + "Enter subject name: ")
    if name not in data:
        print(Fore.RED + "Subject not found!")
        time.sleep(2)
        return
    
    print(Fore.CYAN + f"Loaded subject: {name}")
    print(Fore.YELLOW + f"Total Study Time: {data[name]['total_time']} minutes")
    time.sleep(2)
    start_timer(name)

def set_goal():
    data = load_data()
    if not data:
        print(Fore.RED + "No subjects available to set a goal!")
        time.sleep(2)
        return
    
    list_subjects()
    name = input(Fore.GREEN + "Enter subject name: ")
    if name not in data:
        print(Fore.RED + "Subject not found!")
        time.sleep(2)
        return
    
    goal = int(input(Fore.GREEN + "Enter study goal in minutes: "))
    data[name]["goal"] = goal
    save_data(data)
    print(Fore.CYAN + f"Goal of {goal} minutes set for '{name}'.")
    time.sleep(2)

def main():
    while True:
        clear_screen()
        cmd = input(Fore.MAGENTA + "\nEnter command (new/load/version/exit/goal/delete/edit/export): ").strip().lower()
        if cmd == "new":
            new_subject()
        elif cmd == "load":
            load_subject()
        elif cmd == "version":
            print(Fore.CYAN + f"Version: {VERSION}")
            time.sleep(2)
        elif cmd == "exit":
            break
        elif cmd == "goal":
            set_goal()
        elif cmd == "delete":
            delete_subject()
        elif cmd == "edit":
            edit_sessions()
        elif cmd == "export":
            export_data()
        else:
            print(Fore.RED + "Invalid command!")
            time.sleep(2)

if __name__ == "__main__":
    main()
