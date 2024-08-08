import os
import json
from difflib import get_close_matches

database = {}
file_name = "threats.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_threats():
    with open(file_name, "w") as file:
        json.dump(database, file)

def load_threats():
    global database
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            database = json.load(file)

def create_threat():
    clear_screen()
    name = input("Name: ")
    if not name:
        print("[ERROR] Please enter a name")
        input("Press Enter to continue...")
        create_threat()
        return
    surname = input("Surname: ")

    while True:
        age_input = input("Age: ")
        if age_input == '' or age_input.isdigit(): 
            age = int(age_input) if age_input else 'Unknown'
            break
        else:
            print("[ERROR] Please enter a valid age (numeric) or leave blank.")
    
    while True:
        phone_input = input("Phone Number: ")
        if phone_input == '' or phone_input.isdigit():
            phone_number = phone_input or 'Unknown'
            break
        else:
            print("[ERROR] Please enter a valid phone number (numeric) or leave blank.")
    
    social_media = input("Social Media Accounts: ")
    IP = input("Enter IP Address: ")
    database[name.lower()] = {
        'Surname': surname or 'Unknown',
        'Age': age or 'Unknown',
        'Phone Number': phone_number or 'Unknown',
        'Social Media Accounts': social_media or 'Unknown',
        'IP Address': IP or 'Unknown'
    }
    save_threats()
    print("Threat saved successfully!")

def found():
    name_to_search = input("Enter the name to search: ").lower()
    if name_to_search in database:
        print(f"Name: {name_to_search}")
        for key, value in database[name_to_search].items():
            print(f"{key}: {value}")
        print("\n[1] Edit\n[99] Delete")
        choice = input("Enter your choice: ")
        if choice == '1':
            edit_threat(name_to_search)
        elif choice == '99':
            delete_threat(name_to_search)
    else:
        similar_names = get_close_matches(name_to_search, database.keys())
        if similar_names:
            print(f"Name not found. Did you mean {', '.join(similar_names)}?")
            choice = input("[Y/n] ").lower()
            if choice == 'y':
                for name in similar_names:
                    print(f"\nName: {name}")
                    for key, value in database[name].items():
                        print(f"{key}: {value}")
        else:
            print("[ERROR] Name not found.")

def edit_threat(name_to_edit):
    surname = input("Enter new Surname: ")
    age = input("Enter new Age: ")
    phone_number = input("Enter new Phone Number: ")
    social_media = input("Enter new Social Media Accounts: ")
    IP = input("Enter new IP Address: ")
    database[name_to_edit] = {
        'Surname': surname or 'Unknown',
        'Age': age or 'Unknown',
        'Phone Number': phone_number or 'Unknown',
        'Social Media Accounts': social_media or 'Unknown',
        'IP Address': IP or 'Unknown'
    }
    save_threats()
    print("Threat edited successfully.")

def delete_threat(name_to_delete):
    del database[name_to_delete]
    save_threats()
    print("Threat deleted successfully.")

def saved_threats():
    if database:
        clear_screen()
        print("Saved Threats:")
        sorted_names = list(reversed(list(database.keys())))
        for index, name in enumerate(sorted_names, 1):
            print(f"{index}. {name}")
        choice = input("Enter the number of the threat to view details: ").strip()
        if choice == '':
            return
        elif choice.isdigit() and 0 < int(choice) <= len(sorted_names):
            choice = int(choice)
            selected_threat = sorted_names[choice - 1]
            clear_screen()
            print(f"Details of {selected_threat}:")
            for key, value in database[selected_threat].items():
                print(f"{key}: {value}")
            print("\n[1] Edit\n[99] Delete")
            choice = input("Enter your choice: ")
            if choice == '1':
                edit_threat(selected_threat)
            elif choice == '99':
                delete_threat(selected_threat)
        else:
            print("[ERROR] Invalid input. Please enter a valid threat number.")
    else:
        print("No threats saved.")

import signal

def signal_handler(signal, frame):
    print("\nExiting...")
    save_threats()
    exit(0)

def set_signal_handler():
    signal.signal(signal.SIGINT, signal_handler)

def main():
    set_signal_handler()
    load_threats()
    while True:
        clear_screen()
        print("▀█▀ █░█ █▀▀▄ █▀ ▄▀▄ ▀█▀")
        print("░█░ █▀█ █▐█▀ █▀ █▀█ ░█░")
        print("░▀░ ▀░▀ ▀░▀▀ ▀▀ ▀░▀ ░▀░")
        print("----{By No_Name.exe}----")
        print("")

        print("[0] Exit\n[1] Create Threat\n[2] Found\n[3] Saved Threats\n")
        choice = input("Enter your choice: ")

        if choice == '0':
            signal_handler(None, None)
        elif choice == '1':
            create_threat()
            input("Press Enter to continue...")
        elif choice == '2':
            found()
            input("Press Enter to continue...")
        elif choice == '3':
            saved_threats()
            input("Press Enter to continue...")
        else:
            print("[ERROR] Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
