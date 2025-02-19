import json
import time
import os
import sys
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

def load_subject():
    clear_screen()
    data = list_subjects()
    if not data:
        return
    
    name = input(Fore.GREEN + "Enter subject name: ")
    if name not in data:
        print(Fore.RED + "Subject not found!")
        return
    
    subject = data[name]
    while True:
        clear_screen()
        print(Fore.CYAN + f"\nSubject: {name}")
        print(Fore.YELLOW + f"Total Study Time: {subject['total_time']} minutes")
        if subject["goal"]:
            print(Fore.GREEN + f"Goal: {subject['goal']} minutes")
        print(Fore.MAGENTA + "Sessions:")
        for session in subject["sessions"]:
            print(Fore.LIGHTWHITE_EX + f"- {session['timestamp']} → {session['duration']} minutes")
        
        if subject["goal"]:
            progress = min(subject["total_time"] / subject["goal"], 1)
            bar_length = 20
            filled_length = int(bar_length * progress)
            print(Fore.CYAN + "Progress:")
            print(Fore.YELLOW + "[" + "█" * filled_length + "-" * (bar_length - filled_length) + "]" + f" {progress * 100:.1f}%")
        
        print(Fore.CYAN + "\nPress Enter to start timer or type 'exit' to return.")
        choice = input().strip().lower()
        if choice == 'exit':
            return
        start_timer(name, data)

def start_timer(name, data):
    print(Fore.GREEN + "Timer started. Press Ctrl+C to stop.")
    start_time = time.time()
    try:
        while True:
            elapsed = int(time.time() - start_time)
            minutes, seconds = divmod(elapsed, 60)
            clear_screen()
            print(Fore.GREEN + "Timer started. Press Ctrl+C to stop.")
            print(Fore.CYAN + f"Studying {name} - Time: {minutes:02}:{seconds:02}")
            time.sleep(1)
    except KeyboardInterrupt:
        elapsed_minutes = max(1, elapsed // 60)  # Ensure at least 1 min is recorded
        print(Fore.YELLOW + f"\nSession ended. Total time: {elapsed_minutes} minutes.")
        data[name]["total_time"] += elapsed_minutes
        data[name]["sessions"].append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "duration": elapsed_minutes})
        save_data(data)
        print(Fore.CYAN + "Returning to menu...")
        time.sleep(2)
        return

def set_goal():
    data = load_data()
    if not data:
        print(Fore.RED + "No subjects available to set a goal!")
        return
    
    print(Fore.CYAN + "Available subjects:")
    for subject in data.keys():
        print(Fore.YELLOW + f"- {subject}")
    
    name = input(Fore.GREEN + "Enter subject name: ")
    if name not in data:
        print(Fore.RED + "Subject not found!")
        return
    
    goal = int(input(Fore.CYAN + "Enter goal in minutes: "))
    data[name]["goal"] = goal
    save_data(data)
    print(Fore.YELLOW + f"Goal set for {name}: {goal} minutes")

def main():
    while True:
        clear_screen()
        cmd = input(Fore.MAGENTA + "\nEnter command (new/load/version/exit/goal): ").strip().lower()
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
        else:
            print(Fore.RED + "Invalid command!")
            time.sleep(2)

if __name__ == "__main__":
    main()
