import os
import json
import signal
from difflib import get_close_matches

# 'colorama' kütüphanesi Python 3.2.3 ile uyumlu olmayabilir. Bu yüzden basit string ile renklendirme kaldırılıyor.
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
    name = input("Name : ")
    if not name:
        print("[ERROR] Please enter a name")
        input("Press Enter to continue...")
        create_threat()
        return
    surname = input("Surname : ")
    
    while True:
        age_input = input("Age : ")
        if age_input == '' or age_input.isdigit(): 
            if age_input:
                age = int(age_input)
            else:
                age = 'Unknown'
            break
        else:
            print("[ERROR] Please enter a valid phone number (numeric) or leave blank.")
    
    while True:
        phone_input = input("Phone Number : ")
        if phone_input == '' or not phone_input.replace(' ', '').isalpha():
            phone_number = phone_input or 'Unknown'
            break
        else:
            print("[ERROR] Please enter a valid phone number (numeric) or leave blank.")
    
    social_media = input("Social Media Accounts : ")
    IP = input("Enter IP Adress: ")
    database[name.lower()] = {
        'Surname': surname or 'Unknown', 
        'Age': age, 
        'Phone Number': phone_number, 
        'Social Media Accounts': social_media or 'Unknown', 
        'IP Adress': IP or 'Unknown'
    }
    save_threats()
    print("Threat saved successfully!")

def found():
    name_to_search = input("Enter the name to search: ").lower()
    if name_to_search in database:
        print("Name: {}".format(name_to_search))
        for key, value in database[name_to_search].items():
            print("{}: {}".format(key, value))
        print("\n[1] Edit\n[99] Delete")
        choice = input("Enter your choice: ")
        if choice == '1':
            edit_threat(name_to_search)
        elif choice == '99':
            delete_threat(name_to_search)
    else:
        similar_names = get_close_matches(name_to_search, database.keys())
        if similar_names:
            print("Name not found. Did you mean {}?".format(", ".join(similar_names)))
            choice = input("[Y/n] ").lower()
            if choice == 'y':
                for name in similar_names:
                    print("\nName : {}".format(name))
                    for key, value in database[name].items():
                        print("{}: {}".format(key, value))
        else:
            print("Name not found.")

def edit_threat(name_to_edit):
    surname = input("Enter new Surname: ")
    age = input("Enter new Age: ")
    phone_number = input("Enter new Phone Number: ")
    social_media = input("Enter new Social Media Accounts: ")
    IP = input("Enter new IP Adress: ")
    database[name_to_edit] = {
        'Surname': surname or 'Unknown', 
        'Age': age or 'Unknown', 
        'Phone Number': phone_number or 'Unknown', 
        'Social Media Accounts': social_media or 'Unknown', 
        'IP Adress': IP or 'Unknown'
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
            print("{}. {}".format(index, name))
        choice = input("Enter the number of the threat to view details: ").strip()
        if choice == '':
            return
        elif choice.isdigit() and 0 < int(choice) <= len(sorted_names):
            choice = int(choice)
            selected_threat = sorted_names[choice - 1]
            clear_screen()
            print("Details of {}:".format(selected_threat))
            for key, value in database[selected_threat].items():
                print("{}: {}".format(key, value))
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
