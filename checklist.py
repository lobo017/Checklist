import sys
import re
import csv
import os
from tqdm import tqdm
from colorama import Fore
import time


def main():
    file_name = ""
    counter = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    user = input("New or Existing Account? \n(Enter \"Exit\" to Exit) ").lower()
    if user == "exit":
        sys.exit("\nThank you!")
    for _ in range(3):
        if user != "new" and user != "existing" and user != "n" and user != "e":
            user = input("Please enter New or Existing: ").lower()
            counter += 1
            if counter == 3:
                sys.exit("Too many incorrect tries")
        else:
            if user == "new":
                file_name = new_user()
                break
            else:
                file_name = existing_user()
                break
    login = input("\nWould You Like to Open Your File? ").lower()
    if login == 'y' or login == 'yes':
        writeToFile(file_name)
    elif login == 'n' or login == 'no':
        sys.exit("\nThank you!")


def new_user():
    username = input("\nWelcome New User!\nPlease Enter a Username: ")
    validate_username(username)
    password = input("Please Enter a Password: ")
    validate_password(password)
    title = input("Please Enter a File Name: ")
    Accounts = [{"Username": username, "Password": password, "Title": title}]
    names = ["Username", "Password", "Title"]
    with open("accounts.csv", "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=names)
        writer.writerows(Accounts)
    return title


def existing_user():
    while True:
        username = input("Please Enter Your Username: ")
        password = input("Please Enter Your Password: ")
        key = checkAccount(username, password)
        if not key:
            print("Incorrect Username or Password, Please Try Again")
        else:
            break
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Welcome Back {username}\n")
    title = input("Please Enter your File Name: ")
    while True:
        if title == key:
            return title
        else:
            title = input("Incorrect Title, Please Try Again: ")
            key = checkAccount(username, password)
            if not key:
                continue
            else:
                return title


def validate_username(username):
    username_list = []
    with open("accounts.csv", "r") as file:
        reader = csv.reader(file)
        for lines in reader:
            username_list.append(lines[0])
    while True:
        if username in username_list:
            print("Username Already Exists")
        else:
            break
        username = input("Please Enter a Username: ")


def validate_password(password):
    while True:
        if len(password) < 8:
            print("Password needs to be at least 8 digits")
        elif re.search('[0-9]', password) is None:
            print("Password needs a number, (0-9)")
        elif re.search('[A-Z]', password) is None:
            print("Password needs a capital letter, (A-Z)")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Welcome!\n")
            return True
        password = input("Please Enter a Password: ")


def checkAccount(username, password):
    username_list = []
    password_list = []
    title_list = []
    with open("accounts.csv", "r") as file:
        reader = csv.reader(file)
        for lines in reader:
            username_list.append(lines[0])
            password_list.append(lines[1])
            title_list.append(lines[2])
    if username in username_list:
        index = username_list.index(username)
        if password in password_list and password == password_list[index]:
            return title_list[index]
        else:
            return False
    else:
        return False


def writeToFile(name):
    with open(f"{name}.txt", "a+") as _:
        if os.stat(f"{name}.txt").st_size == 0:
            insert = input("\nFile is Empty\nWould You Like to Add Content? ")
            if insert == 'y' or insert == 'yes':
                os.system('cls' if os.name == 'nt' else 'clear')
                fileInput(name)
            elif insert == 'n' or insert == 'no':
                os.system('cls' if os.name == 'nt' else 'clear')
                sys.exit("\nThank you!")
    with open(f"{name}.txt", "r") as file1:
        contents = file1.read()
        print("\nYour Current File Content:\n", contents,sep="")
        insert = input("Would You Like to Add Content? ")
        if insert == 'y' or insert == 'yes':
            fileInput(name)
        elif insert == 'n' or insert == 'no':
            delete = input("Would You Like to Delete Content? ")
            if delete == 'y' or delete == 'yes':
                print(contents)
                deleteContent(name)
            elif delete == 'n' or delete == 'no':
                os.system('cls' if os.name == 'nt' else 'clear')
                choices(name)
        with open(f"{name}.txt") as file2:
            contents = file2.read()
            print("Printing Your File\n", contents, sep="")
            choices(name)


def fileInput(name):
    os.system('cls' if os.name == 'nt' else 'clear')
    object = 0
    line_content = []
    with open(f"{name}.txt", "a+") as file:
        try:
            if os.stat(f"{name}.txt").st_size == 0:
                counter = 0
            else:
                with open(f"{name}.txt", "r+") as file1:
                    for lines in file1:
                        line_content.append(lines)
                    for items in range(len(line_content)):
                        object = line_content.index(line_content[-1])
                    counter = object + 1
                file1.close()
        except IndexError:
            counter = line_content.index("")
        try:
            counter +=1
            create = input(
                f"You Can Now Add to Your Checklist\nPress Ctrl+C to Exit Edit Mode\n\n{counter}. ")
            while True:
                counter += 1
                file.write(f"{counter-1}. {create}\n")
                create = input(f"{counter}. ")
        except KeyboardInterrupt:
            file.close()
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Edit Mode Ended\n")
            choices(name)


def deleteContent(name):
    while True:
        try:
            with open(f"{name}.txt", "r") as file3:
                content = file3.read()
            delete = int(input(f"\nWhich Item Do You Want Removed?\n\n{content}\n").replace(".","").strip())
            break
        except ValueError:
            delete = input("\nPlease Input the Number: ").replace(".","").strip()

    with open(f"{name}.txt", "r+") as file:
        lines = []
        try:
            for line in file:
                _,contents = line.split(".")
                lines.append(contents)
            file.close()
            counter = 1
            for _ in range(len(lines)):
                if delete == counter and lines[delete-1] == lines[counter-1]:
                    lines.remove(lines[counter-1])
                    break
                else:
                    counter += 1
            with open(f"{name}.txt", "r+") as file2:
                file2.truncate(0)
            with open(f"{name}.txt", "w") as file1:
                for line in lines:
                    index = lines.index(line) + 1
                    line = f"{index}.{line}"
                    file1.write(line)
            os.system('cls' if os.name == 'nt' else 'clear')
            choices(name)
        except ValueError:
            print("Line Not Found")


def choices(name):
    with open(f"{name}.txt", "r") as file:
        while True:
            content = file.read()
            print(f"File Contents:\n{content}")
            choice = input(
                "What Would You Like to Do?\n[1] Add Items\n[2] Delete Item\n[3] Log Off\n[4] Exit\n\n")
            if choice == "1":
                load()
                fileInput(name)
            elif choice == "2":
                load()
                deleteContent(name)
            elif choice == "3":
                load()
                print()
                main()
            elif choice == "4":
                os.system('cls' if os.name == 'nt' else 'clear')
                sys.exit("Thank You!")
            else:
                print("Please Choose One of the Given Options")
                choices(name)


def load():
    os.system('cls' if os.name == 'nt' else 'clear')
    for _ in tqdm(range(100),
                  desc=Fore.RED + "Loading. . .",
                  ascii=False, ncols=75):
        time.sleep(0.01)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + "Complete. . .")
    time.sleep(0.5)
    print(Fore.WHITE)
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    main()