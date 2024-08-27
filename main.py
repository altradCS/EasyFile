import os
import shutil
import sys 
import time
import pyfiglet
import paramiko
import requests
from zipfile import ZipFile, BadZipFile
from pathlib import Path
from termcolor import colored  # Add this if you want to use colored text

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

homePath = Path.home()

def clear_screen():
    # Cross-platform screen clear function
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/Mac
        os.system('clear')

def mainMenu():
    try:
        print(f'''
{colored(pyfiglet.figlet_format('EasyFile', font='slant'), 'green', attrs=['bold'])}
----------------------------------------------------------------------------------------------------------------------------------------
    1. {color.BOLD + 'Remote File Management' + color.END}
    2. {color.BOLD + 'Manage Files' + color.END}
    3. {color.BOLD + 'Download Files From The Internet' + color.END}
-----------------------------------------------------------------------------------------------------------------------------------------
CTRL-C To Go Back Anytime.
            ''')
        while True:
            choice = input("Choose a Number: ")

            if choice.strip() == "1":
                remoteFileManagement()
            elif choice.strip() == "2":
                manageFiles()
            elif choice.strip() == "3":
                downloadFiles()
            else:
                print("Invalid Choice")
    except KeyboardInterrupt:
        sys.exit("\n Exiting Program...")

def main():
    dot = "."
    checkSystem = "Checking your system before starting EasyFile Management System."

    for i in range(3):
        clear_screen()  # Use cross-platform clear function
        print(checkSystem)
        time.sleep(0.5)
        clear_screen()  # Use cross-platform clear function
        checkSystem = checkSystem + dot

    print(color.BOLD + color.GREEN + "\t EasyFile Management System" + color.END)
    time.sleep(0.1)
    clear_screen()  # Use cross-platform clear function
    mainMenu()

if __name__ == "__main__":
    main()
