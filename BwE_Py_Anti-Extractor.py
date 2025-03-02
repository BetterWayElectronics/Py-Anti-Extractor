import os
import re
import random
import sys  
from colorama import init, Fore, Style, Back

# Initialize Colorama
init(autoreset=True)

import ctypes

def set_window_title(title):
    # Encode the title to ANSI
    title_ansi = title.encode('ansi', 'ignore')
    ctypes.windll.kernel32.SetConsoleTitleA(title_ansi)

set_window_title('BwE Py Anti-Extractor')

def print_banner():
    print(Fore.CYAN + "*-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*")
    print(Fore.CYAN + "|" + Fore.WHITE + "            __________          __________               " + Fore.CYAN + "|")
    print(Fore.CYAN + "|" + Fore.WHITE + "            \\______   \\ __  _  _\\_   ____/               " + Fore.CYAN + "|")
    print(Fore.CYAN + ":" + Fore.WHITE + "             |    |  _//  \\/ \\/  /|  __)_                " + Fore.CYAN + ":")
    print(Fore.CYAN + "." + Fore.WHITE + "             |    |   \\\\        //       \\               " + Fore.CYAN + ".")
    print(Fore.CYAN + ":" + Fore.WHITE + "  (\\_/)      |______  / \\__/\\__//______  /               " + Fore.CYAN + ":")
    print(Fore.CYAN + "|" + Fore.WHITE + " ( x_x)             \\/" + Fore.CYAN + "Py Anti-Extractor" + Fore.WHITE + "\\/0.0.3           " + Fore.CYAN + "|")
    print(Fore.CYAN + "|" + Fore.WHITE + " (>  >)                                                  " + Fore.CYAN + "|")
    print(Fore.CYAN + "*-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*\n")

print_banner()


# Function to search for the string to replace based on the provided logic
def find_search_string(data):
    pattern = re.compile(rb'<assemblyIdentity name="(.*?)"')
    match = pattern.search(data)
    if match:
        search_str = match.group(1).decode('utf-8')
        return search_str
    else:
        return None

# Function to search for a string in a binary file
def search_and_replace(filename):
    with open(filename, 'rb') as file:
        data = file.read()
        search_str = find_search_string(data)

        if search_str:
            print(f"\nFound Python App Name: {search_str}")

            # Check if ".py" appears immediately after the found string
            ascii_search = search_str.encode('ascii')
            index = data.find(ascii_search)
            found = False  # Flag to track if we found a suitable string
            while index != -1:
                # Check if the string is surrounded by double quotes
                if (index == 0 or data[index - 1] != 0x22) and (index + len(ascii_search) == len(data) or data[index + len(ascii_search)] != 0x22):
                    # Check if ".py" appears immediately after the string
                    if data[index + len(ascii_search):index + len(ascii_search) + 3] != b".py":
                        print(f"Name Found At: 0x{index:08X}")

                        # Calculate the length of the string in hex
                        length_hex = format(len(ascii_search), 'X')

                        # Generate random hex values between 00 and 1F
                        new_hex = '00 08 ' + ' '.join([format(random.randint(0, 31), '02X') for _ in range(0, len(ascii_search) - 2)])

                        # Replace the string with the generated hex pattern
                        modified_data = data[:index] + bytes.fromhex(new_hex) + data[index + len(ascii_search):]

                        # Save the modified file with _patched suffix
                        patched_filename = filename.replace('.exe', '_patched.exe')

                        # Print the written data
                        print(Fore.YELLOW + "Modified Data: " + new_hex + Style.RESET_ALL)

                        with open(patched_filename, 'wb') as patched_file:
                            patched_file.write(modified_data)

                        print(Fore.GREEN + "Modified Program Saved As: " + patched_filename + Style.RESET_ALL)
                        found = True
                        print("\nPress Enter to Exit...")
                        input()  
                        sys.exit(1)
                        break  # Break out of the loop once we found and patched

                    else:
                        print(f"Found '.py' immediately after the string, continuing to search.")
                        # Move to the next position after ".py" to continue searching
                        index = data.find(ascii_search, index + len(ascii_search) + 3)
                else:
                    # Continue searching from the next position
                    index = data.find(ascii_search, index + 1)

            if not found:
                print("{0:60}".format(Fore.RED + "\nNo Suitable String Found\n" + Style.RESET_ALL),'\r', end=' ')
                print("\nPress Enter to Exit...")
                input()  
                sys.exit(1)
        else:
            print("{0:60}".format(Fore.RED + "\nPython App Name Not Found\n" + Style.RESET_ALL),'\r', end=' ')
            print("\nPress Enter to Exit...")
            input()  
            sys.exit(1)

# Prompt user to select a .exe file from the current directory
exe_files = [file for file in os.listdir() if file.endswith('.exe')]
if not exe_files:
    print("No Programs Found In Current Directory!")
else:
    print("Executables Found:\n")
    for i, exe_file in enumerate(exe_files):
        print(f"{i + 1}. {exe_file}")

    choice = input("\nSelect Executable To Patch: ")

    try:
        choice = int(choice)
        if 1 <= choice <= len(exe_files):
            selected_file = exe_files[choice - 1]
            search_and_replace(selected_file)
        else:
            print("Invalid Choice.")
    except ValueError:
        print("Invalid Input.")
